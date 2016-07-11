#!/bin/env python
# -*- coding: utf-8 -*-
# ####################################################################
# Copyright (C) 2016  Fridolin Pokorny, fpokorny@redhat.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# ####################################################################


import ast
import logging
from predicate import Predicate


class BuildinPredicate(Predicate):
    """
    Abstract build in predicate representation
    """
    pass


class NaryPredicate(BuildinPredicate):
    """
    Abstract n-ary build in predicate representation
    """
    def __init__(self, children):
        self._children = children

    def _str(self, op):
        ret = ""
        for child in self._children:
            if len(ret) > 0:
                ret += " %s " % op
            ret += str(child)

        if len(self._children) > 1:
            ret = "(" + ret + ")"

        return ret

    def src_defined(self):
        ret = ""
        for child in self._children:
            ret += child.src_defined()
            ret += "\n\n"
        return ret

    @staticmethod
    def _create(tree, cls):
        if not isinstance(tree, list):
            raise ValueError("Nary logical operators expect list of children")
        children = []
        for child in tree:
            children.append(Predicate.construct(child))
        return cls(children)

    def predicates_used(self):
        return reduce(lambda x, y: x + y.predicates_used(), self._children, [])


class UnaryPredicate(BuildinPredicate):
    """
    Abstract unary build in predicate representation
    """
    def __init__(self, child):
        self._child = child

    def src_defined(self):
        return self._child.src_defined()

    @staticmethod
    def _create(tree, cls):
        if isinstance(tree, list):
            raise ValueError("Unary logical operators expect one child")
        return cls(Predicate.construct(tree))

    def predicates_used(self):
        return self._child.predicates_used()


class AndPredicate(NaryPredicate):
    """
    Build in n-ary logical AND
    """
    def __str__(self):
        """
        String representation
        :return: string representation
        :rtype: str
        """
        return "(" + reduce(lambda x, y: str(x) + ' and ' + str(y), self._children) + ")"

    def ast(self):
        """
        AST of the predicate
        :return: AST representation of the predicate
        :rtype: ast.BoolOp
        """
        return ast.BoolOp(ast.And(), [ast.Expr(value=x.ast()) for x in self._children])

    @staticmethod
    def create(tree):
        """
        Create predicate by its definition
        :param tree: tree-like predicate representation of a predicate using dict
        :type tree: dict
        :return: predicate instance
        :rtype: AndPredicate
        """
        return NaryPredicate._create(tree, AndPredicate)

    def evaluate(self, message):
        """
        True if all child predicates are True for given message
        :param message: message to evaluate predicates on
        :return: True if all predicates returned True, False otherwise
        :rtype: bool
        """
        # since we are simulating Python code evaluation, we want to simulate short circuit evaluation
        logging.info("and:")
        for predicate in self._children:
            if not predicate.evaluate(message):
                return False
        return True


class OrPredicate(NaryPredicate):
    def __str__(self):
        """
        String representation
        :return: string representation
        :rtype: str
        """
        return "(" + reduce(lambda x, y: str(x) + ' or ' + str(y), self._children) + ")"

    def ast(self):
        """
        AST of the predicate
        :return: AST representation of the predicate
        :rtype: ast.BoolOp
        """
        return ast.BoolOp(ast.Or(), [ast.Expr(value=x.ast()) for x in self._children])

    @staticmethod
    def create(tree):
        """
        Create predicate by its definition
        :param tree: tree-like predicate representation of a predicate using dict
        :type tree: dict
        :return: predicate instance
        :rtype: OrPredicate
        """
        return NaryPredicate._create(tree, OrPredicate)

    def evaluate(self, message):
        """
        True if at least one child predicate is True for given message
        :param message: message to evaluate predicates on
        :return: True if at least one predicate returned True, False otherwise
        :rtype: bool
        """
        # since we are simulating Python code evaluation, we want to simulate short circuit evaluation
        logging.info("or:")
        for predicate in self._children:
            if predicate.evaluate(message):
                return True
        return False


class NotPredicate(UnaryPredicate):
    """
    Build in n-ary logical NOT
    """
    def __str__(self):
        """
        String representation
        :return: string representation
        :rtype: str
        """
        return "(not %s)" % str(self._child)

    def ast(self):
        """
        AST of the predicate
        :return: AST representation of the predicate
        :rtype: ast.UnaryOp
        """
        return ast.UnaryOp(ast.Not(), ast.Expr(value=self._child.ast()))

    @staticmethod
    def create(tree):
        """
        Create predicate by its definition
        :param tree: tree-like predicate representation of a predicate using dict
        :type tree: dict
        :return: predicate instance
        :rtype: NotPredicate
        """
        return UnaryPredicate._create(tree, NotPredicate)

    def evaluate(self, message):
        """
        True child predicate returned False
        :param message: message to evaluate predicates on
        :return: True if child predicate returned False, True otherwise
        :rtype: bool
        """
        logging.info("not:")
        return not self._child.evaluate(message)
