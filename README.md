# FaceSwap Web UI

A simple web UI for face-swapping photos, powered by the [Deepfake Offensive Toolkit](https://github.com/blues-creations/dot) (SimSwap) and served with [Gradio](https://www.gradio.app/). Built to run as a GPU container (e.g. on SaladCloud).

Upload a **source face** and a **target photo**, hit **Swap**, and download the result.

> **Use it responsibly:** only swap faces you have the right to use — your own, or someone who has clearly said yes.

## Run it (Docker)

Requires an NVIDIA GPU with the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/) installed.

```bash
docker run --gpus all -p 7860:7860 ghcr.io/boogie07/faceswap-webui/faceswap-webui:latest
```

Then open http://localhost:7860 in a browser.

## Deploy on SaladCloud

1. Create a **Container Group** at [portal.salad.com](https://portal.salad.com).
2. Image: `ghcr.io/boogie07/faceswap-webui/faceswap-webui:latest`
3. Pick a **GPU** node group.
4. Expose container port **7860**.
5. Deploy — the Gradio UI is served on the group's public endpoint.

## How it works

- `app.py` — Gradio interface (port 7860). Takes the two uploads and calls dot's `scripts/image_swap.py` with the GPU config.
- `Dockerfile` — CUDA 12.1 runtime, PyTorch (cu121), InsightFace + `onnxruntime-gpu`, Gradio. The ~4.1 GB SimSwap/GPEN/ArcFace checkpoints are baked into the image so the container starts ready.
- `fileswap_gpu.yaml` — copied into the image as `configs/fileswap_gpu.yaml`; enables GPU inference (`use_gpu: true`).
- `.github/` — workflow that builds the image and pushes it to GHCR on every push to `main`.

## Build the image yourself

```bash
docker build -t faceswap-webui .
```

## Notes

- Image swaps only (no video in this build); a single swap typically takes under a minute on a GPU and times out after 15 minutes.
- Uploaded images are processed in a temp directory inside the container and are not stored.
