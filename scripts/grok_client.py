"""GrokClient wrapper providing resilient text generation for the AI engine."""
from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Dict, Optional

import requests


DEFAULT_MODEL = "grok-beta"
DEFAULT_API_URL = "https://api.x.ai/v1/chat/completions"


class GrokClientError(RuntimeError):
    """Raised when the Grok backend returns an error response."""


@dataclass
class GrokClient:
    """Lightweight client for Grok text generation with retry support."""

    api_key: Optional[str] = None
    api_url: str = DEFAULT_API_URL
    model: str = DEFAULT_MODEL
    max_retries: int = 3
    backoff_seconds: float = 1.5

    def __post_init__(self) -> None:
        if not self.api_key:
            self.api_key = os.getenv("GROK_API_KEY")
        if not self.api_key:
            raise GrokClientError("GROK_API_KEY is required to initialize GrokClient")

    def generate_text(self, prompt: str, context: Dict) -> str:
        """Send a generation request with exponential backoff on failure."""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": context.get("system_prompt", "")},
                {"role": "user", "content": prompt},
            ],
            "temperature": context.get("temperature", 0.3),
            "max_tokens": context.get("max_tokens", 512),
        }

        attempt = 0
        while attempt <= self.max_retries:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            if response.ok:
                data = response.json()
                choices = data.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "")
                raise GrokClientError("Grok API returned an empty response")

            attempt += 1
            if attempt > self.max_retries:
                break
            sleep_for = self.backoff_seconds * attempt
            time.sleep(sleep_for)

        raise GrokClientError(
            f"Grok API request failed after {self.max_retries} retries: {response.text}"
        )
