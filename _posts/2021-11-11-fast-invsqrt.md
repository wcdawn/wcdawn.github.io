---
layout: post
title: "Fast Inverse Square Root in Fortran"
date: 2021-11-11
categories: fortran
---

# Fast Inverse Square Root in Fortran

In the early days of computing, the square root operation was one of the slowest operations possible. As such, computer scientists and mathematicians worked hard to develop efficient algorithms to evaluate the square root.

Evaluating the square root is often necessary to normalize a vector. For example, we may want to calculate the direction between two coordinates, <img src="https://i.upmath.me/svg/%5Cmathbf%7Bx%7D%3D(x_1%2C%20x_2%2C%20x_3)" alt="\mathbf{x}=(x_1, x_2, x_3)" /> and <img src="https://i.upmath.me/svg/%5Cmathbf%7By%7D%3D(y_1%2C%20y_2%2C%20y_3)" alt="\mathbf{y}=(y_1, y_2, y_3)" />. Then, the direction between these two vectors, <img src="https://i.upmath.me/svg/%5Chat%7B%5Cmathbf%7Bd%7D%7D" alt="\hat{\mathbf{d}}" /> is

<img src="https://i.upmath.me/svg/%20%5Chat%7B%5Cmathbf%7Bd%7D%7D%20%3D%20%5Cfrac%7B((x_1-y_1)%2C(x_2-y_2)%2C(x_3-y_3))%7D%7B%5Csqrt%7B(x_1-y_1)%5E2%20%2B%20(x_2-y_2)%5E2%20%2B%20(x_3-y_3)%5E2%7D%7D.%20" alt=" \hat{\mathbf{d}} = \frac{((x_1-y_1),(x_2-y_2),(x_3-y_3))}{\sqrt{(x_1-y_1)^2 + (x_2-y_2)^2 + (x_3-y_3)^2}}. " />

We can define the inverse square root function as

<img src="https://i.upmath.me/svg/%20f(x)%20%3D%20%5Cfrac%7B1%7D%7B%5Csqrt%7Bx%7D%7D.%20" alt=" f(x) = \frac{1}{\sqrt{x}}. " />


