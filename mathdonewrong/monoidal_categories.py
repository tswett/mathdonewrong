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
import inspect
from typing import Callable, TypeVar

A, B, C, D = TypeVar('A'), TypeVar('B'), TypeVar('C'), TypeVar('D')

class Category:
    Ob: type
    Arr: type

    def id(self, A: Ob) -> Arr:
        raise NotImplementedError

    def compose_(self, f: Arr[A, B], g: Arr[B, C]) -> Arr[A, C]:
        raise NotImplementedError

    def compose(self, *args: Arr) -> Arr:
        return reduce(self.compose_, args)

class MonoidalCategory(Category):
    @property
    def unit(self) -> Ob:
        raise NotImplementedError

    def tensor(self, A: Ob, B: Ob) -> Ob:
        raise NotImplementedError

    def tensor_arr(self, f: Arr[A, B], g: Arr[C, D]) -> Arr[tensor(A, C), tensor(B, D)]:
        raise NotImplementedError

    def associator(self, A: Ob, B: Ob, C: Ob) -> Arr[tensor(tensor(A, B), C), tensor(A, tensor(B, C))]:
        raise NotImplementedError

    def associator_inv(self, A: Ob, B: Ob, C: Ob) -> Arr[tensor(A, tensor(B, C)), tensor(tensor(A, B), C)]:
        raise NotImplementedError

    def left_unitor(self, A: Ob) -> Arr[tensor(unit, A), A]:
        raise NotImplementedError

    def left_unitor_inv(self, A: Ob) -> Arr[A, tensor(unit, A)]:
        raise NotImplementedError

    def right_unitor(self, A: Ob) -> Arr[tensor(A, unit), A]:
        raise NotImplementedError

    def right_unitor_inv(self, A: Ob) -> Arr[A, tensor(A, unit)]:
        raise NotImplementedError

class CategoryOfTupleTypes(MonoidalCategory):
    Ob = tuple[type, ...]
    Arr = Callable

    def id(self, A: Ob) -> Arr[A, A]:
        return lambda *args: args

    def compose_(self, f: Arr[A, B], g: Arr[B, C]) -> Arr[A, C]:
        return lambda *args: g(*f(*args))

    def tensor(self, A: Ob, B: Ob) -> Ob:
        return A + B

    def tensor_arr(self, f: Arr[A, B], g: Arr[C, D]) -> Arr[tensor(A, C), tensor(B, D)]:
        def inner(*args):
            f_arg_count = len(inspect.signature(f).parameters)
            return f(*args[:f_arg_count]) + g(*args[f_arg_count:])
        return inner

    def associator(self, A: Ob, B: Ob, C: Ob) -> Arr[tensor(tensor(A, B), C), tensor(A, tensor(B, C))]:
        return lambda *args: args

    def associator_inv(self, A: Ob, B: Ob, C: Ob) -> Arr[tensor(A, tensor(B, C)), tensor(tensor(A, B), C)]:
        return lambda *args: args

    def left_unitor(self, A: Ob) -> Arr[tensor(unit, A), A]:
        return lambda *args: args

    def left_unitor_inv(self, A: Ob) -> Arr[A, tensor(unit, A)]:
        return lambda *args: args

    def right_unitor(self, A: Ob) -> Arr[tensor(A, unit), A]:
        return lambda *args: args

    def right_unitor_inv(self, A: Ob) -> Arr[A, tensor(A, unit)]:
        return lambda *args: args
