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
from mathdonewrong.functions import ComposedPRFunction, EnumMatchFunction, PRConstFunction, PRIdentity
from mathdonewrong.proofs import PREqualByExhaustion

MyFalse, MyTrue = MyBool.MyFalse, MyBool.MyTrue
match_not = EnumMatchFunction(MyBool, MyBool, {MyFalse: MyTrue, MyTrue: MyFalse})

def test_EnumMatchFunction():
    assert match_not(MyFalse) == MyTrue
    assert match_not(MyTrue) == MyFalse

not_not = ComposedPRFunction(match_not, match_not)

def test_not_not():
    assert not_not(MyFalse) == MyFalse
    assert not_not(MyTrue) == MyTrue

bool_id = PRIdentity(MyBool)

def test_bool_id():
    assert bool_id(MyFalse) == MyFalse
    assert bool_id(MyTrue) == MyTrue

const_false = PRConstFunction(MyBool, MyFalse)

def test_const_false():
    assert const_false(MyFalse) == MyFalse
    assert const_false(MyTrue) == MyFalse

def test_equality_by_exhaustion_successful():
    PREqualByExhaustion(not_not, bool_id)

def test_equality_by_exhaustion_failed():
    with pytest.raises(AssertionError):
        PREqualByExhaustion(bool_id, const_false)

if __name__ == '__main__':
    pytest.main([__file__])
