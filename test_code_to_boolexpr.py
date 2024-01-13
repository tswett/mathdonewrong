# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.boolexpr import And, F, Not, Or, T, Var
from mathdonewrong.code_to_boolexpr import code_to_boolexpr

def test_from_code_constant():
    assert code_to_boolexpr(lambda x, y: True) == T
    assert code_to_boolexpr(lambda x, y: False) == F
