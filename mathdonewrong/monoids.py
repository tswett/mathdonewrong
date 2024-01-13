# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from __future__ import annotations
from functools import reduce

class Monoid:
    T: type

    @property
    def id(self) -> T:
        raise NotImplementedError

    def oper_(self, a: T, b: T) -> T:
        raise NotImplementedError

    def oper(self, *args: T) -> T:
        return reduce(self.oper_, args, self.id)

class CommutativeMonoid(Monoid):
    pass

class AdditiveMonoid(Monoid):
    def oper_(self, a: T, b: T) -> T:
        return a + b

class MultiplicativeMonoid(Monoid):
    def oper_(self, a: T, b: T) -> T:
        return a * b

class IntAddition(CommutativeMonoid, AdditiveMonoid):
    T = int

    @property
    def id(self) -> int:
        return 0

int_addition = IntAddition()

class IntMultiplication(CommutativeMonoid, MultiplicativeMonoid):
    T = int

    @property
    def id(self) -> int:
        return 1

int_multiplication = IntMultiplication()

class StringMonoid(AdditiveMonoid):
    T = str

    @property
    def id(self) -> str:
        return ''

string_monoid = StringMonoid()

class TupleMonoid(AdditiveMonoid):
    T = tuple

    @property
    def id(self) -> tuple:
        return ()

tuple_monoid = TupleMonoid()
