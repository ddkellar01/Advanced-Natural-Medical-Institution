"""Write-Ahead Logging (WAL) & Instant State Auto-Save Checkpointer."""

import os
import json
import time
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class SystemState:
    session_id: str
    active_phase: str
    processed_compounds: int
    system_metrics: Dict[str, Any]
    timestamp: float


class CrashRecoveryEngine:
    def __init__(self, checkpoint_dir: str = "data/checkpoints"):
        self.checkpoint_dir = checkpoint_dir
        os.makedirs(self.checkpoint_dir, exist_ok=True)

    def auto_save(self, state: SystemState) -> str:
        """Atomic write pattern to prevent corruption during sudden crashes."""
        filepath = os.path.join(self.checkpoint_dir, f"{state.session_id}.wal")
        tmp_filepath = filepath + ".tmp"
        
        with open(tmp_filepath, "w") as f:
            json.dump(asdict(state), f, indent=2)
            
        os.replace(tmp_filepath, filepath)
        return filepath

    def recover_state(self, session_id: str) -> SystemState:
        """Restores last saved state upon system crash recovery."""
        filepath = os.path.join(self.checkpoint_dir, f"{session_id}.wal")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No checkpoint found for session: {session_id}")
            
        with open(filepath, "r") as f:
            data = json.load(f)
            
        print(f"[*] State successfully recovered for session: {session_id}")
        return SystemState(**data)
      
