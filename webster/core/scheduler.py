"""
WEBSTER Task Scheduler
======================
Schedules and manages timed tasks, reminders, and recurring jobs.
"""

import time
import uuid
import threading
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

from webster.core.logger import Logger


class ScheduleType(Enum):
    """Types of scheduled tasks."""
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    INTERVAL = "interval"
    CRON = "cron"


class TaskStatus(Enum):
    """Status of a scheduled task."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ScheduledTask:
    """A task scheduled for future execution."""
    id: str
    name: str
    schedule_type: ScheduleType
    callback: Callable
    interval_seconds: int = 0
    run_at: Optional[datetime] = None
    recurring: bool = False
    status: TaskStatus = TaskStatus.PENDING
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


class Scheduler:
    """
    Background task scheduler for timed operations.
    One-time delayed tasks, recurring tasks, reminders, alarms.
    """

    def __init__(self):
        self.logger = Logger().get_logger("SCHEDULER")
        self._tasks: Dict[str, ScheduledTask] = {}
        self._running = False
        self._worker_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self.logger.info("Scheduler initialized")

    def schedule_once(self, name: str, callback: Callable, delay_seconds: int, *args, **kwargs) -> str:
        """Schedule a one-time task after a delay."""
        task_id = str(uuid.uuid4())[:8]
        run_at = datetime.now() + timedelta(seconds=delay_seconds)
        task = ScheduledTask(
            id=task_id, name=name, schedule_type=ScheduleType.ONCE,
            callback=callback, run_at=run_at, next_run=run_at,
            args=args, kwargs=kwargs
        )
        with self._lock:
            self._tasks[task_id] = task
        self.logger.debug(f"Scheduled one-time: {name} in {delay_seconds}s [ID: {task_id}]")
        return task_id

    def schedule_at(self, name: str, callback: Callable, run_at: datetime, *args, **kwargs) -> str:
        """Schedule a task at a specific datetime."""
        task_id = str(uuid.uuid4())[:8]
        task = ScheduledTask(
            id=task_id, name=name, schedule_type=ScheduleType.ONCE,
            callback=callback, run_at=run_at, next_run=run_at,
            args=args, kwargs=kwargs
        )
        with self._lock:
            self._tasks[task_id] = task
        self.logger.debug(f"Scheduled at: {name} at {run_at.isoformat()} [ID: {task_id}]")
        return task_id

    def schedule_daily(self, name: str, callback: Callable, hour: int = 0, minute: int = 0, *args, **kwargs) -> str:
        """Schedule a daily recurring task."""
        task_id = str(uuid.uuid4())[:8]
        now = datetime.now()
        run_at = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if run_at <= now:
            run_at += timedelta(days=1)
        task = ScheduledTask(
            id=task_id, name=name, schedule_type=ScheduleType.DAILY,
            callback=callback, recurring=True, run_at=run_at, next_run=run_at,
            args=args, kwargs=kwargs
        )
        with self._lock:
            self._tasks[task_id] = task
        self.logger.debug(f"Scheduled daily: {name} at {hour:02d}:{minute:02d} [ID: {task_id}]")
        return task_id

    def schedule_interval(self, name: str, callback: Callable, interval_seconds: int, *args, **kwargs) -> str:
        """Schedule a recurring task at a fixed interval."""
        task_id = str(uuid.uuid4())[:8]
        run_at = datetime.now() + timedelta(seconds=interval_seconds)
        task = ScheduledTask(
            id=task_id, name=name, schedule_type=ScheduleType.INTERVAL,
            callback=callback, interval_seconds=interval_seconds,
            recurring=True, run_at=run_at, next_run=run_at,
            args=args, kwargs=kwargs
        )
        with self._lock:
            self._tasks[task_id] = task
        self.logger.debug(f"Scheduled interval: {name} every {interval_seconds}s [ID: {task_id}]")
        return task_id

    def cancel(self, task_id: str) -> bool:
        """Cancel a scheduled task."""
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].status = TaskStatus.CANCELLED
                return True
        return False

    def get_task(self, task_id: str) -> Optional[ScheduledTask]:
        with self._lock:
            return self._tasks.get(task_id)

    def get_tasks(self, status: Optional[TaskStatus] = None) -> List[ScheduledTask]:
        with self._lock:
            if status:
                return [t for t in self._tasks.values() if t.status == status]
            return list(self._tasks.values())

    def get_due_tasks(self) -> List[ScheduledTask]:
        now = datetime.now()
        due = []
        with self._lock:
            for task in self._tasks.values():
                if task.status != TaskStatus.PENDING:
                    continue
                if task.next_run and task.next_run <= now:
                    due.append(task)
        return due

    def start(self):
        """Start the scheduler worker thread."""
        if self._running:
            return
        self._running = True
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()
        self.logger.info("Scheduler started")

    def stop(self):
        """Stop the scheduler."""
        self._running = False
        if self._worker_thread:
            self._worker_thread.join(timeout=5.0)
        self.logger.info("Scheduler stopped")

    def _worker_loop(self):
        """Main scheduler loop."""
        while self._running:
            due_tasks = self.get_due_tasks()
            for task in due_tasks:
                self._execute_task(task)
            time.sleep(1)

    def _execute_task(self, task: ScheduledTask):
        self.logger.debug(f"Executing task: {task.name} [ID: {task.id}]")
        with self._lock:
            task.status = TaskStatus.RUNNING
            task.last_run = datetime.now()
        try:
            task.callback(*task.args, **task.kwargs)
            with self._lock:
                task.status = TaskStatus.COMPLETED
                if task.recurring:
                    if task.schedule_type == ScheduleType.DAILY:
                        task.next_run = task.last_run + timedelta(days=1)
                    elif task.schedule_type == ScheduleType.INTERVAL:
                        task.next_run = task.last_run + timedelta(seconds=task.interval_seconds)
                    task.status = TaskStatus.PENDING
        except Exception as e:
            with self._lock:
                task.status = TaskStatus.FAILED
            self.logger.error(f"Task failed: {task.name} - {e}")

    def remind(self, message: str, delay_seconds: int, callback: Optional[Callable] = None) -> str:
        """Set a reminder."""
        if callback is None:
            callback = lambda msg: self.logger.info(f"REMINDER: {msg}")
        return self.schedule_once(f"Reminder: {message[:30]}", callback, delay_seconds, message)

    def remind_daily(self, message: str, hour: int, minute: int, callback: Optional[Callable] = None) -> str:
        """Set a daily reminder."""
        if callback is None:
            callback = lambda msg: self.logger.info(f"DAILY REMINDER: {msg}")
        return self.schedule_daily(f"Daily: {message[:30]}", callback, hour, minute, message)

    def status(self) -> dict:
        with self._lock:
            pending = sum(1 for t in self._tasks.values() if t.status == TaskStatus.PENDING)
            completed = sum(1 for t in self._tasks.values() if t.status == TaskStatus.COMPLETED)
            failed = sum(1 for t in self._tasks.values() if t.status == TaskStatus.FAILED)
        return {
            "running": self._running, "total": len(self._tasks),
            "pending": pending, "completed": completed,
            "failed": failed, "recurring": sum(1 for t in self._tasks.values() if t.recurring),
        }

    def clear_completed(self):
        with self._lock:
            self._tasks = {
                tid: task for tid, task in self._tasks.items()
                if task.status not in (TaskStatus.COMPLETED, TaskStatus.CANCELLED)
            }
