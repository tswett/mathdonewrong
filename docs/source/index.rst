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

This is "mathdonewrong," a collection of experiments in doing formalized
mathematics in Python.

At first blush, Python seems like the wrong tool for doing formal math (hence
the name of the project!). After all, Python has no proof-checking mechanisms,
or even a static typechecker, and the language itself is not designed for
expressing the sorts of things we want to be able to express.

However, this lack of any type of checking mechanism also gives us the freedom
to check our work in whatever way *we* want—or even to deliberately do things a
little bit wrong, in order to see what will happen.

Organization
------------

The modules are, in roughly descending order of importance:

- :mod:`~mathdonewrong.algebras`: The :class:`~mathdonewrong.algebras.Algebra`
  class, which represents algebraic structures (or *algebras* for short).
- :mod:`~mathdonewrong.expressions`: The
  :class:`~mathdonewrong.expressions.Expression` class, which represents
  expression trees. An ``Algebra`` is fundamentally nothing more than a
  collection of functions implementing the operations in an ``Expression``.
  These two classes are the foundation of everything else.
- :mod:`~mathdonewrong.monoidlike`: The definition of a monoid (the
  :class:`~mathdonewrong.monoidlike.monoids.Monoid` class), and a few examples and
  related concepts. As of this writing, monoids are the most fleshed-out type of
  algebraic structure.
- :mod:`~mathdonewrong.common`: Some common operator definitions which can be
  used for various different types of algebraic structures.
- :mod:`~mathdonewrong.equality`: Operations for manipulating equations and
  equality proofs.
- :mod:`~mathdonewrong.boolean_algebra`: Boolean algebras, including an
  implementation of the standard Boolean algebra.
- :mod:`~mathdonewrong.categories` and
  :mod:`~mathdonewrong.monoidal_categories`: An early-feeling attempt at
  defining categories.
- :mod:`~mathdonewrong.lambda_calc`: Lambda calculus.
- :mod:`~mathdonewrong.primitive_recursive`: Primitive recursive functions, and
  the theory of primitive recursive arithmetic.
- :mod:`~mathdonewrong.varieties`: Varieties of algebras—a particular formal
  definition of what a "type of algebraic structure" is.
- :mod:`~mathdonewrong.python_exprs`: Python expressions, represented as
  :class:`~mathdonewrong.expressions.Expression` objects.
- :mod:`~mathdonewrong.pyfunctors`: Functors and monads internal to Python. (The
  idea behind these is the same as the ``Functor`` and ``Monad`` typeclasses in
  Haskell.)
- :mod:`~mathdonewrong.code_to_boolexpr`,
  :mod:`~mathdonewrong.code_to_expression`,
  :mod:`~mathdonewrong.code_to_monoidal`: Various early attempts at
  automatically converting Python code into various kinds of expressions.

Fundamental classes
-------------------

The two fundamental classes are :class:`~mathdonewrong.expressions.Expression`
and :class:`~mathdonewrong.algebras.Algebra`.

An ``Expression`` is an expression tree, consisting of operators, literals, and
variables. Generally speaking, an expression, by itself, is meaningless. An
``Algebra`` is an object that provides meanings for expressions by implementing
their operators.

There are many subclasses of ``Algebra`` corresponding to various varieties and
instances of mathematical structures. For example,
:class:`~mathdonewrong.monoidlike.monoids.Monoid` is a subclass of ``Algebra`` which
describes the concept of a monoid (but doesn't provide any implementations), and
:class:`~mathdonewrong.monoidlike.monoids.IntAddition` and
:class:`~mathdonewrong.monoidlike.monoids.IntMultiplication` are subclasses of ``Monoid``
which actually represent particular monoids, and provide the appropriate
implementations.

Miscellaneous
-------------

Sorry—I don't know how Sphinx works so this documentation looks pretty messed up
at the moment.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   stuff



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
