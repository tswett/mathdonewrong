# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from __future__ import annotations

class PyMonad:
    def map(self, func: Func[A, B]) -> Func[m[A], m[B]]:
        raise NotImplementedError
    
    def join(self, x: m[m[A]]) -> m[A]:
        raise NotImplementedError
    
    def pure(self, x: A) -> m[A]:
        raise NotImplementedError
    
    def compose(self, f: Func[A, m[B]], g: Func[B, m[C]]) -> Func[A, m[C]]:
        def compose_func(x: A):
            return self.join(self.map(g)(f(x)))
        
        return compose_func

    def bind(self, f: Func[A, m[B]]) -> Func[m[A], m[B]]:
        def bind_func(x: m[A]):
            y: m[m[B]] = self.map(f)(x)
            return self.join(y)

        return bind_func

    # TODO: write tests to motivate the Map, Join, Pure, Compose, and Bind operators
    def join_op(self) -> Func[m[m[A]], m[A]]:
        return self.join
    
    def pure_op(self) -> Func[A, m[A]]:
        return self.pure

class TupleMonad(PyMonad):
    def map(self, func):
        def map_func(tpl):
            return tuple(func(x) for x in tpl)

        return map_func

    def join(self, x):
        return tuple(inner for middle in x for inner in middle)

    def pure(self, x):
        return (x,)

class IdentityMonad(PyMonad):
    def map(self, func):
        return func

    def join(self, x):
        return x

    def pure(self, x):
        return x

class ReaderMonad(PyMonad):
    def __init__(self, context: type):
        pass

    def map(self, func: Func[A, B]) -> Func[Func[context, A], Func[context, B]]:
        def map_func(reader: Func[context, A]) -> Func[context, B]:
            def map_reader(ctx: context) -> B:
                return func(reader(ctx))
            
            return map_reader
        
        return map_func

    def join(self, reader: Func[context, Func[context, A]]) -> Func[context, A]:
        def join_reader(ctx: context) -> A:
            return reader(ctx)(ctx)
        
        return join_reader

    def pure(self, x: A) -> Func[context, A]:
        def pure_reader(ctx: context) -> A:
            return x
        
        return pure_reader
