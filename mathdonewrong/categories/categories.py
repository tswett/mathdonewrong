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

from mathdonewrong.algebras import Algebra

class Category(Algebra):
    def id(self, A: Ob):
        raise NotImplementedError

    def compose(self, f: Arr[A, B], g: Arr[B, C]) -> Arr[A, C]:
        raise NotImplementedError

    def domain(self, f: Arr) -> Ob:
        raise NotImplementedError
    
    def codomain(self, f: Arr) -> Ob:
        raise NotImplementedError
