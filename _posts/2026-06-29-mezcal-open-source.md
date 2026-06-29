---
layout: post
title: "Open-Source of MEZCAL"
date: 2026-06-29
categories: update
---

I recently chose to open-source [MEZCAL](https://github.com/wcdawn/mezcal), the code that I wrote for my Ph.D. research. The code solves the neutron transport equation on unstructured mesh using the Self-Adjoint Angular Flux (SAAF) form. The numerical backbone of MEZCAL is the [MFEM](https://mfem.org/) finite element framework.

The development of MEZCAL was funded by the [Exascale Computing Project](https://www.exascaleproject.org/) (ECP). As such, the original emphasis was on massively parallel computing with GPUs. Specifically, MEZCAL was designed to run on [Summit](https://en.wikipedia.org/wiki/Summit_(supercomputer)) on NVIDIA A100s. Fun fact: at the time of development, MEZCAL was running on Summit which was the largest computer in the world according to [Top500](https://top500.org/lists/top500/2019/11/).

The methodology of MEZCAL is documented in my [dissertation](https://www.lib.ncsu.edu/resolver/1840.20/39687) and in a [journal article](https://doi.org/10.1080/00295639.2023.2189510). Much of the research was dedicated to developing a performant eigensolver for exascale computing architectures. Ultimately, I concluded that using power iterations with Diffusion Synthetic Acceleration (DSA) was preferable to using a Generalized Davidson method as it required less memory. The amount of available memory can be quite limiting on GPUs.

Part of my reluctance to open-source MEZCAL is that I think it is not some of my best software development work. The code was developed so that I could graduate, not so that I could write elegant code. I expect that the code style (and the heavy use of C-style functions) may reflect this development style.

Finally, I would be remiss if I didn't discuss the choice of SAAF. In short, I started the project with MFEM and wanted to run efficiently on GPUs, so I ended up with continuous finite elements. Once I had chosen continuous finite elements, SAAF seemed like a natural choice. In retrospect, I wish that I had done things differently. SAFF is extremely inefficiently computationally. By going to a second-order angular formulation, extremely high-order angular quadratures are necessary to resolve the angular dependence of neutron streaming. That means that the number of Degrees Of Freedom (DOF) grows extremely rapidly to solve even reasonably small problems. SAAF did serve its purpose for this work, but for most practical calculations, it requires too many resources to be practical.
