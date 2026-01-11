#include "reslik/reslik_unit.hpp"
#include "reslik/normalization.hpp"
#include "reslik/gating.hpp"
#include <iostream>
#include <cmath>
#include <numeric>
#include <algorithm>

namespace reslik {

// GELU activation approximation (theory.md Step 2)
static float gelu(float x) {
    return 0.5f * x * (1.0f + std::tanh(0.7978845608f * (x + 0.044715f * x * x * x)));
}

struct ResLikUnit::Impl {
    int input_dim;  // d
    int latent_dim; // h

    // Parameters for Step 2: f = GELU(W1 * z + b1)
    std::vector<float> W1; // (latent_dim, input_dim)
    std::vector<float> b1; // (latent_dim)

    // Parameters for Step 3: s = softplus(u^T * z_tilde)
    std::vector<float> u; // (input_dim)

    Impl(int d, int h) : input_dim(d), latent_dim(h), 
                         W1(h * d), b1(h, 0.0f),
                         u(d, 0.0f) {
        // Deterministic initialization: scaled identity or simple Xavier-like
        float scale = std::sqrt(2.0f / (d + h));
        for (int i = 0; i < h; ++i) {
            for (int j = 0; j < d; ++j) {
                // Pseudo-random deterministic fill
                W1[i * d + j] = (( (i * d + j) % 100) / 50.0f - 1.0f) * scale;
            }
        }
        // Initialize u to small values
        for (int j = 0; j < d; ++j) {
            u[j] = ((j % 100) / 1000.0f);
        }
    }

    std::vector<float> project(const std::vector<float>& z_tilde) {
        std::vector<float> f(latent_dim, 0.0f);
        for (int i = 0; i < latent_dim; ++i) {
            float sum = b1[i];
            for (int j = 0; j < input_dim; ++j) {
                sum += W1[i * input_dim + j] * z_tilde[j];
            }
            f[i] = gelu(sum);
        }
        return f;
    }
};

ResLikUnit::ResLikUnit(int input_dim, int latent_dim) 
    : pImpl(std::make_unique<Impl>(input_dim, latent_dim)) {}

std::vector<float> ResLikUnit::forward(const std::vector<float>& input) {
    if (input.size() != static_cast<size_t>(pImpl->input_dim)) {
        throw std::runtime_error("Input dimension mismatch in ResLikUnit::forward");
    }

    // Step 1: Pre-Normalization
    normalization::MatrixView view{input.data(), 1, static_cast<size_t>(pImpl->input_dim)};
    std::vector<float> z_tilde = normalization::standardize_per_feature(view);

    // Step 2: Shared Feed-Forward Projection
    std::vector<float> f = pImpl->project(z_tilde);

    // Step 3: Learned Scale Computation
    float s = gating::compute_learned_scale(z_tilde, pImpl->u);

    // a_i = s_i * f_i
    std::vector<float> a = f;
    for (float& val : a) val *= s;

    // TODO: Steps 4-5 (Discrepancy and Final Gating) in subsequent sub-tasks
    return a; 
}

void ResLikUnit::update_stats(const std::vector<std::vector<float>>& batch) {
    // Stub for now, Phase 2 focuses on forward pass
}

ResLikUnit::~ResLikUnit() = default;

} // namespace reslik