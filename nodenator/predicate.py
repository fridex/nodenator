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


from utils.helpers import dict2json


class Predicate(object):
    """
    Predicate representation - abstract class
    """

    def __init__(self):
        raise NotImplementedError("Abstract method not implemented")

    def __str__(self):
        raise NotImplementedError("Abstract method not implemented")

    def evaluate(self, message):
        raise NotImplementedError("Abstract method not implemented")

    @staticmethod
    def create(tree):
        raise NotImplementedError("Abstract method not implemented")

    def ast(self):
        raise NotImplementedError("Abstract method not implemented")

    def predicates_used(self):
        raise NotImplementedError("Abstract method not implemented")

    @staticmethod
    def construct(tree):
        """
        Construct predicate by its definition
        :param tree: dict representing predicate tree
        :type tree: dict
        :return: LeafPredicate or BuildinPredicate instance
        :rtype: LeafPredicate, BuildinPredicate
        """
        # We are doing it with recursive calls for now (top-down analysis)
        if 'name' in tree:
            return leafPredicate.LeafPredicate.create(tree['name'], tree.get('args'))
        elif 'or' in tree:
            return buildinPredicate.OrPredicate.create(tree['or'])
        elif 'not' in tree:
            return buildinPredicate.NotPredicate.create(tree['not'])
        elif 'and' in tree:
            return buildinPredicate.AndPredicate.create(tree['and'])
        else:
            raise ValueError("Unknown predicate:\n%s" % dict2json(tree))

# get rid of circular dependencies
import leafPredicate
import buildinPredicate
