# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

import pytest

from mathdonewrong.python_exprs.python_exprs import PyAttrL, PyNameL, source_expr_to_expr, source_module_to_expr

relation_def = '''
    @relation()
    def assoc(self, x, y, z):
        return self.mult(self.mult(x, y), z)
'''

def test_parse_an_expression():
    assert source_expr_to_expr('x') == PyNameL('x')
    assert source_expr_to_expr('self.mult') == PyAttrL(PyNameL('self'), 'mult')

def test_parse_a_relation_def():
    source_module_to_expr(relation_def)

if __name__ == '__main__':
    pytest.main([__file__])
