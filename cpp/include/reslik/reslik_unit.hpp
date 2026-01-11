#pragma once

#include <vector>
#include <memory>

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
