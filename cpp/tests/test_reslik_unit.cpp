#include "reslik/reslik_unit.hpp"
#include <iostream>
#include <cassert>
#include <vector>
#include <cmath>
#include <algorithm>

void test_forward_shape_and_finiteness() {
    std::cout << "Testing forward shape and finiteness..." << std::endl;
    int d = 128;
    int h = 64;
    reslik::ResLikUnit unit(d, h);
    
    std::vector<float> input(d, 0.5f);
    auto output = unit.forward(input);
    
    assert(output.size() == static_cast<size_t>(h));
    for (float val : output) {
        assert(std::isfinite(val));
    }
    std::cout << "Passed." << std::endl;
}

void test_monotonic_gating() {
    std::cout << "Testing monotonic gating behavior..." << std::endl;
    int d = 10;
    int h = 5;
    reslik::ResLikUnit unit(d, h);
    unit.set_reference_stats(0.0f, 1.0f); // mu=0, sigma=1
    unit.set_lambda(1.0f);

    // 1. Input at the reference mean (discrepancy ~ 0)
    std::vector<float> clean_input(d, 0.0f);
    auto clean_output = unit.forward(clean_input);
    
    // 2. Input far from reference mean (high discrepancy)
    std::vector<float> noisy_input(d, 10.0f);
    auto noisy_output = unit.forward(noisy_input);

    // Compute norms for comparison
    float clean_norm = 0.0f;
    for (float v : clean_output) clean_norm += v*v;
    
    float noisy_norm = 0.0f;
    for (float v : noisy_output) noisy_norm += v*v;

    // The noisy input should be gated (suppressed) more than the clean input.
    // Note: Since clean_input is all zeros, the FF projection might also be small,
    // but the GATING factor exp(-lambda*C) will be much smaller for the noisy input.
    // Let's check the ratio if possible, or just verify noisy is suppressed.
    
    // 2. Use non-constant inputs that are "clean" vs "noisy"
    // We add a tiny bit of variation to avoid zero-variance issue.
    std::vector<float> base_clean(d, 0.1f);
    base_clean[0] = 0.11f; // variance > 0

    std::vector<float> base_noisy(d, 5.0f);
    base_noisy[0] = 5.01f; // variance > 0
    
    auto out_clean = unit.forward(base_clean);
    auto out_noisy = unit.forward(base_noisy);
    
    // We expect the gate for noisy to be much smaller.
    // C_clean = |0.1 - 0| / 1 = 0.1  => gate = exp(-0.1) ~ 0.9
    // C_noisy = |5.0 - 0| / 1 = 5.0  => gate = exp(-5.0) ~ 0.006
    
    // Since weights are shared, we can roughly expect suppression.
    // Let's just print to verify for now or check ratio if weights allow.
    std::cout << "  Clean output[0]: " << out_clean[0] << std::endl;
    std::cout << "  Noisy output[0]: " << out_noisy[0] << std::endl;
    
    // If we want a strict test, we can check the gate factor indirectly 
    // by comparing outputs where the input to the FF part is normalized.
    // But standardized_per_feature makes them both zero-mean, unit-variance before FF.
    // So the FF part 'a' will be similar for any constant input (with different signs maybe).
    // The GATING however depends on the raw input 'input' via diagnostics::compute_discrepancy.
    
    // Thus, if out_clean and out_noisy receive the same standardized input internally,
    // their relative magnitude is determined ONLY by the gate.
    
    // Constant vectors (non-zero) all standardize to zero after mean subtraction.
    // Wait, standardize_per_feature: (val - mean) / (stddev + eps).
    // If all values are same, stddev is 0. Output is (val - val) / eps = 0.
    
    // So for constant vectors, z_tilde is always 0. 
    // Then f = GELU(W1*0 + b1) = GELU(b1).
    // a = s * f = softplus(u^T * 0) * GELU(b1) = softplus(0) * GELU(b1) = log(2) * GELU(b1).
    
    // The ONLY thing that changes between out_clean and out_noisy for constant inputs 
    // is the gate factor exp(-lambda * C).
    
    // C_clean = 0.1, C_noisy = 5.0.
    // gate_clean = exp(-0.1) > gate_noisy = exp(-5.0).
    // Therefore, ||out_clean|| > ||out_noisy||.
    
    float n_clean = 0.0f; for(float v : out_clean) n_clean += v*v;
    float n_noisy = 0.0f; for(float v : out_noisy) n_noisy += v*v;
    
    assert(n_clean > n_noisy);
    std::cout << "Passed." << std::endl;
}

int main() {
    test_forward_shape_and_finiteness();
    test_monotonic_gating();
    return 0;
}