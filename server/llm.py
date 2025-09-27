"""Async OpenAI chat completion wrapper used by DuoForge."""

from __future__ import annotations

import asyncio
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

_API_KEY = os.getenv("OPENAI_API_KEY")
_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
_TIMEOUT = float(os.getenv("OPENAI_TIMEOUT", "60"))
_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1200"))

_client: AsyncOpenAI | None = None
_client_lock = asyncio.Lock()


async def _get_client() -> AsyncOpenAI:
    global _client
    if _client is not None:
        return _client
    if not _API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    async with _client_lock:
        if _client is None:
            _client = AsyncOpenAI(api_key=_API_KEY)
    return _client


async def chat(messages: List[Dict[str, str]]) -> str:
    """Send a chat completion request to the configured OpenAI model."""

    client = await _get_client()
    response = await asyncio.wait_for(
        client.chat.completions.create(
            model=_MODEL,
            messages=messages,
            max_tokens=_MAX_TOKENS,
        ),
        timeout=_TIMEOUT,
    )
    return response.choices[0].message.content or ""
