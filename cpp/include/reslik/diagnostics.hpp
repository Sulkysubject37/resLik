#pragma once

#include <string>
#include <map>
#include <vector>

namespace reslik {
namespace diagnostics {

/**
 * @brief Container for runtime diagnostics.
 */
struct DiagnosticReport {
    float mean_gate_value;
    float max_discrepancy;
    std::vector<int> collapsed_features;
};

/**
 * @brief Compute the discrepancy score for a feature embedding.
 * Equation: C_i = |mu_hat_i - mu_ref_i| / (sigma_ref_i + epsilon)
 * 
 * @param z Input embedding vector.
 * @param mu_ref Reference mean for this feature.
 * @param sigma_ref Reference standard deviation for this feature.
 * @param epsilon Stability constant.
 * @return float Discrepancy score C_i.
 */
float compute_discrepancy(
    const std::vector<float>& z, 
    float mu_ref, 
    float sigma_ref, 
    float epsilon = 1e-8f
);

/**
 * @brief Get the latest diagnostic report.
 * 
 * @return DiagnosticReport 
 */
DiagnosticReport get_last_report();

} // namespace diagnostics
} // namespace reslik
