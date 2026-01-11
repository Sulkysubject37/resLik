#include "reslik/diagnostics.hpp"
#include <cmath>
#include <numeric>

namespace reslik {
namespace diagnostics {

float compute_discrepancy(
    const std::vector<float>& z, 
    float mu_ref, 
    float sigma_ref, 
    float epsilon
) {
    if (z.empty()) return 0.0f;

    // 1. Operational mu_hat: mean of current embedding
    double sum = 0.0;
    for (float val : z) sum += val;
    float mu_hat = static_cast<float>(sum / z.size());

    // 2. Discrepancy calculation (theory.md Step 4)
    return std::abs(mu_hat - mu_ref) / (sigma_ref + epsilon);
}

DiagnosticReport get_last_report() {
    return DiagnosticReport{1.0f, 0.0f, {}};
}

} // namespace diagnostics
} // namespace reslik