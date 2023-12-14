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
from enum import Enum, EnumMeta

class PRType(ABC):
    pass

class PRFunction(ABC):
    @property
    @abstractmethod
    def domain(self) -> PRType:
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

class PrimitivePRFunction(PRFunction):
    def __init__(self, domain, func):
        self._domain = domain
        self.func = func

    @property
    def domain(self) -> PRType:
        return self._domain

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __repr__(self):
        return f'PrimitivePRFunction({repr(self.func)})'

def primitive(domain: PRType):
    def decorator(func):
        return PrimitivePRFunction(domain, func)

    return decorator

class ComposedPRFunction(PRFunction):
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
        return f"ComposedPRFunction({', '.join(repr(part) for part in self.parts)})"

class PRIdentity(PRFunction):
    _domain: PRType

    def __init__(self, domain: PRType):
        self._domain = domain

    @property
    def domain(self) -> PRType:
        return self._domain

    def __call__(self, x):
        return x

    def __repr__(self):
        return f'PRIdentity({self.domain})'

class PRConstFunction(PRFunction):
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
        return f'PRConst({self.domain}, {self.value})'

@primitive(bool)
def id_(x: bool) -> bool:
    return x

@primitive(bool)
def not_(x: bool) -> bool:
    return not x

not_not = ComposedPRFunction(not_, not_)

class PREquality(ABC):
    """Conceptually, a PREquality is a proof in primitive recursive arithmetic that two PRFunctions are identical."""

    left: PRFunction
    right: PRFunction

class PREqualityAxiom(PREquality):
    def __init__(self, left: PRFunction, right: PRFunction):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f'PREqualityAxiom({repr(self.left)}, {repr(self.right)})'

class PREqualByExhaustion(PREquality):
    domain: EnumMeta
    left: PRFunction
    right: PRFunction

    def __init__(self, left: PRFunction, right: PRFunction):
        assert left.domain == right.domain

        self.domain = left.domain
        self.left = left
        self.right = right

        self._check()

    def _check(self):
        for value in self.domain:
            assert self.left(value) == self.right(value)

    def __repr__(self):
        return f'PREqualByExhaustion({repr(self.left)}, {repr(self.right)})'

not_not_is_id = PREqualityAxiom(not_not, id_)

class MyBool(Enum):
    MyFalse = 0
    MyTrue = 1

class EnumMatchFunction(PRFunction):
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
        return f'EnumMatchFunction({self.domain}, {self.codomain}, {self.values})'
