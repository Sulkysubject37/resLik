#' Population-Level Sensor (ResLik)
#'
#' @param z Numeric vector or matrix.
#' @param ref_mean Numeric. Reference mean.
#' @param ref_sd Numeric. Reference standard deviation.
#' @param lambda Numeric. Sensitivity.
#' @param tau Numeric. Dead-zone threshold.
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
