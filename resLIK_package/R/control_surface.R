#' Deterministic Control Surface
#'
#' @title RLCS Control Surface
#'
#' @description
#' The Control Surface integrates inputs from multiple reliability sensors (ResLik, TCS, Agreement)
#' to issue a standardized control signal (`PROCEED`, `DEFER`, `ABSTAIN`). It uses a deterministic,
#' rule-based logic to ensure safety and predictability.
#'
#' @details
#' The logic implements a "Conservative OR" strategy:
#' \itemize{
#'   \item \strong{ABSTAIN}: Triggered if `ResLik` discrepancy exceeds `reslik_max_disc`.
#'     This indicates the input is fundamentally invalid (e.g., sensor failure).
#'   \item \strong{DEFER}: Triggered if `TCS` consistency is below `tcs_consistency` OR
#'     `Agreement` is below `agreement`. This indicates valid but unstable or conflicting data.
#'   \item \strong{PROCEED}: Default state if no negative flags are raised.
#' }
#'
#' @param reslik List. The output from the \code{reslik()} function.
#' @param tcs List (Optional). The output from the \code{tcs()} function.
#' @param agreement List (Optional). The output from the \code{agreement()} function.
#' @param thresholds List. Custom thresholds to override defaults:
#'   \itemize{
#'     \item \code{reslik_max_disc} (default 3.0)
#'     \item \code{tcs_consistency} (default 0.2)
#'     \item \code{agreement} (default 0.3)
#'   }
#'
#' @return A character vector of signals (same length as input batch).
#'
#' @examples
#' # Mock Inputs
#' res_pass <- list(diagnostics = list(discrepancy = c(0.1), max_discrepancy = 0.1))
#' res_fail <- list(diagnostics = list(discrepancy = c(5.0), max_discrepancy = 5.0))
#' tcs_pass <- list(consistency = c(0.9))
#' tcs_fail <- list(consistency = c(0.1))
#'
#' # Scenario 1: All Good
#' rlcs_control(res_pass, tcs_pass)
#'
#' # Scenario 2: ResLik Fail -> ABSTAIN
#' rlcs_control(res_fail, tcs_pass)
#'
#' # Scenario 3: TCS Fail -> DEFER
#' rlcs_control(res_pass, tcs_fail)
#'
#' @export
rlcs_control <- function(reslik,
                         tcs = NULL,
                         agreement = NULL,
                         thresholds = list()) {
  
  # Defaults
  defaults <- list(
    reslik_max_disc = 3.0,
    tcs_consistency = 0.2,
    agreement = 0.3
  )
  
  # Merge thresholds
  th <- modifyList(defaults, thresholds) # modifyList is in utils, usually available. Or base R?
  # modifyList is in utils package, which is standard. But better safe to manual merge or check.
  # Let's manual merge for zero dependency (other than stats/base).
  for (n in names(thresholds)) {
    th[[n]] <- thresholds[[n]]
  }
  
  # Determine n from reslik discrepancy
  disc <- reslik$diagnostics$discrepancy
  n <- length(disc)
  
  # Initialize result
  decision <- rep("PROCEED", n)
  
  # 1. ResLik Check (Global/Batch level based on max_discrepancy as per prompt)
  # "reslik$diagnostics$max_discrepancy > 3.0 -> ABSTAIN"
  if (reslik$diagnostics$max_discrepancy > th$reslik_max_disc) {
    decision[] <- "ABSTAIN"
    return(decision)
  }
  
  # 2. TCS Check (Per sample)
  if (!is.null(tcs)) {
    # tcs$consistency < 0.2 -> DEFER
    mask_tcs <- tcs$consistency < th$tcs_consistency
    decision[mask_tcs] <- "DEFER"
  }
  
  # 3. Agreement Check (Per sample)
  # Only apply if not already ABSTAIN or DEFER?
  # "Conservative OR logic".
  # Usually DEFER overrides PROCEED. ABSTAIN overrides DEFER.
  # If TCS says DEFER, and Agreement says DEFER, it is DEFER.
  # If TCS says PROCEED, but Agreement says DEFER, it is DEFER.
  
  if (!is.null(agreement)) {
    mask_ag <- agreement$agreement < th$agreement
    # Apply DEFER where currently PROCEED.
    # If already DEFER (from TCS), stays DEFER.
    # If already ABSTAIN (from global), stays ABSTAIN (but we returned early for global).
    
    # Effectively: decision becomes DEFER if agreement is low
    decision[mask_ag] <- "DEFER"
  }
  
  decision
}