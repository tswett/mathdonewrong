# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.categories.examples import DictCategory, MonoidToCategory
from mathdonewrong.monoidlike.monoids import int_addition, int_multiplication, string_monoid

def test_MonoidToCategory():
    cat = MonoidToCategory(int_addition)
    assert cat.id(None) == 0
    assert cat.compose(2, 5) == 7

    cat = MonoidToCategory(int_multiplication)
    assert cat.id(None) == 1
    assert cat.compose(2, 5) == 10

    cat = MonoidToCategory(string_monoid)
    assert cat.id(None) == ''
    assert cat.compose('bike', 'shed') == 'bikeshed'

def test_DictCategory():
    cat = DictCategory()

    assert cat.id([]) == {}
    assert cat.id([1, 2, 3]) == {1: 1, 2: 2, 3: 3}
    assert list(cat.id([1, 2, 3])) == [1, 2, 3]

    d1 = {'a': 1, 'b': 2, 'c': 3}
    d2 = {1: 'one', 2: 'two', 3: 'three'}

    assert cat.compose(d1, d2) == {'a': 'one', 'b': 'two', 'c': 'three'}
    assert list(cat.compose(d1, d2)) == ['a', 'b', 'c']
