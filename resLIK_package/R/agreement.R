#' Agreement Sensor
#'
#' @title Agreement Sensor
#'
#' @description
#' The Agreement Sensor measures the alignment between two latent representations, typically
#' from different modalities or redundant sensors. It uses cosine similarity to quantify
#' agreement.
#'
#' @details
#' The sensor computes the cosine similarity between `z1` and `z2`:
#' \deqn{A = \frac{z_1 \cdot z_2}{||z_1|| ||z_2|| + \epsilon}}
#'
#' Values close to 1 indicate strong agreement, 0 indicates orthogonality (no agreement),
#' and -1 indicates opposition. In the context of RLCS, high positive agreement is generally
#' required for a `PROCEED` signal.
#'
#' @param z1 Numeric vector or matrix. The first representation.
#' @param z2 Numeric vector or matrix. The second representation. Must have the same shape as `z1`.
#' @param eps Numeric. Small constant for numerical stability. Defaults to 1e-8.
#'
#' @return A list containing:
#' \item{agreement}{The cosine similarity score (-1 to 1).}
#'
#' @examples
#' # Example 1: Perfect Agreement
#' z1 <- c(1, 2, 3)
#' z2 <- c(2, 4, 6)
#' agreement(z1, z2)
#'
#' # Example 2: Disagreement (Orthogonal)
#' z3 <- c(1, 0, 0)
#' z4 <- c(0, 1, 0)
#' agreement(z3, z4)
#'
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