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
from mathdonewrong.code_to_monoidal import MonoidalExprWithContext, expressionize_m
from mathdonewrong.monoidal_categories.category_of_functions import CategoryOfUnaryFunctions

pytest.skip(allow_module_level=True)

cat = CategoryOfUnaryFunctions()

def test_make_adjustment_from_x_to_x():
    adjustment = MonoidalExprWithContext.make_adjustment(('x',), ('x',))

    func = adjustment.evaluate_in(cat, {'x': None})
    assert func('red') == 'red'

def test_make_adjustment_from_y_to_y():
    adjustment = MonoidalExprWithContext.make_adjustment(('y',), ('y',))

    func = adjustment.evaluate_in(cat, {'y': None})
    assert func('blue') == 'blue'

def test_make_adjustment_from_nothing_to_nothing():
    adjustment = MonoidalExprWithContext.make_adjustment((), ())

    func = adjustment.evaluate_in(cat, {})
    assert func(None) == None

def test_make_adjustment_from_nothing_to_x():
    adjustment = MonoidalExprWithContext.make_adjustment((), ('x',))

    func = adjustment.evaluate_in(cat, {'x': 'whatever'})
    assert func('green') == None

def test_make_adjustment_from_x_to_x_y():
    adjustment = MonoidalExprWithContext.make_adjustment(('x',), ('x', 'y'))

    func = adjustment.evaluate_in(cat, {'x': None})
    assert func(('orange', 'purple')) == 'orange'

def text_make_adjustment_from_x_to_x_x_error():
    with pytest.raises(ValueError):
        MonoidalExprWithContext.make_adjustment(('x',), ('x', 'x'))

def test_make_adjustment_from_x_x_to_x_error():
    with pytest.raises(ValueError):
        MonoidalExprWithContext.make_adjustment(('x', 'x'), ('x',))

def test_make_adjustment_from_x_y_to_x_error():
    with pytest.raises(ValueError):
        MonoidalExprWithContext.make_adjustment(('x', 'y'), ('x',))

@expressionize_m
def t_id(x):
    return x

def test_expressionize_m_id():
    func = t_id.expression.evaluate_in(cat, {})
    assert func(84) == 84
    assert func('yellow') == 'yellow'

@expressionize_m
def t_x_y_take_x(x, y):
    return x

@expressionize_m
def t_x_y_take_y(x, y):
    return y

@expressionize_m
def t_y_x_take_x(y, x):
    return x

@expressionize_m
def t_y_x_take_y(y, x):
    return y

def test_expressionize_m_take():
    for input_func in [t_x_y_take_x, t_x_y_take_y, t_y_x_take_x, t_y_x_take_y]:
        func = input_func.expression.evaluate_in(cat, {})
        assert func(('red', 'yellow')) == input_func('red', 'yellow')

if __name__ == '__main__':
    pytest.main([__file__])
