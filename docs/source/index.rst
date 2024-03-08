..
   Copyright 2024 Tanner Swett.
   
   This file is part of mathdonewrong. mathdonewrong is free software: you can
   redistribute it and/or modify it under the terms of version 3 of the GNU GPL
   as published by the Free Software Foundation.
   
   mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
   FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

Math done wrong!
================

This is "mathdonewrong," a somewhat silly attempt at doing formalized
mathematics in Python. You may be thinking that Python is not the right language
for doing formalized mathematics in—and that's the reason for the name.

The two fundamental classes are :class:`~mathdonewrong.expressions.Expression`
and :class:`~mathdonewrong.algebras.Algebra`.

An ``Expression`` is an expression tree, consisting of operators, literals, and
variables. Generally speaking, an expression, by itself, is meaningless. An
``Algebra`` is an object that provides meanings for expressions by implementing
their operators.

There are many subclasses of ``Algebra`` corresponding to various varieties and
instances of mathematical structures. For example,
:class:`~mathdonewrong.monoids.monoids.Monoid` is a subclass of ``Algebra`` which
describes the concept of a monoid (but doesn't provide any implementations), and
:class:`~mathdonewrong.monoids.monoids.IntAddition` and
:class:`~mathdonewrong.monoids.monoids.IntMultiplication` are subclasses of ``Monoid``
which actually represent particular monoids, and provide the appropriate
implementations.

There are a few modules which attempt to implement various particular kinds of
mathematical structures. In no particular order, some of these are:

- The :mod:`~mathdonewrong.monoids` module describes monoids and implements a
  few examples. It also contains an initial attempt at defining what a
  homomorphism is.
- The :mod:`~mathdonewrong.boolean_algebra` module describes Boolean algebras
  and provides an implementation of the standard Boolean algebra.
- The :mod:`~mathdonewrong.categories` and
  :mod:`~mathdonewrong.monoidal_categories` modules are an early-feeling attempt
  at defining categories.
- The :mod:`~mathdonewrong.lambda_calc` and
  :mod:`~mathdonewrong.primitive_recursive` modules define a couple of models of
  computation.

(sorry, I don't know how Sphinx works so this documentation looks pretty messed
up at the moment)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   stuff



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
