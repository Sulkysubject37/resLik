#include "reslik/gating.hpp"
#include <cmath>
#include <numeric>
#include <algorithm>

namespace reslik {
namespace gating {

float softplus(float x) {
    // Stability: log(1 + exp(x)) is approx x for large x
    if (x > 20.0f) return x;
    return std::log1p(std::exp(x));
}

float compute_learned_scale(const std::vector<float>& z_tilde, const std::vector<float>& u) {
    if (z_tilde.size() != u.size()) {
        return 1.0f; // Fallback for dimension mismatch
    }
    float dot = 0.0f;
    for (size_t i = 0; i < z_tilde.size(); ++i) {
        dot += z_tilde[i] * u[i];
    }
    return softplus(dot);
}

std::vector<float> compute_discrepancy(const std::vector<float>& normalized_input) {
    // Stub: placeholder for sub-task 5
    return normalized_input; 
}

std::vector<float> compute_gate(
    const std::vector<float>& discrepancy,
    const std::vector<float>& scale
) {
    // Stub: placeholder for sub-task 6
    return std::vector<float>(discrepancy.size(), 1.0f);
}

} // namespace gating
} // namespace reslik