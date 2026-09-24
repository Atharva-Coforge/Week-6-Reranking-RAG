"""Chat completion call. The only module that talks to Ollama."""

import re

import httpx

_THINK = re.compile(r"<think>.*?</think>", re.DOTALL)


class OllamaLLM:
    """One chat call to local `qwen3:8b`. Thinking is on."""

    def __init__(self, url: str, model: str) -> None:
        self._url = url.rstrip("/")
        self._model = model

    def complete(self, system: str, user: str) -> str:
        """Return the answer text with the thinking trace already removed."""
        response = httpx.post(
            f"{self._url}/api/chat",
            json={
                "model": self._model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "stream": False,
                "think": True,
            },
            timeout=120.0,
        )
        response.raise_for_status()
        message = response.json().get("message", {})
        return _strip_thinking(str(message.get("content", "")))


def _strip_thinking(text: str) -> str:
    """Drop `<think>...</think>` if Ollama left it in the content field."""
    return _THINK.sub("", text).strip()
