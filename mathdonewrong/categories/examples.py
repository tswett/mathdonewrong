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
from typing import Any, TypeVar

from mathdonewrong.categories.categories import Category
from mathdonewrong.monoids.monoids import Monoid

A, B, C = TypeVar('A'), TypeVar('B'), TypeVar('C')

class MonoidToCategory(Category):
    def __init__(self, monoid: Monoid):
        self.monoid = monoid

    def id(self, _: Any) -> self.monoid.T:
        return self.monoid.id

    def compose(self, f: self.monoid.T, g: self.monoid.T) -> self.monoid.T:
        return self.monoid.oper(f, g)

class DictCategory(Category):
    def id(self, domain: list) -> dict:
        return {x: x for x in domain}

    def compose(self, f: dict[A, B], g: dict[B, C]) -> dict[A, C]:
        return {x: g[f[x]] for x in f}
