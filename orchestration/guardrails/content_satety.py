from dataclasses import dataclass
from azure.identity import DefaultAzureCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from config import AiServicesConfig


class ContentSatefy:

    def __init__(self):
        self.client = self._get_client()

    def _get_client(self):
        return ContentSafetyClient(
            endpoint=AiServicesConfig.CONTENT_SAFETY_ENDPOINT,
            credential=DefaultAzureCredential(),
        )

    async def is_safe(self, message: str) -> dict:
        messages = []
        max_size = 10000
        if len(message) > max_size:
            n_chunk = len(message) // max_size
            for chunk in range(0, n_chunk):
                messages.append(message[chunk * max_size : (chunk + 1) * max_size])
            messages.append(
                message[
                    n_chunk * max_size : n_chunk * max_size + len(message) % max_size
                ]
            )

        responses = []
        for chunk in messages:
            request = AnalyzeTextOptions(chunk)
            response = self.client.analyze_text(request)
            responses.append(
                {
                    "hate": response.hate_results,
                    "self_harm": response.self_harm_results,
                    "sexual": response.sexual_results,
                    "violence": response.violence_results,
                }
            )

        return {
            "safe": False,
            "blocked_categories": []
        }
