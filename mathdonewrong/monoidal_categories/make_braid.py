# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.monoidal_categories.monoidalexpr import Braid, Drop, Id, MonoidalExpr, Stack, Unit, Var

VarTree = str | None | tuple['VarTree', 'VarTree']

def vartree_to_expr(tree: VarTree) -> MonoidalExpr:
    if tree is None:
        return Unit()
    elif isinstance(tree, str):
        return Var(tree)
    else:
        left, right = tree
        return Stack(vartree_to_expr(left), vartree_to_expr(right))

def make_braid(domain: VarTree, codomain: VarTree) -> MonoidalExpr:
    if domain == codomain:
        return Id(vartree_to_expr(domain))
    elif codomain is None:
        return Drop(vartree_to_expr(domain))
    elif isinstance(domain, tuple) and isinstance(codomain, tuple):
        domain_l, domain_r = domain
        codomain_l, codomain_r = codomain
        if domain_l == codomain_r and domain_r == codomain_l:
            return Braid(vartree_to_expr(domain_l), vartree_to_expr(domain_r))

    raise NotImplementedError(f"I can't figure out how to make a braid from {domain} to {codomain} yet.")
