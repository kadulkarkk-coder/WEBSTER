"""
WEBSTER Workflow Engine
===========================
Create and run automated workflows with steps.
"""

from typing import Any, Callable, Dict, List, Optional
import json
import threading
from datetime import datetime
from webster.core.logger import Logger


class WorkflowEngine:
    """Create, save, and execute multi-step workflows."""

    def __init__(self):
        self.logger = Logger().get_logger("WORKFLOW")
        self._workflows: Dict[str, Dict] = {}
        self._running = False

    def create(self, name: str, steps: List[Dict]) -> str:
        workflow_id = f"wf_{len(self._workflows)}_{datetime.now().timestamp():.0f}"
        self._workflows[workflow_id] = {
            "id": workflow_id,
            "name": name,
            "steps": steps,
            "created": datetime.now().isoformat(),
        }
        self.logger.info(f"Workflow created: {name} [{workflow_id}]")
        return workflow_id

    def add_step(self, workflow_id: str, step: Dict) -> bool:
        if workflow_id not in self._workflows:
            return False
        self._workflows[workflow_id]["steps"].append(step)
        return True

    def execute(self, workflow_id: str, **kwargs) -> List[Dict]:
        if workflow_id not in self._workflows:
            return [{"error": "Workflow not found"}]
        workflow = self._workflows[workflow_id]
        self._running = True
        results = []
        for i, step in enumerate(workflow["steps"]):
            if not self._running:
                break
            result = self._execute_step(step, i, **kwargs)
            results.append(result)
        self._running = False
        return results

    def execute_async(self, workflow_id: str, callback: Callable = None, **kwargs):
        thread = threading.Thread(
            target=lambda: callback(self.execute(workflow_id, **kwargs)) if callback else None,
            daemon=True
        )
        thread.start()

    def _execute_step(self, step: Dict, index: int, **kwargs) -> Dict:
        step_type = step.get("type", "")
        params = step.get("params", {})
        try:
            if step_type == "delay":
                import time
                time.sleep(params.get("seconds", 1))
                return {"step": index, "type": step_type, "success": True}
            elif step_type == "message":
                msg = params.get("message", "").format(**kwargs)
                return {"step": index, "type": step_type, "message": msg, "success": True}
            elif step_type == "command":
                from webster.automation.commands import CommandExecutor
                executor = CommandExecutor()
                result = executor.run(params.get("command", ""))
                return {"step": index, "type": step_type, **result}
            elif step_type == "launch":
                from webster.automation.apps import AppLauncher
                launcher = AppLauncher()
                success = launcher.launch(params.get("app", ""), params.get("args", ""))
                return {"step": index, "type": step_type, "success": success}
            elif step_type == "browser":
                from webster.automation.browser import BrowserController
                browser = BrowserController()
                browser.open(params.get("url", ""))
                return {"step": index, "type": step_type, "success": True}
            else:
                return {"step": index, "type": step_type, "success": False, "error": f"Unknown type: {step_type}"}
        except Exception as e:
            return {"step": index, "type": step_type, "success": False, "error": str(e)}

    def list_workflows(self) -> List[Dict]:
        return list(self._workflows.values())

    def get_workflow(self, workflow_id: str) -> Optional[Dict]:
        return self._workflows.get(workflow_id)

    def delete_workflow(self, workflow_id: str) -> bool:
        if workflow_id in self._workflows:
            del self._workflows[workflow_id]
            return True
        return False

    def stop(self):
        self._running = False
