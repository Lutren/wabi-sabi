class DeepSeeStub:
    """Stub adapter for Deep See 4 models."""

    def __init__(self, model_id: str = "deep_see4"):
        self.model_id = model_id

    def generate(self, prompt: str) -> str:
        return f"[STUB][{self.model_id}] simulated response for: {prompt[:80]}"


if __name__ == "__main__":
    stub = DeepSeeStub()
    print(stub.generate("Deep See test"))
    import time

    while True:
        time.sleep(3600)
