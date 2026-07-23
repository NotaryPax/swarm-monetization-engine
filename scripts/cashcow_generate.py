#!/usr/bin/env python3
"""Cash-cow content generator (cron-safe). Generates briefs without video rendering."""
import os, sys, json, time, subprocess, glob

ROOT = "/opt/data/content_engine"
PY = f"{ROOT}/.pubenv/bin/python"
SCRIPTS = f"{ROOT}/scripts"
N = int(os.environ.get("CC_COUNT", "2"))

def run(cmd, timeout, env=None):
    base_env = os.environ.copy()
    base_env["HOME"] = "/opt/data/home"
    if env:
        base_env.update(env)
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=base_env)
    return r.returncode, r.stdout, r.stderr

def main():
    ts0 = time.time()
    print(f"=== CASH-COW CONTENT GEN {time.strftime('%Y-%m-%d %H:%M:%S')} (n={N}) ===")

    # 0. enrichment (non-blocking)
    print("[enrich] Running competitor research...")
    rc, out, err = run([PY if os.path.exists(PY) else "python3", f"{SCRIPTS}/enrich_pipeline.py"], 180)
    print("[enrich]", "OK" if rc == 0 else f"SKIP: {err[-100:]}")

    # 1. generate briefs
    rc, out, err = run([PY, f"{SCRIPTS}/generate_content.py", str(N)], 300)
    print("[generate]", out.strip()[-500:])
    if rc != 0:
        print("[generate] FAILED:", err[-400:])
        return 1

    briefs = sorted(glob.glob(f"{ROOT}/outbox/brief_*.json"), key=os.path.getmtime, reverse=True)[:N]
    print(f"=== DONE: {len(briefs)} briefs generated in {int(time.time()-ts0)}s ===")
    return 0

if __name__ == "__main__":
    sys.exit(main())
