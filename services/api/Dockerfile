# ============================================================
# 1. IMAGEN DE EJECUCIÓN: MISMA RAMA QUE PYTHON LOCAL
# ============================================================
FROM python:3.14-slim

# ============================================================
# 2. CONFIGURACIÓN DEL CONTENEDOR
# ============================================================
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

# ============================================================
# 3. INSTALACIÓN DE LAS DEPENDENCIAS
# ============================================================
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

# ============================================================
# 4. CÓDIGO DEL BACKEND Y USUARIO NO PRIVILEGIADO
# ============================================================
COPY app/ /app/app/
RUN useradd --create-home --uid 10001 sismo && chown -R sismo:sismo /app
USER sismo

# ============================================================
# 5. SERVIDOR HTTP PARA RENDER Y PRUEBAS LOCALES
# ============================================================
EXPOSE 10000
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
