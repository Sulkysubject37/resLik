"""
Example: Applying ResLik to Mock RNA-seq Embeddings.

Intent:
- Show how ResLik fits into a gene expression workflow.
- Input: Gene embeddings (e.g., from an Autoencoder or PCA).
- Output: Gated embeddings + Quality Control diagnostics.
"""

import numpy as np
from reslik import ResLikUnit

def apply_reslik_rna():
    print("=== ResLik RNA-seq Example (Mock) ===")
    
    # Mock parameters
    n_genes = 2000 # Number of highly variable genes
    embedding_dim = 128
    
    # Mock embeddings (e.g., latent space of a VAE)
    embeddings = np.random.randn(n_genes, embedding_dim).astype(np.float32)
    
    # Initialize Unit
    unit = ResLikUnit(input_dim=embedding_dim, latent_dim=64)
    
    # Apply ResLik
    # In a real scenario, ref_mean/ref_std would come from a healthy reference atlas.
    gated_embeddings, diagnostics = unit(
        embeddings, 
        ref_mean=0.0, 
        ref_std=1.0, 
        gating_lambda=1.5 # Stricter gating
    )
    
    print(f"Input Shape: {embeddings.shape}")
    print(f"Output Shape: {gated_embeddings.shape}")
    print(f"Diagnostics: {diagnostics.summary()}")

if __name__ == "__main__":
    apply_reslik_rna()