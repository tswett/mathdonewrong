This is "mathdonewrong," a somewhat silly attempt at doing formalized
mathematics in Python.

The name of the project alludes to the fact that everything is done in a very
loose manner: there's no static typechecking and no overarching theory.

## Ideas behind this

There are two core concepts in mathdonewrong: _expressions_ and _algebras_.

An **expression** is a tree with three types of nodes: variables, literals, and
operators. An example of an expression may be

```python
Plus(Times(Var('x'), Literal(7)), Var('y'))
```

Above, `Plus` and `Times` are operators. An operator carries no meaningful
information besides its own name. As a result, an expression, considered alone,
is meaningless.

An **algebra** is a Python object which provides meaning to operators. For
example, a Python object with a `plus` method and a `times` method could be used
as an algebra for the above expression. If you define an algebra and name it
`alg`, then evaluating the above expression in that algebra will essentially
evaluate

```python
alg.plus(alg.times(x, 7), y)
```

Both expressions and algebras are duck typed. This means that the sole criterion
for an expression to be "valid" is that it can be evaluated in the desired
algebra, and the sole criterion for an algebra to be "valid" is that it can
evaluate the desired expression. Any animal that can quack is a duck, and any
sound that can be made by a duck is a quack.

## Installing and testing

This is a Poetry project, so you can install the dependencies and run the tests
in the usual way:

    poetry install
    poetry run pytest

There are no instructions for use, because there aren't actually any particular
intended use cases for any of this. The primary purpose of the libraries is to
satisfy the tests and the primary purpose of the tests is to motivate the
libraries.

## Legal information

Copyright 2024 Tanner Swett.

mathdonewrong is free software: you can redistribute it and/or modify it under
the terms of version 3 of the GNU GPL as published by the Free Software
Foundation.

mathdonewrong is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.
