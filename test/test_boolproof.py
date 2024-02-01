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
from mathdonewrong.boolean_algebra import BoolExpr, Var
from mathdonewrong.boolproof import BoolProofDestructor, ComposedProof, OrAssociativity, OrCommutativity

def test_or_commutativity():
    a, b = Var('a'), Var('b')

    proof = OrCommutativity(a, b)

    assert proof.lhs == a | b
    assert proof.rhs == b | a

def test_or_associativity():
    a, b, c = Var('a'), Var('b'), Var('c')

    proof = OrAssociativity(a, b, c)

    assert proof.lhs == a | (b | c)
    assert proof.rhs == (a | b) | c

def test_can_compose_proofs():
    a, b, c = Var('a'), Var('b'), Var('c')

    proof1 = OrAssociativity(a, b, c)
    proof2 = OrCommutativity(a | b, c)

    proof = ComposedProof(proof1, proof2)

    assert proof.lhs == proof1.lhs
    assert proof.rhs == proof2.rhs

def test_cannot_compose_proofs_with_mismatched_lhs_and_rhs():
    a, b, c = Var('a'), Var('b'), Var('c')

    proof1 = OrAssociativity(a, b, c)
    proof2 = OrCommutativity(a, b)

    with pytest.raises(ValueError):
        ComposedProof(proof1, proof2)

class TestBoolProofDestructor(BoolProofDestructor):
    def or_associativity(self, a: BoolExpr, b: BoolExpr) -> None:
        pass

    def or_commutativity(self, a: BoolExpr, b: BoolExpr) -> None:
        pass

    def composed_proof(self, proof1: None, proof2: None) -> None:
        pass

def test_can_destruct_complex_proof():
    a, b, c = Var('a'), Var('b'), Var('c')

    proof1 = OrAssociativity(a, b, c)
    proof2 = OrCommutativity(a | b, c)

    proof = ComposedProof(proof1, proof2)

    destructor = TestBoolProofDestructor()

    proof.destruct(destructor)
