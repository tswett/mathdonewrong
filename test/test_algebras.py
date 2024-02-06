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

from mathdonewrong.algebras import Algebra, attr_name_to_operator_name, operator

def test_funcname_to_operator_name():
    assert attr_name_to_operator_name('my_favorite_operator') == 'MyFavoriteOperator'

class TestMagma(Algebra):
    @operator()
    def mult(self, x, y):
        raise NotImplementedError

def test_magma_variety_operators():
    oper, = TestMagma.variety.operators
    assert oper.name == 'Mult'

if __name__ == '__main__':
    pytest.main([__file__])
