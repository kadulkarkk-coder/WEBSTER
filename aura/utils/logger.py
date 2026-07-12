from datetime import datetime


class Logger:

    def info(self, message):

        current = datetime.now().strftime("%H:%M:%S")

        print(f"[INFO {current}] {message}")

    def warning(self, message):

        current = datetime.now().strftime("%H:%M:%S")

        print(f"[WARNING {current}] {message}")

    def error(self, message):

        current = datetime.now().strftime("%H:%M:%S")

        print(f"[ERROR {current}] {message}")