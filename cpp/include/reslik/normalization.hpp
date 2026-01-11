#pragma once

#include <vector>
#include <string>

namespace reslik {
namespace normalization {

/**
 * @brief Simple view into a 2D row-major matrix.
 * Shape: (n_features, embedding_dim)
 */
struct MatrixView {
    const float* data;
    size_t rows;
    size_t cols;
};

/**
 * @brief Checks if the matrix contains any NaNs or Infinities.
 * @throws std::runtime_error if invalid values are found.
 */
void validate_finiteness(const MatrixView& mat, const std::string& context);

/**
 * @brief Checks if two matrices have the same shape.
 * @throws std::runtime_error if shapes mismatch.
 */
void validate_shape(const MatrixView& a, const MatrixView& b, const std::string& context);

/**
 * @brief Checks if standard deviations are strictly positive and finite.
 * @throws std::runtime_error if invalid stddevs are found.
 */
void validate_stddev(const std::vector<float>& stddev, const std::string& context);

} // namespace normalization
} // namespace reslik
