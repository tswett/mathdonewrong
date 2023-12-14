# Copyright 2023 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from abc import ABC, abstractmethod

from mathdonewrong.types import PRType, to_prtype

class PRFunction(ABC):
    _domain: PRType

    @property
    def domain(self) -> PRType:
        return self._domain
    
    @domain.setter
    def domain(self, value):
        self._domain = to_prtype(value)

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

class Compose(PRFunction):
    parts: tuple[PRFunction]

    def __init__(self, *parts):
        self.parts = parts
        self.domain = parts[0].domain

    def __call__(self, *args):
        for part in self.parts:
            args = (part(*args),)

        result, = args

        return result

    def __repr__(self):
        return f"Compose({', '.join(repr(part) for part in self.parts)})"

class Identity(PRFunction):
    def __init__(self, domain: PRType):
        self.domain = domain

    def __call__(self, x):
        return x

    def __repr__(self):
        return f'Identity({self.domain})'

class Const(PRFunction):
    value: object

    def __init__(self, domain: PRType, value: object):
        self.domain = domain
        self.value = value

    def __call__(self, x):
        return self.value

    def __repr__(self):
        return f'Const({self.domain}, {self.value})'

class MatchEnum(PRFunction):
    codomain: PRType

    values: dict['domain', 'codomain']

    def __init__(self, domain: PRType, codomain: PRType, values: dict['domain', 'codomain']):
        self.domain = domain
        self.codomain = codomain
        self.values = values

    def __call__(self, x: 'domain') -> 'codomain':
        return self.values[x]

    def __repr__(self):
        return f'MatchEnum({self.domain}, {self.codomain}, {self.values})'
