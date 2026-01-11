# What ResLik Is Not

To prevent misuse and manage expectations, we explicitly state what ResLik is **not** designed to do.

## 1. Not a Biological Discovery Engine
ResLik does not "discover" pathways or gene modules. If the gating mechanism highlights a set of genes, it simply means those genes were statistically unexpected relative to the reference. It does not imply they are the "drivers" of disease.

## 2. Not a Causal Inference Tool
The gating mechanism is correlational and statistical. It suppresses features that drift from the manifold. It cannot distinguish between a "compensatory" biological signal (which is unusual but necessary) and "technical artifact" (which is unusual and bad) without proper reference data.

## 3. Not a Full "Multi-Omics Integration" Framework
ResLik is a **unit**, not a framework. It does not handle data alignment, batch correction across modalities, or missing data imputation. It assumes aligned, numeric embeddings as input.

## 4. Not a Generative Model
ResLik is a discriminative representation refinement tool. It cannot generate new "healthy" samples from scratch.
