# tools/ai_clients.py

class GeminiClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def query(self, prompt: str):
        # Placeholder for Gemini API call
        return f"Simulated Gemini response for prompt: {prompt}"


class CrewAIWrapper:
    def __init__(self, api_key):
        self.api_key = api_key

    def run_task(self, task_name, inputs):
        # Placeholder for CrewAI task execution
        return f"Simulated CrewAI task {task_name} with inputs {inputs}"
