import time
import random


class LLMClient:
    """
    Simple mock LLM client.
    Replace with real API call if needed.
    """

    def run(self, prompt: str) -> str:
        # simulate latency
        time.sleep(random.uniform(1.0, 3.0))

        return f"LLM RESPONSE:\nProcessed prompt:\n{prompt}"