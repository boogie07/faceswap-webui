# Face-swap web UI container for SaladCloud (GPU).
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3.10 python3-pip git unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN git clone -q https://github.com/blues-creations/dot
WORKDIR /app/dot

# CUDA torch first (Kaggle/VM-tested combo: torch 2.x + cu121)
RUN pip install --no-cache-dir torch torchvision \
        --index-url https://download.pytorch.org/whl/cu121
# dot file-based swap deps (repo pinned requirements.txt is Python 3.8-era; skipped)
RUN pip install --no-cache-dir gdown click pyyaml face-alignment mediapipe insightface gradio
RUN pip uninstall -y onnxruntime && pip install --no-cache-dir onnxruntime-gpu
RUN pip install --no-cache-dir -e . --no-deps

# model checkpoints (~4.1 GB, baked into the image)
RUN gdown --id 1Y_11R66DL4N1WY8cNlXVNR3RkHnGDGWX -O checkpoints.zip \
    && unzip -q -o checkpoints.zip && rm checkpoints.zip \
    && test -f saved_models/simswap/checkpoints/people/550000_net_G.pth

COPY fileswap_gpu.yaml configs/fileswap_gpu.yaml
COPY app.py /app/app.py

EXPOSE 7860
CMD ["python3", "/app/app.py"]
