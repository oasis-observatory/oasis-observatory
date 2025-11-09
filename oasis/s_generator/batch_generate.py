# oasis/s_generator/batch_generate_single_asi.py

#!/usr/bin/env python3
"""
OASIS BATCH GENERATOR — SINGLE-ASI SCENARIOS
"""
import subprocess
import sys
import time
from datetime import datetime

# CORRECT: Use the actual subcommand
PYTHON = sys.executable
CLI_COMMAND = [PYTHON, "-m", "oasis.s_generator.cli", "--n", "1"]

def generate_one():
    """Call oasis generate via correct subcommand."""
    result = subprocess.run(
        CLI_COMMAND,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        lines = result.stdout.strip().split("\n")
        # Find the last non-empty line (usually the title)
        for line in reversed(lines):
            if line.strip() and not line.startswith("INFO"):
                print("Generated:", line.strip())
                return
        print("Generated: [scenario]")
    else:
        print("ERROR:", result.stderr.strip())

def main():
    print("="*65)
    print("OASIS BATCH GENERATOR — SINGLE-ASI SCENARIOS")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {PYTHON}")
    print(f"Command: {' '.join(CLI_COMMAND)}")
    print("="*65)

    try:
        n_str = input(f"\nHow many single-ASI scenarios to generate? [5]: ").strip()
        n = int(n_str) if n_str else 5
    except:
        n = 5

    delay = 0.5

    print(f"\nGenerating {n} scenarios... (delay: {delay}s)\n")

    start_time = time.time()
    success_count = 0
    for i in range(1, n + 1):
        print(f"[{i:3d}/{n}] Generating...", end=" ")
        try:
            generate_one()
            success_count += 1
        except Exception as e:
            print(f"FAILED: {e}")
        if i < n:
            time.sleep(delay)

    total_time = time.time() - start_time
    print("\n" + "="*65)
    print(f"BATCH COMPLETE")
    print(f"Successful: {success_count}/{n}")
    print(f"Total time: {total_time:.1f}s ({total_time/max(1,success_count):.2f}s per success)")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*65)

if __name__ == "__main__":
    main()