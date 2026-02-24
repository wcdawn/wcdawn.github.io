---
layout: post
title: "Computing Gauss-Legendre Quadrature Weights and Abscissae in Arbitrary Precision"
date: 2021-08-30
categories: update
---

Well, it's been a while (over four years!) since I've posted on this thing. I suppose most of my writing these days is confined to emails and corporate memos.

In numerical solutions to the neutron transport equation (especially the SN form) it is often necessary to numerically evaluate integrals on the interval [-1,1]. An obvious choice of numerical quadrature for this integration is the Gauss-Legendre quadratrure series. The abscissae for the quadratures are the zeros of the Legendre polynomials and the weights can be described by a relationship between the abscissae and the derivatives of the Legendre polynomials.

One may readily find online pre-computed values for these Gauss-Legendre quadrature weights and abscissae. For an example, see [here](https://pomax.github.io/bezierinfo/legendre-gauss.html). Out of a personal curiosity, I wanted to try to compute these weights and abscissae with arbitrary precision.

My overall attempt was to use recursion relationships for the Legendre polynomials, the [`mpmath`](https://mpmath.org/) Python library, and a uniform grid on the unit interval with a bisection search to find zeros of the Legendre polynomials. You can see the GitHub repo with my attempt [here](https://github.com/wcdawn/one_dimensional_quadrature).

The attempt was (generally) successful, but fairly slow. I tested my results out to N = 16 and things worked as expected. However, the code was fairly slow. I expect that there must be a better way to compute the zeroes of the Legendre polynomials, but I know of none at the moment. If you have a suggestion for how to more efficiently compute the zeros of the Legendre polynomials than using a bisection search on a uniform grid, please get in touch with me.
