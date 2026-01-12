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

## 5. Not a Controller or Decision Engine
ResLik is a **control surface**, not a controller. It emits signals that describe the state of a representation, but it does not execute decisions (e.g., "stop," "abort," "reroute"). Any logic that acts upon ResLik signals must reside in external, system-level controllers.

## 6. Not a Policy Learner
ResLik does not learn "how to behave." It has no concept of rewards, goals, or objectives. It simply reports on the statistical consistency of the data it sees. It does not replace reinforcement learning or classical control policies.

## 7. Not Task-Specific or Domain-Bound
ResLik is a primitive for representation-level health. While initially validated on biological data, its mathematical core is agnostic to the semantic meaning of the features. It is equally applicable to robotics, audio processing, or finance, provided a valid reference distribution is available.

