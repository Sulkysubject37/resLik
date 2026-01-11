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

/**
 * @brief Normalizes each feature embedding independently.
 * Equation: \tilde{z}_i = (z_i - \mu(z_i)) / (\sigma(z_i) + \epsilon)
 * 
 * @param input Input matrix of shape (n_features, embedding_dim)
 * @param epsilon Stability constant.
 * @return std::vector<float> Normalized data in row-major order.
 */
std::vector<float> standardize_per_feature(const MatrixView& input, float epsilon = 1e-8f);

} // namespace normalization
} // namespace reslik
