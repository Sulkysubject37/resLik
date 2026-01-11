#pragma once

#include <vector>

namespace reslik {
namespace gating {

/**
 * @brief Compute the discrepancy score for an embedding.
 * 
 * @param normalized_input Standardized input vector.
 * @return std::vector<float> Element-wise discrepancy scores.
 */
std::vector<float> compute_discrepancy(const std::vector<float>& normalized_input);

/**
 * @brief Compute the multiplicative gate values.
 * 
 * @param discrepancy Discrepancy scores.
 * @param scale Learned scale factors.
 * @return std::vector<float> Gate values (0 to 1).
 */
std::vector<float> compute_gate(
    const std::vector<float>& discrepancy,
    const std::vector<float>& scale
);

} // namespace gating
} // namespace reslik
