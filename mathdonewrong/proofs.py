# Copyright 2023 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from abc import ABC
from enum import EnumMeta

from mathdonewrong.functions import PRFunction
from mathdonewrong.types import PRType

class PREquality(ABC):
    """Conceptually, a PREquality is a proof in primitive recursive arithmetic that two PRFunctions are identical."""

    left: PRFunction
    right: PRFunction

class ByCases(PREquality):
    domain: PRType
    left: PRFunction
    right: PRFunction

    def __init__(self, left: PRFunction, right: PRFunction):
        assert left.domain == right.domain

        self.domain = left.domain
        self.left = left
        self.right = right

        assert isinstance(self.domain, PRType)

        self._check()

    def _check(self):
        for value in self.domain:
            assert self.left(value) == self.right(value)

    def __repr__(self):
        return f'ByCases({repr(self.left)}, {repr(self.right)})'
