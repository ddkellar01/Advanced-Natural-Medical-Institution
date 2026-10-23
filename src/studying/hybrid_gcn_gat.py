"""Hybrid GCN-GAT Neural Network Module for Phytochemical Molecular Screening."""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any


class GraphConvolutionLayer(nn.Module):
    def __init__(self, in_features: int, out_features: int):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)

    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        """Isotropic neighborhood aggregation (GCN style)."""
        support = self.linear(x)
        # Message passing via normalized adjacency matrix
        out = torch.matmul(adj, support)
        return F.relu(out)


class GraphAttentionLayer(nn.Module):
    def __init__(self, in_features: int, out_features: int, alpha: float = 0.2):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.alpha = alpha

        self.W = nn.Parameter(torch.zeros(size=(in_features, out_features)))
        nn.init.xavier_uniform_(self.W.data, gain=1.414)
        
        self.a = nn.Parameter(torch.zeros(size=(2 * out_features, 1)))
        nn.init.xavier_uniform_(self.a.data, gain=1.414)

        self.leakyrelu = nn.LeakyReLU(self.alpha)

    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        """Anisotropic attention mechanism (GAT style)."""
        h = torch.matmul(x, self.W)
        N = h.size(0)

        a_input = torch.cat([h.repeat(1, N).view(N * N, -1), h.repeat(N, 1)], dim=1)
        a_input = a_input.view(N, N, 2 * self.out_features)
        
        e = self.leakyrelu(torch.matmul(a_input, self.a).squeeze(2))
        
        zero_vec = -9e15 * torch.ones_like(e)
        attention = torch.where(adj > 0, e, zero_vec)
        attention = F.softmax(attention, dim=1)
        
        out = torch.matmul(attention, h)
        return F.elu(out)


class HybridGCN_GATModel(nn.Module):
    def __init__(self, num_node_features: int, hidden_dim: int, output_dim: int):
        super().__init__()
        # Parallel or sequential fusion of GCN and GAT
        self.gcn_branch = GraphConvolutionLayer(num_node_features, hidden_dim)
        self.gat_branch = GraphAttentionLayer(num_node_features, hidden_dim)
        
        # Fusion layer combining both topological and attentive representations
        self.fusion_fc = nn.Linear(hidden_dim * 2, hidden_dim)
        self.predictor = nn.Linear(hidden_dim, output_dim)

    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        """Executes hybrid feature extraction and binding affinity regression."""
        gcn_out = self.gcn_branch(x, adj)
        gat_out = self.gat_branch(x, adj)
        
        # Concatenate topological structure (GCN) with attentive functional focus (GAT)
        combined = torch.cat([gcn_out, gat_out], dim=1)
        fused = F.relu(self.fusion_fc(combined))
        
        # Global mean pooling over nodes to predict molecular property / affinity
        graph_representation = torch.mean(fused, dim=0, keepdim=True)
        affinity_score = self.predictor(graph_representation)
        
        return affinity_score
