# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from dataclasses import dataclass

from mathdonewrong.expressions import Expression

@dataclass
class Operator:
    name: str

@dataclass
class Relation:
    lhs: Expression
    rhs: Expression

class Variety:
    operators: list[Operator]
    relations: list[Relation]

    def __init__(self):
        self.operators = []
        self.relations = []
