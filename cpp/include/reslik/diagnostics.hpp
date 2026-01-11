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
 * @brief Get the latest diagnostic report.
 * 
 * @return DiagnosticReport 
 */
DiagnosticReport get_last_report();

} // namespace diagnostics
} // namespace reslik
