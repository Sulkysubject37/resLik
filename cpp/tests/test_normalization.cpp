#include "reslik/normalization.hpp"
#include <iostream>
#include <cassert>
#include <vector>
#include <cmath>

void test_per_feature_normalization() {
    std::cout << "Testing per-feature normalization..." << std::endl;
    
    // 2 features, 3 dimensions each
    std::vector<float> data = {
        1.0f, 2.0f, 3.0f, // Feature 0: mean=2, stddev=sqrt(2/3)
        10.0f, 20.0f, 30.0f // Feature 1: mean=20, stddev=sqrt(200/3)
    };
    
    reslik::normalization::MatrixView view{data.data(), 2, 3};
    auto normalized = reslik::normalization::standardize_per_feature(view, 1e-8f);
    
    assert(normalized.size() == 6);
    
    // Check Feature 0 mean is ~0
    float m0 = (normalized[0] + normalized[1] + normalized[2]) / 3.0f;
    assert(std::abs(m0) < 1e-5);
    
    // Check Feature 1 mean is ~0
    float m1 = (normalized[3] + normalized[4] + normalized[5]) / 3.0f;
    assert(std::abs(m1) < 1e-5);
    
    // Check variance is ~1
    float v0 = (normalized[0]*normalized[0] + normalized[1]*normalized[1] + normalized[2]*normalized[2]) / 3.0f;
    assert(std::abs(v0 - 1.0f) < 1e-5);

    std::cout << "Passed." << std::endl;
}

int main() {
    test_per_feature_normalization();
    return 0;
}