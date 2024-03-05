# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.pyfunctors.monads import IdentityMonad, ReaderMonad, TupleMonad

def test_tuple_monad():
    mnd = TupleMonad()

    assert mnd.map(lambda x: x + 5)((1, 2, 3)) == (6, 7, 8)

    assert mnd.join((('a', 'p', 'p', 'l', 'e'), ('p', 'i', 'e'))) == ('a', 'p', 'p', 'l', 'e', 'p', 'i', 'e')

    assert mnd.pure('beep') == ('beep',)

    assert mnd.compose(lambda x: (x, x, x), lambda y: (y + 1, y + 2))(100) == (101, 102, 101, 102, 101, 102)

    assert mnd.bind(lambda x: (x * 10, x * 20, x * 30))((1, 2, 4)) == (10, 20, 30, 20, 40, 60, 40, 80, 120)

def test_identity_monad():
    mnd = IdentityMonad()

    assert mnd.map(lambda x: x + 5)(2) == 7

    assert mnd.join('hello') == 'hello'

    assert mnd.pure('boop') == 'boop'

    assert mnd.compose(lambda x: x * 2, lambda y: y + 1)(1200) == 2401

def test_reader_monad():
    mnd = ReaderMonad(int)

    assert mnd.map(lambda x: x + 5)(lambda ctx: ctx * 100)(20) == 2005

    assert mnd.join(lambda ctx1: lambda ctx2: ctx1 * 1000 + ctx2)(7) == 7007

    assert mnd.pure('zoop')(10) == 'zoop'

    def func1(x):
        return lambda ctx: f"The {x} number is {ctx}"
    
    def func2(y):
        return lambda ctx: f"{y}, which is to say the context is {ctx}"

    assert mnd.compose(func1, func2)("magic")(80) == "The magic number is 80, which is to say the context is 80"
