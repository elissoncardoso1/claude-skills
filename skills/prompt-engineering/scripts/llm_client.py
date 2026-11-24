"""Cliente mínimo e plugável para chamar LLMs (Anthropic, OpenAI, Gemini ou mock).

Usado por eval_harness.py e pairwise_judge.py. Só importa o SDK do provedor escolhido.
Chaves de API vêm das variáveis de ambiente padrão de cada SDK
(ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY/GOOGLE_API_KEY).

Uso:
    from llm_client import complete
    texto = complete(provider="anthropic", model="claude-...", system="...", user="...")
"""
from __future__ import annotations

import os
import time
from typing import Callable, Optional


class LLMError(RuntimeError):
    pass


def _anthropic(model: str, system: Optional[str], user: str, temperature: Optional[float], max_tokens: int) -> str:
    import anthropic  # type: ignore

    client = anthropic.Anthropic()
    kwargs = dict(model=model, max_tokens=max_tokens, messages=[{"role": "user", "content": user}])
    if system:
        kwargs["system"] = system
    if temperature is not None:
        kwargs["temperature"] = temperature
    msg = client.messages.create(**kwargs)
    # Seleciona blocos por tipo, não por posição (thinking pode vir antes).
    return "".join(getattr(b, "text", "") for b in msg.content if getattr(b, "type", "") == "text")


def _openai(model: str, system: Optional[str], user: str, temperature: Optional[float], max_tokens: int) -> str:
    from openai import OpenAI  # type: ignore

    client = OpenAI()
    kwargs = dict(model=model, input=[{"role": "user", "content": user}], max_output_tokens=max_tokens)
    if system:
        kwargs["instructions"] = system
    if temperature is not None:
        kwargs["temperature"] = temperature  # alguns modelos de raciocínio não aceitam
    r = client.responses.create(**kwargs)
    return r.output_text


def _gemini(model: str, system: Optional[str], user: str, temperature: Optional[float], max_tokens: int) -> str:
    from google import genai  # type: ignore

    client = genai.Client()
    config: dict = {"max_output_tokens": max_tokens}
    if system:
        config["system_instruction"] = system
    if temperature is not None:
        config["temperature"] = temperature
    r = client.models.generate_content(model=model, contents=user, config=config)
    return r.text or ""


def _mock(model: str, system: Optional[str], user: str, temperature: Optional[float], max_tokens: int) -> str:
    """Provedor de teste offline. Se o prompt contiver uma linha 'MOCK_OUTPUT: ...', devolve o resto dela;
    caso contrário devolve o próprio prompt do usuário (eco)."""
    for line in user.splitlines():
        if line.startswith("MOCK_OUTPUT:"):
            return line[len("MOCK_OUTPUT:"):].strip()
    return user


PROVIDERS: dict[str, Callable[..., str]] = {
    "anthropic": _anthropic,
    "openai": _openai,
    "gemini": _gemini,
    "mock": _mock,
}


def complete(
    provider: str,
    model: str,
    user: str,
    system: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: int = 4096,
    retries: int = 3,
) -> str:
    if provider not in PROVIDERS:
        raise LLMError(f"Provedor desconhecido: {provider}. Use um de {sorted(PROVIDERS)}")
    fn = PROVIDERS[provider]
    last: Exception | None = None
    for attempt in range(retries):
        try:
            return fn(model, system, user, temperature, max_tokens)
        except ImportError as e:
            raise LLMError(f"SDK do provedor '{provider}' não instalado: {e}") from e
        except Exception as e:  # erros transitórios: tenta de novo com backoff
            last = e
            time.sleep(min(2 ** attempt, 10))
    raise LLMError(f"Falha após {retries} tentativas: {last}")


if __name__ == "__main__":
    import sys

    prov = os.environ.get("LLM_PROVIDER", "mock")
    print(complete(prov, os.environ.get("LLM_MODEL", "mock"), " ".join(sys.argv[1:]) or "MOCK_OUTPUT: ok"))
