#pragma once

#include <vector>
#include <memory>
#include "reslik/diagnostics.hpp"

namespace reslik {

/**
 * @brief Main Residual Likelihood Unit.
 * 
 * Coordinates normalization, gating, and diagnostic collection.
 */
class ResLikUnit {
public:
    /**
     * @brief Construct a new ResLikUnit object
     * 
     * @param input_dim Dimension of input embeddings (d).
     * @param latent_dim Dimension of the projection (h).
     */
    explicit ResLikUnit(int input_dim, int latent_dim);

    /**
     * @brief Apply the ResLik gating mechanism.
     * 
     * @param input Input embedding vector.
     * @return std::vector<float> Gated output vector.
     */
    std::vector<float> forward(const std::vector<float>& input);

    /**
     * @brief Set the reference statistics for discrepancy calculation.
     * 
     * @param mu_ref Reference mean.
     * @param sigma_ref Reference standard deviation.
     */
    void set_reference_stats(float mu_ref, float sigma_ref);

    /**
     * @brief Set the gating sensitivity lambda.
     */
    void set_lambda(float lambda);

    /**
     * @brief Set the discrepancy dead-zone threshold tau.
     * Gating will only activate if discrepancy > tau.
     */
    void set_tau(float tau);

    /**
     * @brief Get the internal state diagnostics.
     * 
     * @return DiagnosticReport Structure containing diagnostic data.
     */
    diagnostics::DiagnosticReport get_diagnostics() const;

    /**
     * @brief Update internal running statistics (e.g., for batch norm).
     * 
     * @param batch Batch of input vectors.
     */
    void update_stats(const std::vector<std::vector<float>>& batch);

    ~ResLikUnit();

private:
    struct Impl;
    std::unique_ptr<Impl> pImpl;
};

} // namespace reslik
