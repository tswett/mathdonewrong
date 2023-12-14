# Copyright 2023 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

import pytest

from mathdonewrong.functions import Compose, MatchEnum, Const, Identity
from mathdonewrong.proofs import ByCases

match_not = MatchEnum(bool, bool, {False: True, True: False})

def test_MatchEnum():
    assert match_not(False) == True
    assert match_not(True) == False

not_not = Compose(match_not, match_not)

def test_not_not():
    assert not_not(False) == False
    assert not_not(True) == True

bool_id = Identity(bool)

def test_bool_id():
    assert bool_id(False) == False
    assert bool_id(True) == True

const_false = Const(bool, False)

def test_const_false():
    assert const_false(False) == False
    assert const_false(True) == False

def test_ByCases_success():
    ByCases(not_not, bool_id)

def test_ByCases_failure():
    with pytest.raises(AssertionError):
        ByCases(bool_id, const_false)

if __name__ == '__main__':
    pytest.main([__file__])
