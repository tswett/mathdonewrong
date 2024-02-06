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
from dataclasses import dataclass
import re
from typing import Callable, Optional

import mathdonewrong.varieties as vty
from mathdonewrong.varieties import Variety

def attr_name_to_operator_name(attr_name):
    return attr_name.title().replace('_', '')

def operator_name_to_attr_name(operator_name):
    words = re.split('(?<=.)(?=[A-Z])', operator_name)
    return '_'.join(words).lower()

class AlgebraClass(type):
    members: dict[str, AlgebraMember]

    @classmethod
    def __prepare__(metacls, name, bases):
        return { 'members': {} }

class Algebra(metaclass=AlgebraClass):
    def operate(self, oper_name, operands):
        operator = self.get_operator(oper_name)

        if operator is None:
            raise NotImplementedError(f'operator {oper_name} not implemented in {self}')

        return operator(*operands)

    def get_operator(self, oper_name):
        if oper_name in self.members:
            attr_name = self.members[oper_name].attr_name
        else:
            attr_name = operator_name_to_attr_name(oper_name)

        operator = getattr(self, attr_name)

        return operator

class AlgebraMember:
    name: str
    func: Callable
    attr_name: Optional[str]

    def __init__(self, name, func):
        # TODO: set name automatically if it's None
        self.name = name
        self.func = func
        self.attr_name = None

    def __set_name__(self, owner, attr_name):
        self.attr_name = attr_name
        owner.members[self.name] = self

    def __get__(self, obj):
        raise NotImplementedError

class OperatorMember(AlgebraMember):
    pass

def operator(name=None):
    def operator_decorator(func):
        return OperatorMember(name, func)

    return operator_decorator

def relation():
    def relation_decorator(func):
        return func

    return relation_decorator
