# Prueba 3 — Caza de 3 Bugs Sutiles y Refactorización (20 puntos)

Benchmark reproducible en Python 3 estándar (sin dependencias externas) para evaluar la capacidad real de depuración de modelos de IA.

## Archivos incluidos
- `prueba3_buggy_module.py`: Código con 3 bugs sembrados (es lo que se entrega al modelo).
- `test_prueba3.py`: Suite de 4 tests unitarios que deben pasar en verde.

## Cómo ejecutarlo en pantalla (para grabación en OBS)
```bash
# 1. Ejecutar antes de la corrección (4/4 en ROJO)
python3 -m unittest test_prueba3.py -v

# 2. Pegar el código corregido por el modelo en prueba3_buggy_module.py y volver a ejecutar (objetivo: 4/4 en VERDE)
python3 -m unittest test_prueba3.py -v
```

## Prompt exacto para enviar al modelo evaluado
> Analiza este módulo en Python (`prueba3_buggy_module.py`). Identifica exactamente los 3 bugs presentes, explica en máximo 2 líneas por qué falla cada uno y devuelve el código completo corregido que pase los 4 tests unitarios sin alterar las firmas públicas de las clases ni funciones.

*(Adjuntar el contenido de `prueba3_buggy_module.py` y `test_prueba3.py`.)*

## Rúbrica de evaluación (20 puntos)
- **6 pts:** Detecta los 3 bugs reales sin inventar falsos positivos (rate limiter registrando rechazos, orden invertido de descuentos + validación de negativos, y deduplicación O(n²) + división por cero).
- **4 pts:** Explicación técnica concisa (máximo 2 líneas por error).
- **6 pts:** El código corregido pasa 4/4 tests al primer intento (`OK` en menos de 0.15s).
- **4 pts:** Conserva exactamente las firmas públicas y mantiene el código limpio.
