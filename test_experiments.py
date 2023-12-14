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

from mathdonewrong.experiments import MyBool
from mathdonewrong.functions import Compose, MatchEnum, Const, Identity
from mathdonewrong.proofs import ByCases

MyFalse, MyTrue = MyBool.MyFalse, MyBool.MyTrue
match_not = MatchEnum(MyBool, MyBool, {MyFalse: MyTrue, MyTrue: MyFalse})

def test_MatchEnum():
    assert match_not(MyFalse) == MyTrue
    assert match_not(MyTrue) == MyFalse

not_not = Compose(match_not, match_not)

def test_not_not():
    assert not_not(MyFalse) == MyFalse
    assert not_not(MyTrue) == MyTrue

bool_id = Identity(MyBool)

def test_bool_id():
    assert bool_id(MyFalse) == MyFalse
    assert bool_id(MyTrue) == MyTrue

const_false = Const(MyBool, MyFalse)

def test_const_false():
    assert const_false(MyFalse) == MyFalse
    assert const_false(MyTrue) == MyFalse

def test_ByCases_success():
    ByCases(not_not, bool_id)

def test_ByCases_failure():
    with pytest.raises(AssertionError):
        ByCases(bool_id, const_false)

if __name__ == '__main__':
    pytest.main([__file__])
