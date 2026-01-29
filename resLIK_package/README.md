# resLIK

Deterministic reliability sensors operating on latent representations. This package implements the ResLik, TCS, and Agreement sensors along with a deterministic control surface.

## Usage

### ResLik Sensor

```r
library(resLIK)
z <- matrix(rnorm(20), nrow=2)
out <- reslik(z, ref_mean=0, ref_sd=1)
print(out$gated)
print(out$diagnostics)
```

### Temporal Consistency Sensor

```r
z_t <- c(1, 0, 0)
z_prev <- c(0.9, 0.1, 0)
out <- tcs(z_t, z_prev)
print(out$consistency)
```

### Agreement Sensor

```r
z1 <- c(1, 0)
z2 <- c(0, 1)
out <- agreement(z1, z2)
print(out$agreement)
```

### Control Surface

```r
# Assuming 'res', 'tcs_out', 'ag_out' from above
decision <- rlcs_control(out, tcs=list(consistency=0.9), agreement=list(agreement=0.9))
print(decision)
```

## Note on Folder Name

The package name is `resLIK`. The source folder is named `resLIK_package` to avoid conflicts on case-insensitive filesystems with the existing `reslik` directory.