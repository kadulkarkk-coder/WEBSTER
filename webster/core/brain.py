"""
HELVAC — Hyper-Enhanced Learning, Vision & Autonomous Core
===========================================================
The intelligence engine that coordinates specialized AI modules,
routes tasks, and manages multi-step reasoning.
"""

import time
import threading
from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum

from webster.core.logger import Logger
from webster.core.errors import WebsterError


class TaskType(Enum):
    """Types of tasks HELVAC can handle."""
    CHAT = "chat"
    QUESTION = "question"
    STUDY = "study"
    AUTOMATION = "automation"
    MEMORY = "memory"
    VOICE = "voice"
    RESEARCH = "research"
    CODE = "code"
    WRITING = "writing"
    CREATIVE = "creative"
    PLANNING = "planning"
    SYSTEM = "system"
    BROWSER = "browser"
    FILE = "file"
    UNKNOWN = "unknown"


@dataclass
class Task:
    """A unit of work for HELVAC to process."""
    id: str
    type: TaskType
    input: str
    context: dict = field(default_factory=dict)
    priority: int = 5
    timestamp: float = field(default_factory=time.time)
    callback: Optional[Callable] = None


@dataclass
class TaskResult:
    """Result of a processed task."""
    task_id: str
    success: bool
    output: Any = None
    error: Optional[str] = None
    duration: float = 0.0


