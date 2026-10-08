"""Face-swap web UI (Gradio) for SaladCloud deployment.

Upload a source face and a target photo, hit Swap, get the result.
Wraps the Deepfake Offensive Toolkit (dot) file-based image swap.
"""
import glob
import os
import subprocess
import tempfile

import gradio as gr

DOT_DIR = "/app/dot"
CFG = os.path.join(DOT_DIR, "configs", "fileswap_gpu.yaml")


def do_swap(source_img, target_img):
    if source_img is None or target_img is None:
        raise gr.Error("Upload both a source face and a target photo first.")
    outdir = tempfile.mkdtemp(prefix="swap_")
    try:
        r = subprocess.run(
            ["python3", "scripts/image_swap.py",
             "-c", CFG, "-s", source_img, "-t", target_img, "-o", outdir],
            cwd=DOT_DIR, capture_output=True, text=True, timeout=900,
        )
    except subprocess.TimeoutExpired:
        raise gr.Error("The swap timed out. Try a smaller photo.")
    if r.returncode != 0:
        detail = (r.stderr or r.stdout or "unknown error")[-500:]
        raise gr.Error(f"Swap failed: {detail}")
    outs = sorted(glob.glob(os.path.join(outdir, "*.jpg"))
                  + glob.glob(os.path.join(outdir, "*.png")))
    if not outs:
        raise gr.Error("No output image was produced.")
    return outs[0]


demo = gr.Interface(
    fn=do_swap,
    inputs=[
        gr.Image(type="filepath", label="Source face (the face to put in)"),
        gr.Image(type="filepath", label="Target photo (the photo to change)"),
    ],
    outputs=gr.Image(type="filepath", label="Result"),
    title="Face Swap",
    description=("Upload a source face and a target photo, then press Swap. "
                 "Only swap faces you have the right to use."),
    allow_flagging="never",
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
