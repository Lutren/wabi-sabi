class NemotronStub:
    """Stub adapter for Nemotron-family models for local testing."""

    def __init__(self, model_id: str = "nemotron_ultra_253b"):
        self.model_id = model_id

    def generate(self, prompt: str) -> str:
        return f"[STUB][{self.model_id}] simulated response for: {prompt[:80]}"


if __name__ == "__main__":
    stub = NemotronStub()
    print(stub.generate("Hello world"))
    import time

    while True:
        time.sleep(3600)
