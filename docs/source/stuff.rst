..
   Copyright 2024 Tanner Swett.
   
   This file is part of mathdonewrong. mathdonewrong is free software: you can
   redistribute it and/or modify it under the terms of version 3 of the GNU GPL
   as published by the Free Software Foundation.
   
   mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
   FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

Stuff
=====

I'm still trying to figure out how to use Sphinx for documentation, so here's a
page I've created in the course of figuring it out.

.. autosummary::
   :toctree: generated

   mathdonewrong.algebras
   mathdonewrong.boolean_algebra
   mathdonewrong.categories
   mathdonewrong.common
   mathdonewrong.equality
   mathdonewrong.expressions
   mathdonewrong.lambda_calc
   mathdonewrong.monoidal_categories
   mathdonewrong.monoids
   mathdonewrong.primitive_recursive
   mathdonewrong.pyfunctors
   mathdonewrong.python_exprs
   mathdonewrong.varieties

Information about some arbitrary things
=======================================

.. py:function:: mathdonewrong.monoids.monoids.int_scale(x: int) -> MonoidHomomorphism

   Create a monoid homomorphism :math:`\mathbb{Z} \to \mathbb{Z}` which maps
   each integer :math:`y` to :math:`xy`.

.. py:class:: mathdonewrong.algebras.Algebra

   I guess this is where I would put a description of the ``Algebra`` class.

common_opers because I don't know where to put this
===================================================

.. automodule:: mathdonewrong.common.common_opers
   :members:
   :undoc-members:
   :show-inheritance:

