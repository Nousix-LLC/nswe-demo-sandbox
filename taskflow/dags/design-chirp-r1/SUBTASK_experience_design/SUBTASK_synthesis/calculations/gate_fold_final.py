#!/usr/bin/env python3
"""
Final synthesis gate check — re-derives evidence from the current on-disk deliverable.
Identical logic to gate_fold.py; run at fold time for definitive SYNTHESIS.md evidence.
"""
import sys
sys.path.insert(0, "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_experience_design/SUBTASK_synthesis/calculations")
# Re-run by importing gate_fold.py logic directly.
# Since gate_fold.py is a script (not a module), exec it here.
import runpy
runpy.run_path(
    "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_experience_design/SUBTASK_synthesis/calculations/gate_fold.py",
    run_name="__main__"
)
