#' Agreement Sensor
#'
#' @param z1 First representation
#' @param z2 Second representation
#' @param eps Small constant
#' @export
agreement <- function(z1, z2, eps = 1e-8) {
  
  if (!all(dim(z1) == dim(z2))) {
    stop("Shapes must match")
  }
  
  is_vec <- is.vector(z1)
  
  if (is_vec) {
    dot_prod <- sum(z1 * z2)
    norm1 <- sqrt(sum(z1^2))
    norm2 <- sqrt(sum(z2^2))
    
    A <- dot_prod / (norm1 * norm2 + eps)
    
    ag <- A
  } else {
    dot_prod <- rowSums(z1 * z2)
    norm1 <- sqrt(rowSums(z1^2))
    norm2 <- sqrt(rowSums(z2^2))
    
    A <- dot_prod / (norm1 * norm2 + eps)
    
    ag <- A
  }
  
  list(
    agreement = ag
  )
}
