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

from mathdonewrong.categories.categories import Category

class MonoidalCategory(Category):
    def stack(self, f: Arr[A, C], g: Arr[B, D]) -> Arr[A * B, C * D]:
        raise NotImplementedError

    def assoc_right(self, A: Ob, B: Ob, C: Ob) -> Arr[(A * B) * C, A * (B * C)]:
        raise NotImplementedError

    def assoc_left(self, A: Ob, B: Ob, C: Ob) -> Arr[A * (B * C), (A * B) * C]:
        raise NotImplementedError

    def unit(self) -> Ob:
        raise NotImplementedError

    def unit_left(self, A: Ob) -> Arr[A, Unit * A]:
        raise NotImplementedError

    def unit_right(self, A: Ob) -> Arr[A, A * Unit]:
        raise NotImplementedError

    def unit_left_inv(self, A: Ob) -> Arr[Unit * A, A]:
        raise NotImplementedError

    def unit_right_inv(self, A: Ob) -> Arr[A * Unit, A]:
        raise NotImplementedError

class BraidedMonoidalCategory(MonoidalCategory):
    def braid(self, A: Ob, B: Ob) -> Arr[A * B, B * A]:
        raise NotImplementedError

    def braid_inv(self, A: Ob, B: Ob) -> Arr[B * A, A * B]:
        raise NotImplementedError

class SymmetricMonoidalCategory(BraidedMonoidalCategory):
    def braid_inv(self, A: Ob, B: Ob) -> Arr[B * A, A * B]:
        return self.braid(B, A)

class CartesianMonoidalCategory(SymmetricMonoidalCategory):
    def drop(self, A: Ob) -> Arr[A, Unit]:
        raise NotImplementedError

    def diagonal(self, A: Ob) -> Arr[A, A * A]:
        raise NotImplementedError

class ClosedMonoidalCategory(MonoidalCategory):
    def into(self, A: Ob, f: Arr[B, C]) -> Arr[A >> B, A >> C]:
        raise NotImplementedError

    def curry(self, f: Arr[A * B, C]) -> Arr[A, B >> C]:
        raise NotImplementedError

    def curry_inv(self, f: Arr[A, B >> C]) -> Arr[A * B, C]:
        raise NotImplementedError

class CartesianClosedCategory(CartesianMonoidalCategory, ClosedMonoidalCategory):
    pass
