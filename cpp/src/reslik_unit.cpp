#include "reslik/reslik_unit.hpp"
#include "reslik/normalization.hpp"
#include "reslik/gating.hpp"
#include "reslik/diagnostics.hpp"
#include <iostream>
#include <cmath>
#include <numeric>
#include <algorithm>
#include <cassert>
#include <stdexcept>

namespace reslik {

// GELU activation approximation (theory.md Step 2)
static float gelu(float x) {
    return 0.5f * x * (1.0f + std::tanh(0.7978845608f * (x + 0.044715f * x * x * x)));
}

struct ResLikUnit::Impl {
    const int input_dim;  // d (const to enforce invariant)
    const int latent_dim; // h (const to enforce invariant)

    // Parameters for Step 2: f = GELU(W1 * z + b1)
    std::vector<float> W1; // (latent_dim, input_dim)
    std::vector<float> b1; // (latent_dim)

    // Parameters for Step 3: s = softplus(u^T * z_tilde)
    std::vector<float> u; // (input_dim)

    // Reference Statistics for Step 4 (Discrepancy)
    float mu_ref = 0.0f;
    float sigma_ref = 1.0f;

    // Gating Sensitivity for Step 5
    float lambda = 1.0f;
    float tau = 0.0f; // Dead-zone threshold

    // Diagnostics Storage
    diagnostics::DiagnosticReport last_report;

    // Internal Buffers (Preallocated to enforce shape invariance)
    std::vector<float> f_buffer;

    Impl(int d, int h) : input_dim(d), latent_dim(h), 
                         W1(h * d), b1(h, 0.0f),
                         u(d, 0.0f),
                         f_buffer(h, 0.0f) {
        
        if (d <= 0 || h <= 0) {
             std::string msg = "ResLikUnit: Dimensions must be positive. Got d=" + std::to_string(d) + ", h=" + std::to_string(h);
             throw std::invalid_argument(msg);
        }

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

    // Project input into f_buffer
    void project_internal(const std::vector<float>& z_tilde) {
        // Strict size check for safety
        if (z_tilde.size() != static_cast<size_t>(input_dim)) {
             throw std::runtime_error("ResLikUnit: Internal dimension mismatch in project_internal");
        }

        for (int i = 0; i < latent_dim; ++i) {
            float sum = b1[i];
            for (int j = 0; j < input_dim; ++j) {
                sum += W1[i * input_dim + j] * z_tilde[j];
            }
            f_buffer[i] = gelu(sum);
        }
    }
};

ResLikUnit::ResLikUnit(int input_dim, int latent_dim) 
    : pImpl(std::make_unique<Impl>(input_dim, latent_dim)) {}

void ResLikUnit::set_reference_stats(float mu_ref, float sigma_ref) {
    pImpl->mu_ref = mu_ref;
    pImpl->sigma_ref = std::max(1e-8f, sigma_ref);
}

void ResLikUnit::set_lambda(float lambda) {
    pImpl->lambda = lambda;
}

void ResLikUnit::set_tau(float tau) {
    pImpl->tau = std::max(0.0f, tau);
}

std::vector<float> ResLikUnit::forward(const std::vector<float>& input) {
    if (!pImpl) {
        throw std::runtime_error("ResLikUnit::forward: pImpl is null!");
    }
    if (pImpl->latent_dim <= 0) {
        throw std::runtime_error("ResLikUnit::forward: corrupted state (latent_dim <= 0)");
    }

    // 1. Validate Input Dimension
    if (input.size() != static_cast<size_t>(pImpl->input_dim)) {
        throw std::runtime_error("Input dimension mismatch in ResLikUnit::forward");
    }

    // 2. Pre-Normalization (theory.md Step 1)
    normalization::MatrixView view{input.data(), 1, static_cast<size_t>(pImpl->input_dim)};
    std::vector<float> z_tilde = normalization::standardize_per_feature(view);

    // 3. Projection (theory.md Step 2) -> Populates pImpl->f_buffer
    pImpl->project_internal(z_tilde);

    // 4. Learned Scale (theory.md Step 3)
    float s = gating::compute_learned_scale(z_tilde, pImpl->u);

    // 5. Discrepancy (theory.md Step 4)
    float C = diagnostics::compute_discrepancy(input, pImpl->mu_ref, pImpl->sigma_ref);
    
    // 6. Gating Logic (theory.md Step 5)
    float C_eff = std::max(0.0f, C - pImpl->tau);
    float gate = std::exp(-pImpl->lambda * C_eff);

    // 7. Construct Output (Enforcing Shape Invariance)
    // Always preallocate output vector of correct size.
    std::vector<float> out(pImpl->latent_dim);
    
    // Loop must iterate exactly latent_dim times
    for (int i = 0; i < pImpl->latent_dim; ++i) {
        // a_i = s * f_i
        float a_i = s * pImpl->f_buffer[i];
        
        // z'_i = gate * a_i
        // Multiplicative gating ONLY. No conditional dropping.
        out[i] = gate * a_i;
    }

    // Store diagnostics
    pImpl->last_report.mean_gate_value = gate; 
    pImpl->last_report.max_discrepancy = C; 
    pImpl->last_report.collapsed_features.clear();

    // Final Defensive Assertion
    if (out.size() == 0) {
        throw std::runtime_error("ResLikUnit::forward: Generated EMPTY output vector inside C++!");
    }
    assert(out.size() == static_cast<size_t>(pImpl->latent_dim));

    // Return the fresh vector
    return out;
}

diagnostics::DiagnosticReport ResLikUnit::get_diagnostics() const {
    return pImpl->last_report;
}

void ResLikUnit::update_stats(const std::vector<std::vector<float>>& batch) {
    // Stub
}

ResLikUnit::~ResLikUnit() = default;

} // namespace reslik
