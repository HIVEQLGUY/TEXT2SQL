from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from app.core.config import LLMSettings


class LLMClientError(RuntimeError):
    pass


class OpenAICompatibleClient:
    def __init__(self, settings: LLMSettings) -> None:
        self._settings = settings

    def chat(self, messages: list[dict[str, str]], temperature: float = 0.0) -> dict[str, Any]:
        if not self._settings.api_key:
            raise LLMClientError("LLM_API_KEY is not configured.")
        if not self._settings.base_url:
            raise LLMClientError("LLM_BASE_URL is not configured.")

        model = self._normalized_model()
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": False,
        }
        request = urllib.request.Request(
            url=f"{self._settings.base_url.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self._settings.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self._settings.timeout_seconds) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise LLMClientError(f"LLM HTTP error {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise LLMClientError(f"LLM request failed: {exc.reason}") from exc

        data = json.loads(body)
        choices = data.get("choices") or []
        if not choices:
            raise LLMClientError("LLM returned no choices.")

        content = choices[0].get("message", {}).get("content", "")
        if not content:
            raise LLMClientError("LLM returned empty content.")

        return {
            "content": content,
            "model": data.get("model", model),
            "usage": data.get("usage"),
            "raw": data,
        }

    def _normalized_model(self) -> str:
        model = self._settings.model.strip()
        if self._settings.provider.lower() == "deepseek" and model.upper() == "DEEPSEEK":
            return "deepseek-v4-flash"
        return model
