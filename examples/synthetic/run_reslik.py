"""
Example: Running ResLik on Synthetic Data.

Intent:
- Demonstrate API usage: Initialization, Reference Stats, and Forward Pass.
- Show how to inspect diagnostics.
- This is NOT a benchmark.
"""

import numpy as np
from reslik import ResLikUnit

def main():
    print("=== ResLik Synthetic Example ===")
    
    # 1. Setup
    n_samples = 5
    input_dim = 10
    latent_dim = 5
    
    # 2. Create synthetic "clean" data (mean=0, std=1)
    np.random.seed(42)
    clean_data = np.random.normal(0, 1, (n_samples, input_dim)).astype(np.float32)
    
    # 3. Create synthetic "outlier" data (mean=5, std=1)
    outlier_data = np.random.normal(5, 1, (n_samples, input_dim)).astype(np.float32)
    
    # 4. Initialize ResLik
    unit = ResLikUnit(input_dim=input_dim, latent_dim=latent_dim)
    
    # 5. Run on Clean Data
    print("\nRunning on Clean Data...")
    _, diag_clean = unit(clean_data, ref_mean=0.0, ref_std=1.0)
    print(diag_clean.summary())
    
    # 6. Run on Outlier Data
    print("\nRunning on Outlier Data...")
    _, diag_outlier = unit(outlier_data, ref_mean=0.0, ref_std=1.0)
    print(diag_outlier.summary())
    
    print("\nObservation: Outlier data should have lower mean gate values (more suppression).")

if __name__ == "__main__":
    main()