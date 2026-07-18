import threading
import queue
import traceback

class AIWorker:
    """
    Executes AI tasks on a background thread and
    streams response chunks back to the UI.
    """

    # Sentinel object indicating the stream has finished
    END = object()

    def __init__(self):

        self.thread = None

        self.queue = queue.Queue()

        self.running = False

    # ==================================================
    # Start Streaming
    # ==================================================

    def start_stream(
        self,
        target,
        *args,
        **kwargs
    ):

        # Prevent multiple workers from running
        if self.running:

            return

        self.running = True

        # Clear any leftover chunks
        while not self.queue.empty():

            try:
                self.queue.get_nowait()

            except queue.Empty:
                break

        self.thread = threading.Thread(

            target=self._run,

            args=(target, args, kwargs),

            daemon=True

        )

        self.thread.start()

    # ==================================================
    # Worker Thread
    # ==================================================

    def _run(
        self,
        target,
        args,
        kwargs
    ):

        try:

            for chunk in target(
                *args,
                **kwargs
            ):

                self.queue.put(
                    chunk
                )

        except Exception as error:
            traceback.print_exc()
            self.queue.put(
                error
            )

        finally:

            self.running = False

            self.queue.put(
                AIWorker.END
            )

    # ==================================================
    # Read Next Chunk
    # ==================================================

    def get_chunk(self):

        try:

            return self.queue.get_nowait()

        except queue.Empty:

            return None

    # ==================================================
    # Status
    # ==================================================

    def is_running(self):

        return self.running

    # ==================================================
    # Wait For Completion
    # ==================================================

    def join(self):

        if self.thread is not None:

            self.thread.join()

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):

        self.running = False

        while not self.queue.empty():

            try:

                self.queue.get_nowait()

            except queue.Empty:

                break