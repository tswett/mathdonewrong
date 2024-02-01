# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from typing import Callable, List, TypeVar
from mathdonewrong.monoidal_categories.categories import CartesianClosedCategory

A, B, C, D = TypeVar('A'), TypeVar('B'), TypeVar('C'), TypeVar('D')

Func = Callable[[A], B]

class CategoryOfUnaryFunctions(CartesianClosedCategory):
    def id(self, A: type):
        def id_func(x: A) -> A:
            return x

        return id_func

    def compose(self, f: Func[A, B], g: Func[B, C]) -> Func[A, C]:
        def composed_func(x: A) -> A:
            return g(f(x))

        return composed_func

    def stack(self, f: Func[A, C], g: Func[B, D]) -> Func[tuple[A, B], tuple[C, D]]:
        def stacked_func(t: tuple[A, B]) -> tuple[C, D]:
            x, y = t
            return f(x), g(y)

        return stacked_func

    def assoc_right(self, A: type, B: type, C: type) -> Func[tuple[tuple[A, B], C], tuple[A, tuple[B, C]]]:
        def assoc_right_func(t: tuple[tuple[A, B], C]) -> tuple[A, tuple[B, C]]:
            (x, y), z = t
            return x, (y, z)

        return assoc_right_func

    def assoc_left(self, A: type, B: type, C: type) -> Func[tuple[A, tuple[B, C]], tuple[tuple[A, B], C]]:
        def assoc_left_func(t: tuple[A, tuple[B, C]]) -> tuple[tuple[A, B], C]:
            x, (y, z) = t
            return (x, y), z

        return assoc_left_func

    def unit(self) -> type:
        return None

    def unit_left(self, A: type) -> Func[A, tuple[None, A]]:
        def unit_left_func(x: A) -> tuple[None, A]:
            return None, x

        return unit_left_func

    def unit_right(self, A: type) -> Func[A, tuple[A, None]]:
        def unit_right_func(x: A) -> tuple[A, None]:
            return x, None

        return unit_right_func

    def unit_left_inv(self, A: type) -> Func[tuple[None, A], A]:
        def unit_left_inv_func(t: tuple[None, A]) -> A:
            _, x = t
            return x

        return unit_left_inv_func

    def unit_right_inv(self, A: type) -> Func[tuple[A, None], A]:
        def unit_right_inv_func(t: tuple[A, None]) -> A:
            x, _ = t
            return x

        return unit_right_inv_func

    def braid(self, A: type, B: type) -> Func[tuple[A, B], tuple[B, A]]:
        def braid_func(t: tuple[A, B]) -> tuple[B, A]:
            x, y = t
            return y, x

        return braid_func

    def drop(self, A: type) -> Func[A, None]:
        def drop_func(x: A) -> None:
            return None

        return drop_func

    def diagonal(self, A: type) -> Func[A, tuple[A, A]]:
        def diagonal_func(x: A) -> tuple[A, A]:
            return x, x

        return diagonal_func

    def into(self, A: type, f: Func[B, C]) -> Func[Func[A, B], Func[A, C]]:
        def into_func(g: Func[A, B]) -> Func[A, C]:
            def composed_func(x: A) -> C:
                return f(g(x))

            return composed_func

        return into_func

    def curry(self, f: Func[tuple[A, B], C]) -> Func[A, Func[B, C]]:
        def curried_func(x: A) -> Func[B, C]:
            def partial_func(y: B) -> C:
                return f(x, y)

            return partial_func

        return curried_func

    def curry_inv(self, f: Func[A, Func[B, C]]) -> Func[tuple[A, B], C]:
        def uncurried_func(t: tuple[A, B]) -> C:
            x, y = t
            return f(x)(y)

        return uncurried_func
