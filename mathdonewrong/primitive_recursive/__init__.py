# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

"""
Primitive recursive arithmetic
==============================

This module contains a couple of definitions of primitive recursive functions.

The :mod:`~mathdonewrong.primitive_recursive.primrec_exprs` module is the oldest
one, and it will probably be deleted relatively soon.

I'm hoping that before long, I'll have a definition of the (logic-free) theory
of primitive recursive arithmetic, which will finally allow us to start proving
some substantial theorems. (In fact, in theory, that will allow us to start
proving *most* substantial theorems—primitive recursive arithmetic is powerful
enough to prove nearly any "ordinary" theorem that can be written as a
first-order statement about the integers.)

This module contains:

- :mod:`~mathdonewrong.primitive_recursive.primrec_exprs`: A simple definition
  of untyped primitive recursive functions over the natural numbers.
- :mod:`~mathdonewrong.primitive_recursive.primrec_exprs_typed`: A definition of
  statically typed primitive recursive functions.
- :mod:`~mathdonewrong.primitive_recursive.primrec_categorical`: The 2-category
  of primitive recursive types, functions, and equality proofs
"""