class HelvacEngine:
    """
    HELVAC — Central intelligence coordination engine.
    
    Responsibilities:
    - Task analysis and routing
    - Multi-step reasoning
    - Module coordination
    - Context management
    - Performance optimization
    """

    def __init__(self):
        self.logger = Logger().get_logger("HELVAC")
        self._modules: Dict[str, Any] = {}
        self._task_queue: List[Task] = []
        self._results: Dict[str, TaskResult] = {}
        self._running = False
        self._lock = threading.Lock()
        self._worker_thread: Optional[threading.Thread] = None
        self._context_stack: List[dict] = []
        self.logger.info("HELVAC engine initialized")

    # ── Module Management ──────────────────────────────

    def register_module(self, name: str, module: Any):
        """Register a specialized module with HELVAC."""
        with self._lock:
            self._modules[name] = module
            self.logger.debug(f"Module registered: {name}")

    def unregister_module(self, name: str):
        """Remove a module from HELVAC."""
        with self._lock:
            if name in self._modules:
                del self._modules[name]
                self.logger.debug(f"Module unregistered: {name}")

    def get_module(self, name: str) -> Optional[Any]:
        """Get a registered module by name."""
        return self._modules.get(name)

    def list_modules(self) -> List[str]:
        """List all registered modules."""
        return list(self._modules.keys())

    # ── Task Processing ────────────────────────────────

    def analyze_task(self, task: Task) -> TaskType:
        """Analyze input and determine the task type."""
        text = task.input.lower()
        
        # Study related
        study_keywords = ["study", "learn", "flashcard", "quiz", "note", "pdf", "exam", "subject"]
        if any(kw in text for kw in study_keywords):
            return TaskType.STUDY

        # Automation related
        auto_keywords = ["open", "launch", "close", "file", "app", "browser", "search", "find"]
        if any(kw in text for kw in auto_keywords):
            return TaskType.AUTOMATION

        # Code related
        code_keywords = ["code", "program", "function", "debug", "python", "javascript"]
        if any(kw in text for kw in code_keywords):
            return TaskType.CODE

        # Writing
        write_keywords = ["write", "essay", "email", "letter", "article", "blog"]
        if any(kw in text for kw in write_keywords):
            return TaskType.WRITING

        # Research
        research_keywords = ["research", "search", "find out", "look up", "what is", "who is"]
        if any(kw in text for kw in research_keywords):
            return TaskType.RESEARCH

        # Planning
        plan_keywords = ["plan", "schedule", "organize", "arrange", "remind"]
        if any(kw in text for kw in plan_keywords):
            return TaskType.PLANNING

        # Default to chat
        return TaskType.CHAT

    def submit_task(self, task: Task) -> str:
        """Submit a task to HELVAC for processing."""
        if task.type == TaskType.UNKNOWN:
            task.type = self.analyze_task(task)

        with self._lock:
            self._task_queue.append(task)
            self.logger.debug(f"Task queued: {task.id} ({task.type.value})")
        
        if not self._running:
            self._start_worker()
        
        return task.id

    def get_result(self, task_id: str) -> Optional[TaskResult]:
        """Get the result of a completed task."""
        return self._results.get(task_id)

    def wait_for_result(self, task_id: str, timeout: float = 30.0) -> Optional[TaskResult]:
        """Wait for a task result with timeout."""
        start = time.time()
        while time.time() - start < timeout:
            result = self.get_result(task_id)
            if result:
                return result
            time.sleep(0.1)
        return None

    # ── Worker Thread ──────────────────────────────────

    def _start_worker(self):
        """Start the background task processing worker."""
        self._running = True
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()
        self.logger.info("HELVAC worker started")

    def _worker_loop(self):
        """Main processing loop."""
        while self._running:
            task = None
            with self._lock:
                if self._task_queue:
                    # Sort by priority and take highest
                    self._task_queue.sort(key=lambda t: t.priority, reverse=True)
                    task = self._task_queue.pop(0)

            if task:
                self._process_task(task)
            else:
                time.sleep(0.1)

    def _process_task(self, task: Task):
        """Process a single task."""
        start = time.time()
        self.logger.debug(f"Processing task: {task.id} ({task.type.value})")
        
        try:
            output = self._route_task(task)
            duration = time.time() - start
            result = TaskResult(
                task_id=task.id,
                success=True,
                output=output,
                duration=duration
            )
        except Exception as e:
            duration = time.time() - start
            result = TaskResult(
                task_id=task.id,
                success=False,
                error=str(e),
                duration=duration
            )
            self.logger.error(f"Task failed: {task.id} - {e}")

        with self._lock:
            self._results[task.id] = result

        if task.callback:
            try:
                task.callback(result)
            except Exception as e:
                self.logger.error(f"Task callback failed: {e}")

    def _route_task(self, task: Task) -> Any:
        """Route a task to the appropriate module."""
        module_map = {
            TaskType.CHAT: "ai",
            TaskType.QUESTION: "ai",
            TaskType.STUDY: "study",
            TaskType.AUTOMATION: "automation",
            TaskType.MEMORY: "memory",
            TaskType.VOICE: "voice",
            TaskType.CODE: "ai",
            TaskType.WRITING: "ai",
            TaskType.RESEARCH: "ai",
            TaskType.PLANNING: "ai",
            TaskType.BROWSER: "automation",
            TaskType.FILE: "automation",
        }

        module_name = module_map.get(task.type, "ai")
        module = self._modules.get(module_name)

        if module is None:
            # Fallback to AI module
            module = self._modules.get("ai")

        if module and hasattr(module, "process"):
            return module.process(task)
        elif module and hasattr(module, "ask"):
            return module.ask(task.input)
        else:
            return f"I'm not sure how to handle that yet. (No module for {task.type.value})"

    # ── Reasoning ──────────────────────────────────────

    def reason(self, query: str, context: dict = None) -> str:
        """Perform multi-step reasoning."""
        steps = []
        context = context or {}
        
        steps.append(f"Analyzing: {query}")
        
        # Step 1: Understand
        task_type = self.analyze_task(Task(id="temp", type=TaskType.UNKNOWN, input=query))
        steps.append(f"Task type identified: {task_type.value}")
        
        # Step 2: Context gathering
        if context:
            steps.append(f"Context available: {list(context.keys())}")
        
        # Step 3: Routing
        steps.append(f"Routing to: {task_type.value} module")
        
        return "\n".join(steps)

    # ── Context ────────────────────────────────────────

    def push_context(self, context: dict):
        """Push context onto the stack."""
        with self._lock:
            self._context_stack.append(context)

    def pop_context(self) -> Optional[dict]:
        """Pop context from the stack."""
        with self._lock:
            if self._context_stack:
                return self._context_stack.pop()
        return None

    def current_context(self) -> dict:
        """Get the current context."""
        with self._lock:
            if self._context_stack:
                return self._context_stack[-1].copy()
        return {}

    # ── Lifecycle ──────────────────────────────────────

    def start(self):
        """Start the HELVAC engine."""
        if not self._running:
            self._start_worker()
            self.logger.info("HELVAC engine started")

    def stop(self):
        """Stop the HELVAC engine."""
        self._running = False
        if self._worker_thread:
            self._worker_thread.join(timeout=5.0)
        self.logger.info("HELVAC engine stopped")

    def status(self) -> dict:
        """Get HELVAC status information."""
        return {
            "running": self._running,
            "modules": len(self._modules),
            "queue_size": len(self._task_queue),
            "results_cached": len(self._results),
            "context_depth": len(self._context_stack),
        }
