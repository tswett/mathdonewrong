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
import inspect
import textwrap
from typing import Callable

from mathdonewrong.varieties import Operator, Relation, Variety

class AlgebraClass(type):
    operators: dict[str, AlgebraMember]

    @staticmethod
    def __prepare__(name, bases):
        member_dict = {}

        for base in bases[::-1]:
            if hasattr(base, 'members'):
                member_dict.update(base.members)

        return {'members': member_dict}

    def __init__(cls, name, bases, attrs):
        cls._variety = None

    def extract_expr(cls, attr_name):
        from mathdonewrong.python_exprs.depythonize import depythonize

        source = textwrap.dedent(inspect.getsource(getattr(cls, attr_name)))
        return depythonize(source)

    @property
    def variety(cls):
        if cls._variety is None:
            cls._variety = variety = Variety()

            for member in cls.members.values():
                if isinstance(member, AlgebraOperator):
                    operator = Operator(member.name)
                    variety.operators.append(operator)
                elif isinstance(member, AlgebraRelation):
                    lhs = cls.extract_expr(member.attr_name)
                    rhs = cls.extract_expr(member.attr_name + '_rhs')
                    relation = Relation(lhs, rhs)
                    variety.relations.append(relation)

        return cls._variety

def oper_name_to_attr_name(oper_name):
    with_underscores = oper_name[0] + ''.join('_' + c if c.isupper() else c for c in oper_name[1:])
    return with_underscores.lower()

def attr_name_to_oper_name(attr_name):
    return ''.join(word[:1].upper() + word[1:] for word in attr_name.split('_'))

class Algebra(metaclass=AlgebraClass):
    def operate(self, operator_name, operands):
        if (member := type(self).members.get(operator_name)) is not None:
            operator = getattr(self, member.attr_name)
        elif (operator := getattr(self, oper_name_to_attr_name(operator_name), None)) is not None:
            pass
        else:
            raise NotImplementedError(f"operator {operator_name} not implemented in {self}")

        return operator(*operands)

@dataclass
class AlgebraMember:
    name: str
    attr_name: str
    func: Callable

    def __set_name__(self, owner, attr_name):
        if self.name is None:
            self.name = attr_name_to_oper_name(attr_name)
        if self.attr_name is None:
            self.attr_name = attr_name

        owner.members[self.name] = self

        setattr(owner, attr_name, self.func)

class AlgebraOperator(AlgebraMember):
    pass

class AlgebraRelation(AlgebraMember):
    pass

def operator(name=None):
    def operator_decorator(func):
        return AlgebraOperator(name, None, func)

    return operator_decorator

def relation(name=None):
    def decorator(func):
        return AlgebraRelation(name, None, func)

    return decorator
