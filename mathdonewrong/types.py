# Copyright 2023 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

type_to_prtype_dict = {}

def prtype_for(t: type):
    def decorator(cls):
        type_to_prtype_dict[t] = cls
        return cls
    return decorator

class PRType(type):
    pass

class Enum(PRType):
    values: list

    def __iter__(cls):
        return iter(cls.values)

@prtype_for(bool)
class Bool(metaclass=Enum):
    values = [False, True]

def to_prtype(t: object) -> PRType:
    if isinstance(t, PRType):
        return t
    elif t in type_to_prtype_dict:
        return type_to_prtype_dict[t]
    else:
        raise ValueError(f"Couldn't find a PRType for {t}")
