# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

import dis
from dis import Instruction
from typing import Optional

from mathdonewrong.boolean_algebra import BoolExpr, Const, Var

def code_to_boolexpr(code) -> BoolExpr:
    return CodeWalker.code_to_boolexpr(code)

class CodeWalker:
    expr_stack: list[BoolExpr]
    result: Optional[BoolExpr]

    def __init__(self):
        self.expr_stack = []
        self.result = None

    @staticmethod
    def code_to_boolexpr(code) -> BoolExpr:
        walker = CodeWalker()

        for instruction in dis.get_instructions(code):
            walker.interpret(instruction)

        if walker.result is None:
            raise ValueError("This function doesn't seem to return a value.")

        return walker.result

    def interpret(self, instruction: Instruction):
        method = getattr(self, f'interpret_{instruction.opname}', None)
        if method is None:
            raise NotImplementedError(f"Could not convert this code because we don't know what to do with the {instruction.opname} instruction.")
        method(instruction)

    def interpret_RESUME(self, instruction: Instruction):
        pass

    def interpret_LOAD_CONST(self, instruction: Instruction):
        const = Const(instruction.argval)
        self.expr_stack.append(const)

    def interpret_LOAD_FAST(self, instruction: Instruction):
        var = Var(instruction.argval)
        self.expr_stack.append(var)

    def interpret_RETURN_VALUE(self, instruction: Instruction):
        self.result = self.expr_stack[-1]

    def interpret_BINARY_OP(self, instruction: Instruction):
        right = self.expr_stack.pop()
        left = self.expr_stack.pop()
        if instruction.argrepr == '&':
            self.expr_stack.append(left & right)
        elif instruction.argrepr == '|':
            self.expr_stack.append(left | right)
        else:
            raise NotImplementedError(f"Could not convert this code because we don't know what to do with the {instruction.argrepr} operation.")

    def interpret_UNARY_INVERT(self, instruction: Instruction):
        operand = self.expr_stack.pop()
        self.expr_stack.append(~operand)
