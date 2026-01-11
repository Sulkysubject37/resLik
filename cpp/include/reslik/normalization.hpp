#pragma once

#include <vector>

namespace reslik {
namespace normalization {

/**
 * @brief Apply standard scaling (z-score normalization).
 * 
 * @param input Input vector.
 * @param mean Mean vector.
 * @param stddev Standard deviation vector.
 * @return std::vector<float> Normalized vector.
 */
std::vector<float> standardize(
    const std::vector<float>& input,
    const std::vector<float>& mean,
    const std::vector<float>& stddev
);

} // namespace normalization
} // namespace reslik
