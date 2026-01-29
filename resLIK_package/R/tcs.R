#' Temporal Consistency Sensor
#'
#' @title Temporal Consistency Sensor
#'
#' @description
#' The Temporal Consistency Sensor (TCS) monitors the evolution of a latent representation
#' over time. It quantifies "drift" as the relative rate of change and converts it
#' into a stability score.
#'
#' @details
#' The sensor computes the L2 distance between the current state `z_t` and the previous state `z_prev`.
#' This distance is normalized by the magnitude of the previous state to produce a relative drift score.
#' Consistency is defined as `exp(-drift)`.
#'
#' This metric is essential for detecting "shock" events where the representation changes
#' too rapidly for the downstream system to adapt safely.
#'
#' @param z_t Numeric vector or matrix. The current latent representation.
#' @param z_prev Numeric vector or matrix. The previous latent representation. Must have the same shape as `z_t`.
#' @param eps Numeric. Small constant to avoid division by zero. Defaults to 1e-6.
#'
#' @return A list containing:
#' \item{drift}{The relative drift score (non-negative).}
#' \item{consistency}{The consistency score (0 to 1).}
#'
#' @examples
#' # Example 1: Stable Evolution
#' z_t0 <- c(1.0, 0.0)
#' z_t1 <- c(1.01, 0.01)
#' tcs(z_t1, z_t0)
#'
#' # Example 2: Sudden Shock
#' z_shock <- c(5.0, 0.0)
#' tcs(z_shock, z_t0)
#'
#' @export
tcs <- function(z_t, z_prev, eps = 1e-6) {
  
  if (!all(dim(z_t) == dim(z_prev))) {
    stop("z_t and z_prev must have identical shape")
  }
  
  is_vec <- is.vector(z_t)
  
  if (is_vec) {
    delta_vec <- z_t - z_prev
    norm_delta <- sqrt(sum(delta_vec^2))
    norm_prev <- sqrt(sum(z_prev^2))
    
    D_time <- norm_delta / (norm_prev + eps)
    consistency <- exp(-D_time)
    
    drift <- D_time
    cons <- consistency
  } else {
    # Matrix
    delta_mat <- z_t - z_prev
    
    # Row-wise L2 norms
    norm_delta <- sqrt(rowSums(delta_mat^2))
    norm_prev <- sqrt(rowSums(z_prev^2))
    
    D_time <- norm_delta / (norm_prev + eps)
    consistency <- exp(-D_time)
    
    drift <- D_time
    cons <- consistency
  }
  
  list(
    drift = drift,
    consistency = cons
  )
}