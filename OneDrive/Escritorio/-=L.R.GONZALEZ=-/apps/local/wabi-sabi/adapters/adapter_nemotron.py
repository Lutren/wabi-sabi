class NemotronAdapter:
    """Placeholder adapter for real Nemotron/NVIDIA integration."""

    def __init__(self, model_id: str = "nemotron_ultra_253b"):
        self.model_id = model_id

    def generate(self, prompt: str, **kwargs: object) -> str:
        raise NotImplementedError("Implement NVCR/NGC integration behind ActionGate")
