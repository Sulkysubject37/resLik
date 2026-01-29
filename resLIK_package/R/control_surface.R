#' Deterministic Control Surface
#'
#' @param reslik Output from reslik()
#' @param tcs Output from tcs() (optional)
#' @param agreement Output from agreement() (optional)
#' @param thresholds List of thresholds
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
