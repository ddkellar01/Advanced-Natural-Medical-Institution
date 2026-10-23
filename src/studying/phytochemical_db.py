"""Botanical SMILES Database and Receptor Target Mapping."""

from typing import List, Dict, Any


class PhytochemicalDatabase:
    def __init__(self):
        self._database: List[Dict[str, Any]] = [
            {
                "name": "Curcumin",
                "smiles": "CC(=O)C=C(C)C1=CC=C(O)C=C1",
                "target": "NF-kB Pathway",
                "category": "Polyphenol"
            },
            {
                "name": "Sulforaphane",
                "smiles": "C1=CC=C2C(=C1)C=CN2",
                "target": "Nrf2 Pathway",
                "category": "Isothiocyanate"
            },
            {
                "name": "EGCG",
                "smiles": "C1C(C(OC2=CC(=CC(=C21)O)O)C3=CC(=C(C(=C3)O)O)O)OC(=O)C4=CC(=C(C(=C4)O)O)O",
                "target": "AMPK Pathway",
                "category": "Catechin"
            }
        ]

    def get_all_compounds(self) -> List[Dict[str, Any]]:
        return self._database

    def query_by_target(self, target: str) -> List[Dict[str, Any]]:
        return [c for c in self._database if c["target"] == target]
      
