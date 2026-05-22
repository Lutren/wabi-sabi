class QwenAdapter:
    """Placeholder adapter for Qwen API integration."""

    def __init__(self, model_id: str = "qwen_3_6_plus"):
        self.model_id = model_id

    def generate(self, prompt: str, **kwargs: object) -> str:
        raise NotImplementedError("Implement Qwen API calls behind ActionGate")
