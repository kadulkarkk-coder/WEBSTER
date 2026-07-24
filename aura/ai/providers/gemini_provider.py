from google import genai

from config.api_keys import APIKeys

from aura.ai.providers.base_provider import BaseProvider

import traceback

from aura.ai.errors import *

from aura.utils.debug import Debug

import time

import random

class GeminiProvider(BaseProvider):
    """
    ==================================================

                Gemini Provider

    ==================================================

    Google Gemini AI Provider

    Sprint 21.0

        • Provider Architecture

    Sprint 21.1

        • Gemini API
        • Streaming
        • Chat History
    """

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(self):

        self.client = None

        self.model = "gemini-3.5-flash"

        self.initialized = False

        self.connected = False

        self.last_error = None
        
        self.request_count = 0

        self.total_tokens = 0

        self.streaming = False

        self.last_response = ""

        self.max_retries = 3

        self.retry_delay = 1

        self.retry_count = 0

        self.version = "2.0"
    # ==================================================
    # Lifecycle
    # ==================================================

    def initialize(

        self

    ):

        try:

            api_key = str(

                APIKeys["gemini"]

            ).strip()

            if not api_key:

                raise ValueError(

                    "Gemini API key missing."

                )

            self.client = genai.Client(

                api_key=api_key

            )

            self.connected = True

            self.initialized = True

            self.last_error = None

            Debug.log(

                "Gemini",

                f"Connected ({self.model})"

            )

        except Exception as e:

            self.connected = False

            self.initialized = False

            self.last_error = str(e)

            traceback.print_exc()

            Debug.log(

                "Gemini",

                self.last_error

            )

            raise
    # ==================================================
    # AI
    # ==================================================

    def classify_error(

        self,

        error

    ):

        text = str(error).upper()

        if "API_KEY_INVALID" in text:

           raise InvalidAPIKey(text)

        elif "NOT_FOUND" in text:

            raise InvalidModel(text)

        elif "RESOURCE_EXHAUSTED" in text:

            raise QuotaExceeded(text)

        elif "RATE_LIMIT" in text:

           raise RateLimited(text)

        elif "DEADLINE_EXCEEDED" in text:

           raise TimeoutError(text)

        elif "UNAVAILABLE" in text:

           raise NetworkError(text)

        elif "INTERNAL" in text:

           raise ServerError(text)

        raise UnknownProviderError(text)
    
    def should_retry(

        self,

        error

    ):

        text = str(error).upper()

        retry_errors = (

            "RESOURCE_EXHAUSTED",

            "429",

            "503",

            "UNAVAILABLE",

            "INTERNAL",

            "DEADLINE_EXCEEDED",

            "408"

        )

        return any(

            item in text

            for item in retry_errors

        )

    def generate(

        self,

        prompt

    ):

        self.retry_count = 0

        while self.retry_count <= self.max_retries:

            try:

                response = self.client.models.generate_content(

                    model=self.model,

                    contents=prompt

                )

                self.retry_count = 0

                return response.text

            except Exception as e:

                if not self.should_retry(e):

                    raise

                self.retry_count += 1

                if self.retry_count > self.max_retries:

                    raise

                delay = (

                    self.retry_delay

                    * (2 ** (self.retry_count - 1))

                )

                delay += random.uniform(

                    0,

                    0.5

                )

                Debug.log(

                    "Gemini",

                    f"Retry {self.retry_count} in {delay:.2f}s"

                )

                time.sleep(delay)

    # ==================================================
    # Streaming
    # ==================================================

    def stream(

        self,

        prompt

    ):

        self.retry_count = 0

        while self.retry_count <= self.max_retries:

            try:

                response = self.client.models.generate_content(

                    model=self.model,

                    contents=prompt

                )

                self.retry_count = 0

                self.last_error = None
                
                return response.text

            except Exception as e:

                if not self.should_retry(e):

                    raise

                self.retry_count += 1

                if self.retry_count > self.max_retries:

                    raise

                delay = (

                    self.retry_delay

                    * (2 ** (self.retry_count - 1))

                )

                delay += random.uniform(

                    0,

                    0.5

                )

                Debug.log(

                    "Gemini",

                    f"Retry {self.retry_count} in {delay:.2f}s"

                )

                time.sleep(delay)
    # ==================================================
    # Information
    # ==================================================

    def get_name(self):

        return "Gemini"

    # --------------------------------------------------

    def get_status(self):

        if self.initialized:

            return "Online"

        return "Offline"

    # --------------------------------------------------

    def is_streaming(

        self

    ):

        return self.streaming

    def get_version(self):

        return self.version

    def health(

        self

    ):

        return {

            "provider": "Gemini",

            "connected": self.connected,

            "initialized": self.initialized,

            "streaming": self.streaming,

            "model": self.model,

            "requests": self.request_count,

            "tokens": self.total_tokens,

            "last_error": self.last_error,

            "healthy": self.last_error is None,

            "retry_count": self.retry_count,

            
        }

    def shutdown(self):

        self.initialized = False

        print(
            "Gemini Provider Shutdown"
        )

        