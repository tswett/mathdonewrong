# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.monoidal_categories import CategoryOfTupleTypes

def test_CategoryOfTupleTypes():
    cat = CategoryOfTupleTypes()

    def f(x: int, y: int) -> tuple[int, str, float]:
        return (x, 'hello', y / 2)
    def g(x: int, y: str, z: float) -> tuple[str, float, int]:
        return (y + ' world', z * 3, x + len(y))

    id = cat.id((int, str, float))
    assert id(7, 'bagel', 3.5) == (7, 'bagel', 3.5)

    compose_f_g = cat.compose(f, g)
    assert compose_f_g(2, 3) == ('hello world', 4.5, 7)

    assert cat.tensor((int, int), (int, str, float)) == (int, int, int, str, float)

    tensor_f_g = cat.tensor_arr(f, g)
    assert tensor_f_g(8, 5, 10, 'kitten', 1.25) == (8, 'hello', 2.5, 'kitten world', 3.75, 16)

    assert cat.associator((int,), (str,), (float,))(1, 'hello', 3.5) == (1, 'hello', 3.5)
    assert cat.associator_inv((int,), (str,), (float,))(1, 'hello', 3.5) == (1, 'hello', 3.5)
    assert cat.left_unitor((int, str, float))(1, 'hello', 3.5) == (1, 'hello', 3.5)
    assert cat.left_unitor_inv((int, str, float))(1, 'hello', 3.5) == (1, 'hello', 3.5)
    assert cat.right_unitor((int, str, float))(1, 'hello', 3.5) == (1, 'hello', 3.5)
    assert cat.right_unitor_inv((int, str, float))(1, 'hello', 3.5) == (1, 'hello', 3.5)

    assert cat.braid((int, str), (float,))(1, 'hello', 3.5) == (3.5, 1, 'hello')
    assert cat.braid_inv((int, str), (float,))(3.5, 1, 'hello') == (1, 'hello', 3.5)
