test_that("reslik preserves shape for vector", {
  z <- c(1, 2, 3)
  out <- reslik(z)
  expect_equal(length(out$gated), 3)
  expect_true(is.vector(out$gated))
})

test_that("reslik preserves shape for matrix", {
  z <- matrix(1:6, nrow = 2)
  out <- reslik(z)
  expect_equal(dim(out$gated), dim(z))
})

test_that("reslik is deterministic", {
  z <- matrix(rnorm(10), nrow=2)
  out1 <- reslik(z)
  out2 <- reslik(z)
  expect_equal(out1, out2)
})

test_that("reslik handles scalar parameters", {
  z <- c(10, 10, 10)
  # High z vs mean 0 -> high discrepancy -> gate close to 0
  out <- reslik(z, ref_mean=0, ref_sd=1)
  expect_true(all(abs(out$gated) < abs(z)))
})
