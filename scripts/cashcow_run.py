#!/usr/bin/env python3
"""Cash-cow daily run: generate fresh briefs -> render faceless videos -> publish to Pinterest.

Designed to be called by cron. Self-contained, logs to stdout.
Generates N pieces, renders each, publishes each with the Whop affiliate link.
"""
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

def cleanup_logs():
    """Truncate log files > 24hrs to prevent disk bloat."""
    import glob as gl
    for pattern in ["/opt/data/content_engine/outbox/*.log", "/tmp/cashcow*.log"]:
        for f in gl.glob(pattern):
            try:
                if os.path.getmtime(f) < time.time() - 86400:
                    open(f, "w").close()
            except:
                pass

def main():
    ts0 = time.time()
    cleanup_logs()
    print(f"=== CASH-COW RUN {time.strftime('%Y-%m-%d %H:%M:%S')} (n={N}) ===")

    # 0. enrichment pipeline (trend research + design extraction)
    print("[enrich] Running competitor research + design extraction...")
    rc, out, err = run([PY if os.path.exists(PY) else "python3", f"{SCRIPTS}/enrich_pipeline.py"], 180)
    print("[enrich]", out.strip()[-300:] if rc == 0 else f"FAILED: {err[-200:]}")
    # enrichment non-blocking — continue even if it fails

    # 1. generate briefs (uses system python; reads OPENROUTER key from .env)
    rc, out, err = run([PY, f"{SCRIPTS}/generate_content.py", str(N)], 300)
    print("[generate]", out.strip()[-500:])
    if rc != 0:
        print("[generate] FAILED:", err[-400:]); 
    # collect the freshest briefs
    briefs = sorted(glob.glob(f"{ROOT}/outbox/brief_*.json"), key=os.path.getmtime, reverse=True)[:N]
    if not briefs:
        print("No briefs produced; abort."); return 1

    published = 0
    for bp in briefs:
        b = json.load(open(bp))
        slug_suffix = os.path.basename(bp).split("_")[-1].replace(".json","")
        # 2. render video
        rc, out, err = run([PY if os.path.exists(PY) else "python3", f"{SCRIPTS}/brief_to_video.py", bp], 420)
        print(f"[render {b.get('title','?')[:40]}]", out.strip()[-300:])
        # find the rendered mp4
        vids = sorted(glob.glob(f"{ROOT}/published/cc_*_{slug_suffix}.mp4"), key=os.path.getmtime, reverse=True)
        if not vids:
            print("  -> no video, skip"); continue
        video = vids[0]
        # 3. publish to Pinterest
        rc, out, err = run([PY, f"{SCRIPTS}/publish_pin.py", bp, video], 180)
        print(f"[publish]", out.strip()[-300:])
        if rc == 0:
            published += 1
            # Record in content calendar
            try:
                subprocess.run([PY, f"{SCRIPTS}/content_calendar.py"], capture_output=True, timeout=10)
                subprocess.run([PY, "-c", f"""
import sys; sys.path.insert(0,'{SCRIPTS}')
from content_calendar import record_publish
record_publish(json.load(open('{bp}')))
"""], capture_output=True, timeout=10)
            except:
                pass
        time.sleep(8)  # gentle pacing between pins

    print(f"=== DONE: {published}/{len(briefs)} published in {int(time.time()-ts0)}s ===")
    return 0

if __name__ == "__main__":
    sys.exit(main())
