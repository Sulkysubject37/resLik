#' Temporal Consistency Sensor
#'
#' @param z_t Current representation (vector or matrix)
#' @param z_prev Previous representation (same shape)
#' @param eps Small constant
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
