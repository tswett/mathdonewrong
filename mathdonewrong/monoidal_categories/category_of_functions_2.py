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

A, B, C = TypeVar('A'), TypeVar('B'), TypeVar('C')

Func = Callable[[A], B]

class CategoryOfUnaryFunctions(CartesianClosedCategory):
    def id(self, A: type):
        def id_func(x: A):
            return x

        return id_func

    def compose(self, f: Func[A, B], g: Func[B, C]) -> Func[A, C]:
        def composed_func(x: A):
            return g(f(x))

        return composed_func
