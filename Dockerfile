# Use a slim Python 3.11 base image for a small final image size
FROM python:3.11-slim
 
# ── Metadata ──────────────────────────────────────────────
LABEL maintainer="eshakhan3870@gmail.com"
LABEL description="CYBER-DEF25: AI Malware Detection Inference Container"
LABEL version="1.0"
 
# ── Set working directory inside the container ────────────
WORKDIR /app
 
# ── Install Python dependencies ───────────────────────────
# Copy requirements first (Docker layer-caching optimisation)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# ── Copy application files ────────────────────────────────
COPY model.pkl     .
COPY inference.py  .
 
# ── Create expected I/O directories ──────────────────────
# inference.py reads from /input/logs and writes to /output
RUN mkdir -p /input/logs /output
 
# ── Default command: run the inference script ─────────────
CMD ["python", "inference.py"]
