#include "reslik/gating.hpp"

namespace reslik {
namespace gating {

std::vector<float> compute_discrepancy(const std::vector<float>& normalized_input) {
    // Stub
    return normalized_input; 
}

std::vector<float> compute_gate(
    const std::vector<float>& discrepancy,
    const std::vector<float>& scale
) {
    // Stub: return 1s (no gating)
    return std::vector<float>(discrepancy.size(), 1.0f);
}

} // namespace gating
} // namespace reslik
