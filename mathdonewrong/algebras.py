# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from dataclasses import dataclass
from typing import Callable

import mathdonewrong.varieties as vty
from mathdonewrong.varieties import Variety

class AlgebraClass(type):
    operators: dict[str, Callable]

    def __new__(cls, name, bases, attrs):
        newclass = super().__new__(cls, name, bases, attrs)

        newclass.operators = {}

        for base in bases:
            if hasattr(base, 'operators'):
                newclass.operators.update(base.operators)

        return newclass

    def __init__(cls, name, bases, attrs):
        cls.variety = Variety()
        for key in cls.operators:
            cls.variety.operators.append(vty.Operator(key))

def funcname(operator_name):
    with_underscores = operator_name[0] + ''.join('_' + c if c.isupper() else c for c in operator_name[1:])
    return with_underscores.lower()

def attr_name_to_operator_name(funcname):
    next_uppercase = True
    result = ''

    for c in funcname:
        if c == '_':
            next_uppercase = True
            continue

        if next_uppercase and c.isalpha():
            c = c.upper()
            next_uppercase = False

        result += c

    return result

class Algebra(metaclass=AlgebraClass):
    def operate(self, operator, operands):
        if operator in type(self).operators:
            return getattr(self, type(self).operators[operator])(*operands)
        elif hasattr(self, funcname(operator)):
            return getattr(self, funcname(operator))(*operands)
        else:
            raise NotImplementedError(f'operator {operator} not implemented in {self}')

@dataclass
class Operator:
    name: str
    func: Callable

    def __set_name__(self, owner, attr_name):
        # TODO: we eventually want to store the Operator object here, not just
        # the attribute name
        if self.name is None:
            self.name = attr_name_to_operator_name(attr_name)
        owner.operators[self.name] = attr_name
        setattr(owner, attr_name, self.func)

def operator(name=None):
    def operator_decorator(func):
        return Operator(name, func)

    return operator_decorator
