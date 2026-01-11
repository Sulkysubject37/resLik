#include "reslik/normalization.hpp"
#include <stdexcept>
#include <cmath>
#include <iostream>

namespace reslik {
namespace normalization {

void validate_finiteness(const MatrixView& mat, const std::string& context) {
    for (size_t i = 0; i < mat.rows * mat.cols; ++i) {
        if (!std::isfinite(mat.data[i])) {
            throw std::runtime_error(context + ": Non-finite value (NaN or Inf) detected at index " + std::to_string(i));
        }
    }
}

void validate_shape(const MatrixView& a, const MatrixView& b, const std::string& context) {
    if (a.rows != b.rows || a.cols != b.cols) {
        throw std::runtime_error(context + ": Shape mismatch. (" + 
            std::to_string(a.rows) + "," + std::to_string(a.cols) + ") vs (" +
            std::to_string(b.rows) + "," + std::to_string(b.cols) + ")");
    }
}

void validate_stddev(const std::vector<float>& stddev, const std::string& context) {
    for (size_t i = 0; i < stddev.size(); ++i) {
        if (!std::isfinite(stddev[i])) {
            throw std::runtime_error(context + ": Non-finite standard deviation at index " + std::to_string(i));
        }
        if (stddev[i] <= 0.0f) {
            throw std::runtime_error(context + ": Non-positive standard deviation at index " + std::to_string(i) + " (" + std::to_string(stddev[i]) + ")");
        }
    }
}

std::vector<float> standardize_per_feature(const MatrixView& input, float epsilon) {
    std::vector<float> output(input.rows * input.cols);

    for (size_t i = 0; i < input.rows; ++i) {
        const float* row_ptr = input.data + (i * input.cols);
        float* out_row_ptr = output.data() + (i * input.cols);

        // 1. Compute mean over embedding dimension (theory.md Step 1)
        double sum = 0.0;
        for (size_t j = 0; j < input.cols; ++j) {
            sum += row_ptr[j];
        }
        float mean = static_cast<float>(sum / input.cols);

        // 2. Compute standard deviation (theory.md Step 1)
        double sq_sum = 0.0;
        for (size_t j = 0; j < input.cols; ++j) {
            float diff = row_ptr[j] - mean;
            sq_sum += diff * diff;
        }
        float stddev = std::sqrt(static_cast<float>(sq_sum / input.cols));

        // 3. Normalize: \tilde{z}_i = (z_i - \mu) / (\sigma + \epsilon)
        for (size_t j = 0; j < input.cols; ++j) {
            out_row_ptr[j] = (row_ptr[j] - mean) / (stddev + epsilon);
        }
    }

    return output;
}

} // namespace normalization
} // namespace reslik
