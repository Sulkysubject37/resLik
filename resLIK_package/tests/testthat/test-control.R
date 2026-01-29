test_that("control surface defaults", {
  # Mock reslik output
  res <- list(diagnostics = list(max_discrepancy = 1.0, discrepancy = c(1.0, 1.0)))
  
  dec <- rlcs_control(res)
  expect_equal(dec, c("PROCEED", "PROCEED"))
})

test_that("control surface ABSTAIN on high discrepancy", {
  res <- list(diagnostics = list(max_discrepancy = 10.0, discrepancy = c(10.0, 10.0)))
  dec <- rlcs_control(res)
  expect_equal(dec, c("ABSTAIN", "ABSTAIN"))
})

test_that("control surface DEFER on low consistency", {
  res <- list(diagnostics = list(max_discrepancy = 1.0, discrepancy = c(1.0, 1.0)))
  tcs_out <- list(consistency = c(0.1, 0.9))
  
  dec <- rlcs_control(res, tcs = tcs_out)
  expect_equal(dec, c("DEFER", "PROCEED"))
})

test_that("control surface DEFER on low agreement", {
  res <- list(diagnostics = list(max_discrepancy = 1.0, discrepancy = c(1.0, 1.0)))
  ag_out <- list(agreement = c(0.1, 0.9))
  
  dec <- rlcs_control(res, agreement = ag_out)
  expect_equal(dec, c("DEFER", "PROCEED"))
})
