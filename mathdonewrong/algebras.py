# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from types import MethodType
from typing import Callable

class AlgebraClass(type):
    operators: dict[str, Callable]

    def __new__(cls, name, bases, attrs):
        newclass = super().__new__(cls, name, bases, attrs)

        newclass.operators = {}

        for base in bases:
            if hasattr(base, 'operators'):
                newclass.operators.update(base.operators)

        return newclass

class Algebra(metaclass=AlgebraClass):
    def operate(self, operator, operands):
        if operator in type(self).operators:
            return getattr(self, type(self).operators[operator])(*operands)
        elif hasattr(self, operator):
            return getattr(self, operator)(*operands)
        else:
            raise NotImplementedError(f'operator {operator} not implemented in {self}')

def implement(name):
    class Decorator:
        def __init__(self, func):
            self.func = func

        def __set_name__(self, owner, attr_name):
            owner.operators[name] = attr_name

    return Decorator
