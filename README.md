# Signal Reconstruction using DFT.

## Goal

Given the Discrete Fourier Transform of a signal like the following, 

![DFT of signal] (assets/DFT.png)

is it possible to reconstruct the signal, modelled using the following Double Fourier Series,
```math
\sum_{m}\sum_{n} b_{mn}\sin\left( m\omega x \right)\sin\left( n\omega x \right)
```
given the sampling rate?

In simpler words, can we comment about $b_{mn}, m$ and $n$, which make up the signal?
