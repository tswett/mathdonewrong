# Copyright 2023 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from enum import Enum

from mathdonewrong.functions import ComposedPRFunction, primitive
from mathdonewrong.proofs import PREqualityAxiom

@primitive(bool)
def id_(x: bool) -> bool:
    return x

@primitive(bool)
def not_(x: bool) -> bool:
    return not x

not_not = ComposedPRFunction(not_, not_)

not_not_is_id = PREqualityAxiom(not_not, id_)

class MyBool(Enum):
    MyFalse = 0
    MyTrue = 1
