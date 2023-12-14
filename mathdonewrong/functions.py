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
from enum import EnumMeta

from mathdonewrong.types import PRType

class PRFunction(ABC):
    @property
    @abstractmethod
    def domain(self) -> PRType:
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

#class PrimitivePRFunction(PRFunction):
#    def __init__(self, domain, func):
#        self._domain = domain
#        self.func = func
#
#    @property
#    def domain(self) -> PRType:
#        return self._domain
#
#    def __call__(self, *args, **kwargs):
#        return self.func(*args, **kwargs)
#
#    def __repr__(self):
#        return f'PrimitivePRFunction({repr(self.func)})'

#def primitive(domain: PRType):
#    def decorator(func):
#        return PrimitivePRFunction(domain, func)
#
#    return decorator

class Compose(PRFunction):
    parts: tuple[PRFunction]

    def __init__(self, *parts):
        self.parts = parts

    @property
    def domain(self) -> PRType:
        return self.parts[0].domain

    def __call__(self, *args):
        for part in self.parts:
            args = (part(*args),)

        result, = args

        return result

    def __repr__(self):
        return f"Compose({', '.join(repr(part) for part in self.parts)})"

class Identity(PRFunction):
    _domain: PRType

    def __init__(self, domain: PRType):
        self._domain = domain

    @property
    def domain(self) -> PRType:
        return self._domain

    def __call__(self, x):
        return x

    def __repr__(self):
        return f'Identity({self.domain})'

class Const(PRFunction):
    _domain: PRType
    value: object

    def __init__(self, domain: PRType, value: object):
        self._domain = domain
        self.value = value

    @property
    def domain(self) -> PRType:
        return self._domain

    def __call__(self, x):
        return self.value

    def __repr__(self):
        return f'Const({self.domain}, {self.value})'

class MatchEnum(PRFunction):
    # note that the domain must be an enumerated type (instance of EnumMeta),
    # not a value of an enumerated type (instance of Enum)
    domain: EnumMeta
    codomain: PRType

    values: dict['domain', 'codomain']

    def __init__(self, domain: EnumMeta, codomain: PRType, values: dict['domain', 'codomain']):
        self._domain = domain
        self.codomain = codomain
        self.values = values

    @property
    def domain(self) -> EnumMeta:
        return self._domain

    def __call__(self, x: 'domain') -> 'codomain':
        return self.values[x]

    def __repr__(self):
        return f'MatchEnum({self.domain}, {self.codomain}, {self.values})'
