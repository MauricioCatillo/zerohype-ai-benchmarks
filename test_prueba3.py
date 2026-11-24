"""
Suite de 4 Tests Unitarios — Prueba 3 (Benchmark del Canal IA)
Ejecutar en terminal:
    python3 -m unittest test_prueba3.py -v
"""

import time
import unittest

from prueba3_buggy_module import (
    TokenRateLimiter,
    calculate_discounted_cost,
    summarize_user_usage,
)


class TestPrueba3Benchmark(unittest.TestCase):
    def test_1_rate_limiter_does_not_count_rejected_requests(self) -> None:
        """Las peticiones rechazadas NO deben contar contra el límite ni extender el bloqueo."""
        limiter = TokenRateLimiter(max_requests=2, window_seconds=10)
        self.assertTrue(limiter.allow_request("u1", 100.0))
        self.assertTrue(limiter.allow_request("u1", 101.0))
        # Estas 2 peticiones son rechazadas en t=105 y t=109
        self.assertFalse(limiter.allow_request("u1", 105.0))
        self.assertFalse(limiter.allow_request("u1", 109.0))
        # En t=111 ya expiraron t=100 y t=101: el usuario debe volver a tener cupo
        self.assertTrue(
            limiter.allow_request("u1", 111.0),
            "Las peticiones rechazadas bloquearon indebidamente al usuario.",
        )

    def test_2_volume_discount_tiers_and_validation(self) -> None:
        """El descuento de 20% (>= 1M tokens) debe aplicarse y tokens negativos deben lanzar ValueError."""
        # 1,000,000 input a $2.00 + 500,000 output a $6.00 = $5.00 bruto -> 20% desc = $4.00
        cost_enterprise = calculate_discounted_cost(1_000_000, 500_000, 2.0, 6.0)
        self.assertAlmostEqual(cost_enterprise, 4.0, places=5)

        # 100,000 input a $10.00 = $1.00 bruto -> 10% desc = $0.90
        cost_mid = calculate_discounted_cost(100_000, 0, 10.0, 10.0)
        self.assertAlmostEqual(cost_mid, 0.9, places=5)

        with self.assertRaises(ValueError):
            calculate_discounted_cost(-10, 500, 2.0, 6.0)

    def test_3_summarize_empty_user_returns_zero_average(self) -> None:
        """Un usuario sin registros no debe lanzar ZeroDivisionError."""
        records = [{"user_id": "otro", "request_id": "r1", "tokens": 500}]
        result = summarize_user_usage(records, user_id="inexistente")
        self.assertEqual(
            result,
            {"unique_requests": 0, "total_tokens": 0, "avg_tokens": 0.0},
        )

    def test_4_deduplication_performance_linear_time(self) -> None:
        """La deduplicación debe escalar en O(n), procesando 15,000 registros en menos de 0.15s."""
        records = [
            {"user_id": "u_heavy", "request_id": f"req_{i % 12000}", "tokens": 100}
            for i in range(15_000)
        ]
        start = time.perf_counter()
        result = summarize_user_usage(records, user_id="u_heavy")
        elapsed = time.perf_counter() - start

        self.assertEqual(result["unique_requests"], 12_000)
        self.assertEqual(result["total_tokens"], 1_200_000)
        self.assertEqual(result["avg_tokens"], 100.0)
        self.assertLess(
            elapsed,
            0.15,
            f"Rendimiento degradado (posible O(n^2)): tardó {elapsed:.3f}s (límite 0.15s).",
        )


if __name__ == "__main__":
    unittest.main()
