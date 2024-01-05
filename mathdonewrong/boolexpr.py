# Copyright 2023 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

class BoolExpr:
    pass

class Const:
    value: bool

    def __init__(self, value: bool):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f'Const({self.value})'

    def evaluate(self):
        return self.value

class And:
    left: BoolExpr
    right: BoolExpr

    def __init__(self, left: BoolExpr, right: BoolExpr):
        self.left = left
        self.right = right

    def __str__(self):
        return f'{self.left} & {self.right}'

    def __repr__(self):
        return f'And({self.left!r}, {self.right!r})'
