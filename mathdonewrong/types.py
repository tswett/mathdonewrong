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

class PRType(type):
    """A primitive recursive type

    A PRType represents a "primitive recursive type". Conceptually, a primitive
    recursive type is a type where membership is decidable by a primitive
    recursive function.

    Some PRTypes are intended as representations of built-in Python types. This
    produces the rather ugly situation that these PRTypes are Python types, but
    aren't actually intended to be used as Python types.
    """

    underlying: type

    def __new__(cls, name, bases, namespace, *, underlying=None):
        result = super().__new__(cls, name, bases, namespace)

        if underlying is None:
            result.underlying = result
        else:
            result.underlying = underlying
            type_to_prtype_dict[underlying] = result

        return result

def to_prtype(t: object) -> PRType:
    if isinstance(t, PRType):
        return t
    elif t in type_to_prtype_dict:
        return type_to_prtype_dict[t]
    else:
        raise ValueError(f"Couldn't find a PRType for {t}")



class Enum(PRType):
    values: list

    def __iter__(cls):
        return iter(cls.values)



class Bool(metaclass=Enum, underlying=bool):
    values = [False, True]
