class DeepSeeAdapter:
    """Placeholder adapter for Deep See 4 API."""

    def __init__(self, model_id: str = "deep_see4"):
        self.model_id = model_id

    def generate(self, prompt: str, **kwargs: object) -> str:
        raise NotImplementedError("Implement DeepSee API calls behind ActionGate")
