# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

class TypeTree:
    as_tuple: tuple[type, ...]

class Zero(TypeTree):
    def __init__(self):
        self.as_tuple = ()

class Single(TypeTree):
    def __init__(self, t: type):
        self.as_tuple = (t,)

class Pair(TypeTree):
    def __init__(self, left: TypeTree, right: TypeTree):
        self.as_tuple = left.as_tuple + right.as_tuple

@dataclass
class TFunction:
    domain: TypeTree
    codomain: TypeTree
    func: Callable

    def __call__(self, *args):
        return self.func(*args)
