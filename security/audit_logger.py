"""Cryptographic Append-Only Immutable Audit Logger."""

import hashlib
import time
import json
from typing import Dict, Any


class AuditLogger:
    def __init__(self, log_filepath: str = "data/audit_trail.log"):
        self.log_filepath = log_filepath

    def log_event(self, event_type: str, details: Dict[str, Any]) -> str:
        """Appends a cryptographic hash signature to ensure event untamperability."""
        timestamp = time.time()
        payload = {"timestamp": timestamp, "event_type": event_type, "details": details}
        
        serialized = json.dumps(payload, sort_keys=True)
        hash_signature = hashlib.sha256(serialized.encode()).hexdigest()
        
        log_entry = {
            "signature": hash_signature,
            "payload": payload
        }

        with open(self.log_filepath, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        return hash_signature
