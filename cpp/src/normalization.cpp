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

} // namespace normalization
} // namespace reslik
