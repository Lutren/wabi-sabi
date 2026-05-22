class QwenStub:
    """Stub adapter for Qwen models for local testing."""

    def __init__(self, model_id: str = "qwen_3_6_plus"):
        self.model_id = model_id

    def generate(self, prompt: str) -> str:
        return f"[STUB][{self.model_id}] simulated response for: {prompt[:80]}"


if __name__ == "__main__":
    stub = QwenStub()
    print(stub.generate('print("hello")'))
    import time

    while True:
        time.sleep(3600)
