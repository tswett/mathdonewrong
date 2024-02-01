# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.monoidal_categories.monoidalexpr import Braid, Compose, Drop, Id, MonoidalExpr, Stack, Unit, Var

VarTree = str | None | tuple['VarTree', 'VarTree']

def vartree_to_expr(tree: VarTree) -> MonoidalExpr:
    if tree is None:
        return Unit()
    elif isinstance(tree, str):
        return Var(tree)
    else:
        left, right = tree
        return Stack(vartree_to_expr(left), vartree_to_expr(right))

def vartree_to_set(tree: VarTree) -> set[str]:
    if tree is None:
        return set()
    elif isinstance(tree, str):
        return {tree}
    else:
        left, right = tree
        return vartree_to_set(left) | vartree_to_set(right)

def make_braid(domain: VarTree, codomain: VarTree) -> MonoidalExpr:
    if domain == codomain:
        return Id(vartree_to_expr(domain))
    elif isinstance(domain, tuple) and isinstance(codomain, tuple):
        domain_l, domain_r = domain
        codomain_l, codomain_r = codomain

        if domain_l == codomain_r and domain_r == codomain_l:
            return Braid(vartree_to_expr(domain_l), vartree_to_expr(domain_r))
        elif vartree_to_set(domain_l) >= vartree_to_set(codomain_l) and vartree_to_set(domain_r) >= vartree_to_set(codomain_r):
            left = make_braid(domain_l, codomain_l)
            right = make_braid(domain_r, codomain_r)
            return Stack(left, right)
        elif vartree_to_set(domain_l) >= vartree_to_set(codomain_r) and vartree_to_set(domain_r) >= vartree_to_set(codomain_l):
            left = make_braid(domain_l, codomain_r)
            right = make_braid(domain_r, codomain_l)
            stack = Stack(left, right)
            swap = Braid(vartree_to_expr(codomain_r), vartree_to_expr(codomain_l))
            return Compose(stack, swap)

    raise NotImplementedError(f"I can't figure out how to make a braid from {domain} to {codomain} yet.")

    # Let me think about how to do this the smart way.
    #
    # First of all, domain must not contain any duplicate variables. If it
    # doesn't, we can proceed.
    #
    # If codomain is None, then of course I can always just do a Drop.
    #
    # If codomain is a single variable, then I need to search the domain for it.
    # It has to appear exactly once, and if it does, I can basically do a
    # sequence of Drops in order to obtain it.
    #
    # If codomain is a pair, then things are a little more complicated. The
    # easiest case is that the domain is also a pair, and I can get codomain_l
    # from domain_l and codomain_r from domain_r. Then I can do those two things
    # and Stack them.
    #
    # Another case that's almost as easy is if I can get codomain_l from
    # domain_r and codomain_r from domain_l. In that case, I can do as above and
    # then do a Braid afterwards.
    #
    # If neither of those is the case, then we have kind of a more complicated
    # situation. Let's start by assuming that we don't need to drop or
    # diagonalize any variables.
    #
    # In this case, there are potentially some variables that need to move from
    # the left to the right, and potentially some that need to move from the
    # right to the left. If both are the case, we can just do one move followed
    # by the other move. Otherwise, without loss of generality, assume that we
    # only need to move variables from the left to the right. In this case, we
    # can follow a 3-step process:
    #
    # 1. Gather the variables that need to move into codomain[0][1].
    # 2. Use associativity to move them all into codomain[1][0].
    # 3. Distribute them all to where they need to go.
    #
    # Whew, does that seem complicated yet? Let's go ahead and try to implement
    # everything piece by piece.
