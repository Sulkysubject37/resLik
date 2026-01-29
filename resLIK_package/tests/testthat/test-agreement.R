test_that("agreement vector logic", {
  z1 <- c(1, 0)
  z2 <- c(1, 0)
  out <- agreement(z1, z2)
  expect_equal(out$agreement, 1)
})

test_that("agreement orthogonal", {
  z1 <- c(1, 0)
  z2 <- c(0, 1)
  out <- agreement(z1, z2)
  expect_lt(abs(out$agreement), 1e-6)
})

test_that("agreement matrix", {
  z1 <- matrix(c(1, 0, 0, 1), nrow=2, byrow=TRUE)
  z2 <- matrix(c(1, 0, 0, 1), nrow=2, byrow=TRUE)
  out <- agreement(z1, z2)
  expect_equal(out$agreement, c(1, 1))
})
