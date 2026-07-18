from datetime import datetime


class Debug:

    ENABLED = True

    @staticmethod
    def log(module, message):

        if not Debug.ENABLED:
            return

        now = datetime.now().strftime("%H:%M:%S")

        print(
            f"[{now}] [{module}] {message}"
        )