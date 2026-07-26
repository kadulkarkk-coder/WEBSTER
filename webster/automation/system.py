"""
WEBSTER System Controller
===========================
System operations: processes, system info, shutdown/restart, volume.
"""

import os
import platform
import subprocess
from typing import Dict, List, Optional
from webster.core.logger import Logger


class SystemController:
    """Control system operations."""

    def __init__(self):
        self.logger = Logger().get_logger("SYS_CTRL")

    def info(self) -> Dict:
        """Get comprehensive system information."""
        import psutil
        import datetime
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "hostname": platform.node(),
            "cpu": {
                "physical_cores": psutil.cpu_count(logical=False),
                "total_cores": psutil.cpu_count(logical=True),
                "max_frequency": psutil.cpu_freq().max if psutil.cpu_freq() else None,
                "usage_percent": psutil.cpu_percent(interval=0.1),
            },
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent": psutil.virtual_memory().percent,
            },
            "disk": {
                "total": psutil.disk_usage("/").total,
                "free": psutil.disk_usage("/").free,
                "percent": psutil.disk_usage("/").percent,
            },
            "boot_time": boot_time.isoformat(),
            "uptime_hours": round((datetime.datetime.now() - boot_time).total_seconds() / 3600, 1),
        }

    def processes(self) -> List[Dict]:
        import psutil
        procs = []
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                procs.append(proc.info)
            except:
                pass
        return sorted(procs, key=lambda p: p.get("memory_percent", 0), reverse=True)[:50]

    def kill_process(self, pid: int) -> bool:
        import psutil
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            return True
        except Exception as e:
            self.logger.error(f"Kill process error: {e}")
            return False

    def shutdown(self, delay_sec: int = 0) -> bool:
        self.logger.warning(f"System shutdown in {delay_sec}s")
        if platform.system() == "Windows":
            subprocess.run(["shutdown", "/s", "/t", str(delay_sec)], shell=True)
        else:
            subprocess.run(["shutdown", "-h", f"+{delay_sec // 60}"])
        return True

    def restart(self, delay_sec: int = 0) -> bool:
        self.logger.warning(f"System restart in {delay_sec}s")
        if platform.system() == "Windows":
            subprocess.run(["shutdown", "/r", "/t", str(delay_sec)], shell=True)
        else:
            subprocess.run(["shutdown", "-r", f"+{delay_sec // 60}"])
        return True

    def sleep(self) -> bool:
        if platform.system() == "Windows":
            subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
        return True

    def set_volume(self, level: int):
        """Set system volume (0-100)."""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level / 100.0, None)
        except ImportError:
            self.logger.warning("pycaw not available for volume control")

    def battery(self) -> Optional[Dict]:
        import psutil
        if hasattr(psutil, "sensors_battery"):
            batt = psutil.sensors_battery()
            if batt:
                return {
                    "percent": batt.percent,
                    "power_plugged": batt.power_plugged,
                    "time_left_sec": batt.secsleft if batt.secsleft != -1 else None,
                }
        return None

    def screen_brightness(self, level: int = None) -> Optional[int]:
        """Get or set screen brightness (0-100)."""
        try:
            import screen_brightness_control as sbc
            if level is not None:
                sbc.set_brightness(level)
            return sbc.get_brightness()
        except ImportError:
            self.logger.warning("screen_brightness_control not available")
            return None
