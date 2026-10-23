"""Anti-Hack Shielding: Adversarial Prompt Inspection & WAF Filtering."""

import re
from typing import Dict, Any, Tuple


class AntiHackShield:
    def __init__(self):
        self.blocked_patterns = [
            r"ignore previous instructions",
            r"system prompt override",
            r"drop database",
            r"<script>",
            r"exec\("
        ]

    def inspect_payload(self, input_string: str) -> Tuple[bool, str]:
        """Scans inputs for prompt injections, malicious scripts, and query tampering."""
        for pattern in self.blocked_patterns:
            if re.search(pattern, input_string, re.IGNORECASE):
                return False, f"SECURITY ALERT: Malicious input pattern matched: '{pattern}'"
        return True, "INSPECTION_PASSED"
