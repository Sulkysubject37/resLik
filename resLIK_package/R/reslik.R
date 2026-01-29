#' Population-Level Sensor (ResLik)
#'
#' @title Residual Likelihood Sensor
#'
#' @description
#' The Residual Likelihood (ResLik) sensor measures the conformity of a latent representation
#' against a population reference distribution. It acts as a soft gate, suppressing
#' "out-of-distribution" (OOD) signals while preserving "in-distribution" (ID) fidelity.
#'
#' @details
#' The sensor operates in four steps:
#' 1. **Normalization**: The input `z` is Z-score normalized using `ref_mean` and `ref_sd`.
#' 2. **Discrepancy**: The Mean Absolute Deviation (MAD) is computed for each sample.
#' 3. **Gating**: A gating factor is computed as `exp(-lambda * max(0, discrepancy - tau))`.
#'    This creates a "dead-zone" `tau` where minor deviations are ignored.
#' 4. **Output**: The original `z` is scaled by the gating factor.
#'
#' This implementation is fully deterministic and stateless.
#'
#' @param z Numeric vector or matrix. The latent representation to evaluate.
#' @param ref_mean Numeric or vector. The reference mean of the population. Defaults to 0.
#' @param ref_sd Numeric or vector. The reference standard deviation of the population. Defaults to 1.
#' @param lambda Numeric. The sensitivity of the gate. Higher values suppress OOD samples more aggressively. Defaults to 1.0.
#' @param tau Numeric. The dead-zone threshold. Discrepancies below this value are ignored. Defaults to 0.05.
#'
#' @return A list containing:
#' \item{gated}{The gated representation (same shape as `z`).}
#' \item{diagnostics}{A list of diagnostic metrics:
#'   \itemize{
#'     \item \code{discrepancy}: The raw discrepancy scores.
#'     \item \code{max_discrepancy}: The maximum discrepancy in the batch.
#'     \item \code{mean_discrepancy}: The mean discrepancy in the batch.
#'   }
#' }
#'
#' @examples
#' # Example 1: In-Distribution Sample
#' z_id <- c(0.1, -0.2, 0.05)
#' out_id <- reslik(z_id)
#' print(out_id$gated) # Should be close to z_id
#'
#' # Example 2: Out-of-Distribution Sample
#' z_ood <- c(5.0, 5.0, 5.0)
#' out_ood <- reslik(z_ood)
#' print(out_ood$gated) # Should be strongly suppressed
#'
#' @export
reslik <- function(z,
                   ref_mean = 0,
                   ref_sd = 1,
                   lambda = 1.0,
                   tau = 0.05) {
  
  # Ensure z is handled consistently
  # If vector, treat as single sample (n=1, d=length) for calculation, 
  # but preserve shape in output?
  # Prompt: "Preserve shape exactly"
  
  is_vec <- is.vector(z)
  
  # Normalize
  # (z - ref_mean) / (ref_sd + 1e-8)
  # R recycling handles scalar ref_mean/sd
  z_norm <- (z - ref_mean) / (ref_sd + 1e-8)
  
  # Discrepancy
  if (is_vec) {
    # Single sample
    D_i <- mean(abs(z_norm))
    # g_i is scalar
    gate <- exp(-lambda * max(0, D_i - tau))
    z_out <- z * gate
    
    # Diagnostics
    diag_disc <- D_i
    diag_max <- D_i
    diag_mean <- D_i
    
  } else {
    # Matrix (n x d)
    # Row-wise mean
    D_i <- rowMeans(abs(z_norm))
    
    # Gate (element-wise max and exp)
    # max(0, x) -> pmax(0, x) for vectors
    gate <- exp(-lambda * pmax(0, D_i - tau))
    
    # Output: Scale rows
    # R multiplies column-wise by recycling the vector.
    # We want to multiply each row i by gate[i].
    # Since matrix is stored column-major, and vector is length nrow,
    # default multiplication m * v works exactly as intended (v[1] scales row 1, etc.)
    z_out <- z * gate
    
    diag_disc <- D_i
    diag_max <- max(D_i)
    diag_mean <- mean(D_i)
  }
  
  list(
    gated = z_out,
    diagnostics = list(
      discrepancy = diag_disc,
      max_discrepancy = diag_max,
      mean_discrepancy = diag_mean
    )
  )
}