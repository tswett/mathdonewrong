# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from dataclasses import dataclass
from typing import Callable
from mathdonewrong.monoidal_categories.categories import CartesianMonoidalCategory

TypeTree = type | tuple[()] | tuple['TypeTree', 'TypeTree']

def flatten(t: TypeTree) -> tuple[type, ...]:
    if isinstance(t, tuple):
        return tuple(ty for flat in map(flatten, t) for ty in flat)
    else:
        return (t,)

@dataclass
class TFunction:
    domain: TypeTree
    codomain: TypeTree
    func: Callable

    def __call__(self, *args):
        return self.func(*args)

def tfunction(domain: TypeTree, codomain: TypeTree) -> Callable[[Callable], TFunction]:
    def decorator(func: Callable) -> TFunction:
        return TFunction(domain, codomain, func)

    return decorator

class CategoryOfFunctions(CartesianMonoidalCategory):
    def id(self, A: TypeTree) -> TFunction:
        def func(*args):
            return args

        return TFunction(A, A, func)

    def compose(self, f: TFunction, g: TFunction) -> TFunction:
        def func(*args):
            return g(*f(*args))

        return TFunction(f.domain, g.codomain, func)

    def stack(self, f: TFunction, g: TFunction) -> TFunction:
        def func(*args):
            f_domain_length = len(flatten(f.domain))
            f_result = f(*args[:f_domain_length])
            g_result = g(*args[f_domain_length:])
            return f_result + g_result

        return TFunction((f.domain, g.domain), (f.codomain, g.codomain), func)

    def assoc_right(self, A: TypeTree, B: TypeTree, C: TypeTree) -> TFunction:
        def func(*args):
            return args

        return TFunction(((A, B), C), (A, (B, C)), func)

    def assoc_left(self, A: TypeTree, B: TypeTree, C: TypeTree) -> TFunction:
        def func(*args):
            return args

        return TFunction((A, (B, C)), ((A, B), C), func)

    def unit(self) -> TypeTree:
        return ()

    def unit_left(self, A: TypeTree) -> TFunction:
        def func(*args):
            return args

        return TFunction(A, ((), A), func)

    def unit_right(self, A: TypeTree) -> TFunction:
        def func(*args):
            return args

        return TFunction(A, (A, ()), func)

    def unit_left_inv(self, A: TypeTree) -> TFunction:
        def func(*args):
            return args

        return TFunction(((), A), A, func)

    def unit_right_inv(self, A: TypeTree) -> TFunction:
        def func(*args):
            return args

        return TFunction((A, ()), A, func)

    def braid(self, A: TypeTree, B: TypeTree) -> TFunction:
        def func(*args):
            A_length = len(flatten(A))
            return args[A_length:] + args[:A_length]

        return TFunction((A, B), (B, A), func)

    def braid_inv(self, A: TypeTree, B: TypeTree) -> TFunction:
        def func(*args):
            B_length = len(flatten(B))
            return args[B_length:] + args[:B_length]

        return TFunction((B, A), (A, B), func)

    def drop(self, A: TypeTree) -> TFunction:
        def func(*args):
            return ()

        return TFunction(A, (), func)

    def diagonal(self, A: TypeTree) -> TFunction:
        def func(*args):
            return args + args

        return TFunction(A, (A, A), func)