Evaluating the inverse square root in a fast fashion is often important to video games and other graphics processing. The common method introduces an approximation and uses bit manipulation. An example implementation can be found in the "Quake III Arena" video game and more information can be found on [Wikipedia](https://en.wikipedia.org/wiki/Fast_inverse_square_root).

Bit manipulation is not as common in Fortran as it is in C but can be performed with clever use of the [`transfer`](https://gcc.gnu.org/onlinedocs/gfortran/TRANSFER.html) function. To investigate the efficient evaluation of the inverse square root function in Fortran, we will consider three possibilities:
1. Linking with a C function.
1. Using Fortran intrinsics and the `transfer` function.
1. Using the default `sqrt` function in Fortran.

## Linking with a C Program

The traditional form of the fast inverse square root algorithm is written in C to allow for simple bit manipulation. To use the algorithm in Fortran, one option is to call a C implementation of the algorithm using the Fortran 2003 standard C interface. This consists of a fair amount of boilerplate code.

First, the conventional fast inverse square root algorithm. This implementation uses a `union` to avoid undefined behavior in accordance with the C standard.

```c
/* fast_inv_sqrt.c */
float fast_inv_sqrt(float * x_in)
{
  const float x = *x_in;
  const float x2 = x*0.5F;

  union {
    float f;
    uint32_t i;
  } conv  = { .f = x };

  conv.i  = 0x5f3759df - ( conv.i >> 1 );
  conv.f  *= 1.5f - ( x2 * conv.f * conv.f );
  /* Optionally, include another Newton iteration. */
  return conv.f;
}
```

Next, we need a Fortran interface for the C function.

```f90
! mod_c_interface.f90
module c_interface
use, intrinsic :: ISO_C_BINDING, only : C_FLOAT
IMPLICIT NONE

interface

  real(C_FLOAT) function fast_inv_sqrt(x) bind(c)
    use, intrinsic :: ISO_C_BINDING, only : C_FLOAT
    real(C_FLOAT), intent(in) ::  x
  endfunction fast_inv_sqrt

endinterface

endmodule c_interface
```

Finally, we can call the C function from a Fortran program by `use`-ing the Fortran module containing the C interface.

```f90
! main.f90
program main
use, intrinsic :: ISO_C_BINDING, only : C_FLOAT
use c_interface
IMPLICIT NONE

real(C_FLOAT), parameter :: x = 2.0

write(*,*) fast_inv_sqrt(x)

endprogram main
```

Using the GCC compilers, these files can be compiled as follows.

```
gcc -ansi -O3 -Wall -Wextra -c fast_inv_sqrt.c
gfortran -std=f2003 -O3 -Wall -Wextra -o exec.x mod_c_interface.f90 main.f90 fast_inv_sqrt.o
```

## Using Fortran Intrinsics and `transfer`

Alternatively, we could use the `transfer` function to perform the necessary bit manipulation in Fortran without ever calling a C function. More information about `transfer` can be found in the GNU [documentation](https://gcc.gnu.org/onlinedocs/gfortran/TRANSFER.html).

First, we write the fast inverse square root algorithm in Fortran. `transfer` is used to perform the type punning and the bit-shift (i.e., `<<` in C) is replaced with a division operation (i.e., `/2`).

```f90
! f_fast_inf_sqrt.f90
real(4) function f_fast_inv_sqrt(x)
  IMPLICIT NONE
  real(4), intent(in) :: x

  real(4) :: x2, y
  integer(4) :: i

  x2 = x*5e-1
  y = x
  i = transfer(y, 1_4)
  i = 1597463007 - ( i / 2 )
  y = transfer(i, 1e0)
  y = y * (1.5e0 - (x2 * y**2))
  ! Optionally, include another Newton iteration.

  f_fast_inv_sqrt = y
  return
endfunction f_fast_inv_sqrt
```

Then, we write a simple Fortran program to call the Fortran implementation of the fast inverse square root function.

```f90
! main.f90
program main
IMPLICIT NONE

real(4), external :: f_fast_inv_sqrt
real(4), parameter :: x = 2.0

write(*,*) f_fast_inv_sqrt(x)
endprogram main
```

And using the `gfortran` compiler, this example can be compiled as follows.

```
gfortran -std=f2003 -O3 -Wall -Wextra -o exec.x f_fast_inv_sqrt.f90 main.f90
```

## Using `sqrt` Function

Finally, we could simply evaluate the inverse square root using the "slow" intrinsic `sqrt` function in Fortran. After all, how slow could it be?

```f90
f = 1.0/sqrt(x)
```

## Results

I have ran some simple timing tests to compare the three implementations above. The tests are very simple and simply call the function of interest one-billion times. Note: we have to be a bit clever here. I am a firm believer that if we want to compare these methods, we should compare the optimized executables (i.e., compare `-O3` rather than `-O0`). The problem is, the optimization can be **too** good. If we simply use the intrinsic `sqrt` function and evaluate it many times, the optimizer will replace it with a single evaluation. The code below is how I tested these methods.

```f90
program main
use timing ! some timing module providing tic and toc
use, intrinsic :: ISO_C_BINDING, only : C_FLOAT
IMPLICIT NONE

integer :: i
integer, parameter :: maxiter = 1000000000

real(C_FLOAT) :: xi
real(8) :: x

x = 0d0
call tic()
do i = 1,maxiter
  call random_number(xi)
  xi = xi + 1_C_FLOAT ! algorithm can perform poorly for zero
  x = x + 1.0/sqrt(xi)
enddo
call toc()

endprogram main
```

My hardware is an AMD Ryzen 9 3900X. Total runtime in seconds is in the table below.

| Method | Elapsed [s] |
| -------|-------------|
| C      | 5.057       |
| Fortran| 13.697      |
| Intrinsic| 4.050 |

## Conclusions

So what does any of this mean? I see two main conclusions.

First and most importantly, you should be using the intrinsic Fortran functions. Unless you have some very specialized application, they are typically going to be the fastest option available. In this case also, the fast inverse square root algorithm introduces approximation errors and this is avoided by using `sqrt`. As with most of software design, it is more important to have a working algorithm before we worry about runtime. Don't optimize too early. And if `sqrt` evaluation is restrictive on modern computers, you may need a new algorithm.

Second, bit manipulation is probably best left to C. Performing bit manipulation using `transfer` in Fortran is almost three-times slower than linking to a C function. If you need bit manipulation, it is probably better to use a language that supports it natively.
