# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

import textwrap
import pytest
from mathdonewrong.algebras import Algebra, operator
from mathdonewrong.expressions import Oper, Var
from mathdonewrong.python_exprs.depythonize import depythonize

from mathdonewrong.python_exprs.python_exprs import PyAttrL, PyBlock, PyCallL, PyFunctionDefL, PyNameL, PyReturn, source_expr_to_expr, source_block_to_expr

def test_parse_an_expression():
    assert source_expr_to_expr('x') == PyNameL('x')
    assert source_expr_to_expr('self.mult') == PyAttrL(PyNameL('self'), 'mult')
    assert source_expr_to_expr('f(x, y)') == PyCallL(PyNameL('f'), PyNameL('x'), PyNameL('y'))

def test_parse_a_block():
    assert source_block_to_expr('return x') == PyBlock(PyReturn(PyNameL('x')))

    assert source_block_to_expr('f(x)\nreturn x') == PyBlock(
        PyCallL(PyNameL('f'), PyNameL('x')),
        PyReturn(PyNameL('x'))
    )

    function_def = textwrap.dedent('''\
        def f(x):
            return x''')
    assert source_block_to_expr(function_def) == PyBlock(
        PyFunctionDefL(
            [],
            'f',
            [PyNameL('x')],
            [PyReturn(PyNameL('x'))]))

    decorated_function_def = textwrap.dedent('''\
        @deco
        def f(x):
            return x''')
    assert source_block_to_expr(decorated_function_def) == PyBlock(
        PyFunctionDefL(
            [PyNameL('deco')],
            'f',
            [PyNameL('x')],
            [PyReturn(PyNameL('x'))]))

relation_def = textwrap.dedent('''\
    @relation()
    def assoc(self, x, y, z):
        return self.mult(self.mult(x, y), z)''')

def test_parse_a_relation_def():
    assert source_block_to_expr(relation_def) == PyBlock(
        PyFunctionDefL(
            [PyCallL(PyNameL('relation'))],
            'assoc',
            [PyNameL('self'), PyNameL('x'), PyNameL('y'), PyNameL('z')],
            [PyReturn(
                PyCallL(
                    PyAttrL(PyNameL('self'), 'mult'),
                    PyCallL(
                        PyAttrL(PyNameL('self'), 'mult'),
                        PyNameL('x'),
                        PyNameL('y')),
                    PyNameL('z')))]))

def test_depythonize():
    expr = Oper('Mult', (Oper('Mult', (Var('x'), Var('y'))), Var('z')))
    assert depythonize(relation_def) == expr

class TestMonoid(Algebra):
    @operator('Multiply')
    def mult(self, a, b):
        raise NotImplementedError

def test_depythonize_with_algebra():
    expr = Oper('Multiply', (Oper('Multiply', (Var('x'), Var('y'))), Var('z')))
    assert depythonize(relation_def, TestMonoid) == expr

if __name__ == '__main__':
    pytest.main([__file__])
