"""L0: one command to see what works on this machine. Run: uv run python labs/L0_env/check_env.py"""
import importlib, os, platform, shutil, subprocess, sys


def ver(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=15).stdout.strip().splitlines()[0]
    except Exception:
        return None


rows = []
rows.append(("python", sys.version.split()[0], sys.version_info[:2] == (3, 12)))
for mod in ["torch", "numpy", "transformers", "anthropic", "openai", "pytest", "dotenv"]:
    try:
        m = importlib.import_module(mod)
        rows.append((mod, getattr(m, "__version__", "ok"), True))
    except Exception as e:
        rows.append((mod, f"MISSING ({type(e).__name__})", False))
try:
    import torch
    rows.append(("cuda gpu", str(torch.cuda.is_available()) + " (CPU-only is fine until L7/A4)", True))
except Exception:
    pass
for tool in ["git", "uv", "gh", "ssh", "node", "wsl"]:
    p = shutil.which(tool)
    rows.append((tool, p or "not found", bool(p) or tool in ("wsl", "node")))
for key in ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "HF_TOKEN"]:
    rows.append((key, "set" if os.environ.get(key) else "not set (needed for L5 live run only)", True))
rows.append(("os", platform.platform(), True))

w = max(len(r[0]) for r in rows)
for name, val, ok in rows:
    print(f"{'OK ' if ok else 'FIX'}  {name:<{w}}  {val}")
sys.exit(0 if all(r[2] for r in rows) else 1)
