"""
Example: Cross-Modal Consistency Check.

Intent:
- Demonstrate ResLik's modality-agnostic interface.
- Same unit instance applied to two different 'modalities' (mocked).
"""

import numpy as np
from reslik import ResLikUnit

def test_cross_modal():
    print("=== ResLik Cross-Modal Example ===")
    
    dim = 50
    unit = ResLikUnit(input_dim=dim, latent_dim=25)
    
    # Modality A: "RNA" (Standard Normal)
    rna_embed = np.random.normal(0, 1, (10, dim)).astype(np.float32)
    
    # Modality B: "ATAC" (Different Distribution)
    atac_embed = np.random.normal(2, 0.5, (10, dim)).astype(np.float32)
    
    print("Processing Modality A (RNA)...")
    _, diag_rna = unit(rna_embed, ref_mean=0.0, ref_std=1.0)
    print(f"  Gate: {diag_rna.mean_gate_value:.3f}")
    
    print("Processing Modality B (ATAC)...")
    # Note: We must update reference stats for the new modality!
    _, diag_atac = unit(atac_embed, ref_mean=2.0, ref_std=0.5)
    print(f"  Gate: {diag_atac.mean_gate_value:.3f}")
    
    print("\nKey Takeaway: ResLik adapts to the modality via reference statistics.")

if __name__ == "__main__":
    test_cross_modal()