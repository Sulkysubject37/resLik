test_that("tcs vector logic", {
  z_prev <- c(1, 0)
  z_t <- c(1, 0)
  out <- tcs(z_t, z_prev)
  expect_equal(out$drift, 0)
  expect_equal(out$consistency, 1)
})

test_that("tcs matrix logic", {
  z_prev <- matrix(c(1, 0, 0, 1), nrow=2, byrow=TRUE)
  z_t <- matrix(c(1, 0, 0, 1), nrow=2, byrow=TRUE)
  out <- tcs(z_t, z_prev)
  expect_equal(out$drift, c(0, 0))
  expect_equal(out$consistency, c(1, 1))
})

test_that("tcs detects drift", {
  z_prev <- c(1, 0)
  z_t <- c(10, 0)
  out <- tcs(z_t, z_prev)
  expect_gt(out$drift, 0)
  expect_lt(out$consistency, 1)
})
