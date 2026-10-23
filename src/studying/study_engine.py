"""Updated Botanical Discovery Engine utilizing Hybrid GCN-GAT."""

import torch
from typing import Dict, Any
from src.studying.hybrid_gcn_gat import HybridGCN_GATModel


class BotanicalDiscoveryEngine:
    def __init__(self):
        # Initialize Hybrid GCN-GAT model (e.g., 64 input features -> 128 hidden dim -> 1 binding score)
        self.hybrid_model = HybridGCN_GATModel(num_node_features=64, hidden_dim=128, output_dim=1)
        self.hybrid_model.eval()

    def screen_compound_hybrid(self, compound_name: str, node_features: torch.Tensor, adjacency_matrix: torch.Tensor) -> Dict[str, Any]:
        """Runs the hybrid GCN-GAT model to predict binding affinity."""
        with torch.no_grad():
            prediction = self.hybrid_model(node_features, adjacency_matrix)
            binding_affinity = float(prediction.item())

        return {
            "compound_name": compound_name,
            "architecture": "Hybrid GCN-GAT",
            "predicted_binding_affinity_kcal_mol": round(binding_affinity, 2),
            "status": "VIABLE" if binding_affinity < -7.5 else "REJECTED"
        }
