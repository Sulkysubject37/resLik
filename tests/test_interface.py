import pytest
import numpy as np
from reslik import ResLikUnit

def test_shape_preservation():
    input_dim = 20
    latent_dim = 10
    n_samples = 5
    
    unit = ResLikUnit(input_dim, latent_dim)
    data = np.random.randn(n_samples, input_dim).astype(np.float32)
    
    output, _ = unit(data)
    
    assert output.shape == (n_samples, latent_dim)
    assert np.all(np.isfinite(output))

def test_determinism():
    input_dim = 10
    unit = ResLikUnit(input_dim, 5)
    data = np.random.randn(1, input_dim).astype(np.float32)
    
    out1, _ = unit(data)
    out2, _ = unit(data)
    
    np.testing.assert_array_equal(out1, out2)

def test_input_validation():
    unit = ResLikUnit(10, 5)
    
    # 1. Dimension Mismatch
    with pytest.raises(ValueError, match="Input feature dimension"):
        unit(np.zeros((1, 5)))
        
    # 2. NaNs
    bad_data = np.zeros((1, 10))
    bad_data[0, 0] = np.nan
    with pytest.raises(ValueError, match="NaNs"):
        unit(bad_data)
        
    # 3. Invalid Reference Std
    with pytest.raises(ValueError, match="positive"):
        unit(np.zeros((1, 10)), ref_std=-1.0)

def test_diagnostics_structure():
    unit = ResLikUnit(10, 5)
    data = np.zeros((1, 10))
    
    _, diag = unit(data)
    
    assert hasattr(diag, "mean_gate_value")
    assert hasattr(diag, "max_discrepancy")
    assert isinstance(diag.to_dict(), dict)
    assert "Mean Gate Value" in diag.summary()
