from __future__ import annotations

import json
import os
import urllib.request
from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    model: str


class ProviderError(RuntimeError):
    pass


class BaseProvider:
    config: ProviderConfig

    def complete(self, *, agent_name: str, system: str, user: str) -> str:
        raise NotImplementedError


class OpenAICompatibleProvider(BaseProvider):
    """Minimal OpenAI-compatible chat completion provider.

    Configure with:
    - AGENTPROOF_API_KEY
    - AGENTPROOF_API_BASE, for example https://api.openai.com/v1
    - AGENTPROOF_MODEL
    """

    def __init__(self) -> None:
        api_key = os.getenv("AGENTPROOF_API_KEY")
        api_base = os.getenv("AGENTPROOF_API_BASE", "https://api.openai.com/v1").rstrip("/")
        model = os.getenv("AGENTPROOF_MODEL", "gpt-4.1-mini")
        if not api_key:
            raise ProviderError("AGENTPROOF_API_KEY is not set.")
        self.api_key = api_key
        self.api_base = api_base
        self.config = ProviderConfig(name="openai-compatible", model=model)

    def complete(self, *, agent_name: str, system: str, user: str) -> str:
        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": f"{system}\n\nYou are the {agent_name} agent."},
                {"role": "user", "content": user},
            ],
            "temperature": 0.2,
        }
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.api_base}/chat/completions",
            data=data,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
        try:
            return body["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError(f"Unexpected provider response: {body}") from exc


class LocalProvider(BaseProvider):
    """Deterministic fallback used for demos without an API key."""

    def __init__(self) -> None:
        self.config = ProviderConfig(name="local-deterministic", model="rules-v1")

    def complete(self, *, agent_name: str, system: str, user: str) -> str:
        return (
            f"[{agent_name}] Local deterministic pass completed.\n"
            f"System intent: {system[:160].strip()}\n"
            f"Input digest preview: {user[:320].strip()}"
        )


def build_provider(prefer_remote: bool) -> BaseProvider:
    if prefer_remote:
        try:
            return OpenAICompatibleProvider()
        except ProviderError:
            pass
    return LocalProvider()

