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
from typing import Optional
from mathdonewrong.algebras import Algebra, AlgebraClass, attr_name_to_oper_name
from mathdonewrong.expressions import Expression, Oper, Var
from mathdonewrong.python_exprs.python_exprs import PythonExpr, source_block_to_expr

class DepythonAlgebra(Algebra):
    def py_name(self, name):
        return Name(name)

    def py_args(self, *args):
        return args

    def py_call(self, target, args):
        return Call(target, args)

    def py_decorators(self, *decorators):
        pass

    def py_attr(self, target, attr_name):
        return Attr(target, attr_name)

    def py_return(self, value):
        return value

    def py_block(self, *statements):
        return Block(statements)

    def py_function_def(self, decorators, name, args, body):
        return FunctionDef(decorators, name, args, body)

@dataclass
class Context:
    algebra_class: AlgebraClass

@dataclass
class Name:
    name: str

    def to_expression(self, context: Context):
        return Var(self.name)

@dataclass
class Call:
    target: PythonExpr
    args: list

    def to_expression(self, context: Context):
        if (alg_cls := context.algebra_class) is not None:
            oper_name = alg_cls.attr_name_to_oper_name(self.target.attr_name)
        else:
            oper_name = attr_name_to_oper_name(self.target.attr_name)

        operands = [arg.to_expression(context) for arg in self.args]
        return Oper(oper_name, operands)

@dataclass
class Attr:
    target: PythonExpr
    attr_name: str

@dataclass
class Block:
    statements: list

    def to_expression(self, context: Context):
        function_def, = self.statements
        return_value, = function_def.body.statements
        return return_value.to_expression(context)

@dataclass
class FunctionDef:
    decorators: list
    name: str
    args: list
    body: list

# TODO: Defining depythonize as an algebra is probably a bad idea, because
# depythonize gets used when we're defining algebra classes. It would probably
# be just as easy to just define it as a NodeVisitor.
def depythonize(source_block: str, algebra_class: Optional[AlgebraClass] = None) -> Expression:
    expr = source_block_to_expr(source_block)
    destructed_block = expr.evaluate_in(DepythonAlgebra(), {})

    context = Context(algebra_class)
    return destructed_block.to_expression(context)
