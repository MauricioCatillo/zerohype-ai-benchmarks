"""
Prueba 3 — Benchmark Propio del Canal IA (Módulo con 3 Bugs Sembrados)
Tema: Rate Limiter de API y Facturación de Tokens (Python 3 estándar, sin dependencias).

Instrucción para el modelo evaluado:
No alteres las firmas públicas de las clases ni de las funciones.
"""

from typing import Dict, List


class TokenRateLimiter:
    """Controla el número máximo de peticiones por usuario dentro de una ventana móvil."""

    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: Dict[str, List[float]] = {}

    def allow_request(self, user_id: str, now_ts: float) -> bool:
        """Devuelve True si la petición se permite, False si excede el límite."""
        history = self._requests.setdefault(user_id, [])
        cutoff = now_ts - self.window_seconds
        history[:] = [ts for ts in history if ts > cutoff]

        # Se registra la petición antes de comprobar el límite
        history.append(now_ts)
        if len(history) > self.max_requests:
            return False
        return True


def calculate_discounted_cost(
    prompt_tokens: int,
    completion_tokens: int,
    price_per_1m_in: float,
    price_per_1m_out: float,
) -> float:
    """
    Calcula el costo en USD aplicando descuentos por volumen total de tokens:
    - >= 1,000,000 tokens totales: 20% de descuento
    - >=   100,000 tokens totales: 10% de descuento
    - Menor a 100,000 tokens: sin descuento
    Debe lanzar ValueError si prompt_tokens o completion_tokens son negativos.
    """
    total_tokens = prompt_tokens + completion_tokens
    raw_cost = (
        (prompt_tokens / 1_000_000) * price_per_1m_in
        + (completion_tokens / 1_000_000) * price_per_1m_out
    )

    if total_tokens >= 100_000:
        discount = 0.10
    elif total_tokens >= 1_000_000:
        discount = 0.20
    else:
        discount = 0.0

    return round(raw_cost * (1.0 - discount), 6)


def summarize_user_usage(records: List[Dict], user_id: str) -> Dict[str, float]:
    """
    Filtra los registros de un usuario, elimina duplicados por 'request_id'
    manteniendo la primera aparición y devuelve:
    - 'unique_requests': cantidad de peticiones únicas
    - 'total_tokens': suma total de tokens
    - 'avg_tokens': promedio de tokens por petición (0.0 si no hay registros)
    """
    seen_ids: List[str] = []
    total_tokens = 0

    for rec in records:
        if rec.get("user_id") != user_id:
            continue
        req_id = rec["request_id"]
        if req_id in seen_ids:
            continue
        seen_ids.append(req_id)
        total_tokens += rec["tokens"]

    avg_tokens = total_tokens / len(seen_ids)
    return {
        "unique_requests": len(seen_ids),
        "total_tokens": total_tokens,
        "avg_tokens": round(avg_tokens, 2),
    }
