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
from config import Config
from predicate import Predicate


class LeafPredicate(Predicate):
    """
    Leaf predicate - defined predicate
    """
    def __init__(self, predicate_func, args=None):
        """
        Constructor
        :param predicate_func: predicate function
        :param args: predicate arguments
        """
        self._func = predicate_func
        self._args = args if args is not None else {}

    def _args2str(self):
        """
        Convert arguments to string
        :return: string representation of arguments
        :rtype: str
        """
        ret = ""
        for k, v in self._args.iteritems():
            if len(ret) > 0:
                ret += ", "
            if isinstance(v, list):
                # s/'['foo']['bar']'/['foo']['bar']/ (get rid of leading ')
                ret += "%s=%s" % (k, str(v))
            elif isinstance(v, str):
                ret += "%s='%s'" % (k, v)
            else:
                # some build in type such as bool/long/...
                ret += "%s=%s" % (k, str(v))
        return ret

    def __str__(self):
        """
        A string representation of the predicate
        :return: string representation
        :rtype: str
        """
        return "%s(%s)" % (self._func.__name__, self._args2str())

    def ast(self):
        """
        Construct AST of predicate
        :return: AST of predicate
        :rtype: ast.Call
        """
        return ast.Call(func=ast.Name(id=self._func.__name__, ctx=ast.Load()),
                        args=[ast.Name(id='message', ctx=ast.Load())],
                        keywords=[ast.keyword(arg=k, value=ast.Str(s=v)) for k, v in self._args.iteritems()],
                        starargs=None, kwargs=None)

    def evaluate(self, message):
        """
        Evaluate message
        :param message: message that should be evaluated in predicate
        :type message: Message
        :return: True if predicate returned True, False otherwise
        :rtype: bool
        """
        ret = self._func(message, **self._args)

        logging.info("%s(%s) == %s" % (self._func.__name__, self._args2str(), str(ret)))

        if not isinstance(ret, bool):
            raise RuntimeError("Predicate should always return True/False")

        return ret

    def predicates_used(self):
        """
        Return predicates that are used
        :return: used predicates
        :rtype: function
        """
        return [self._func]

    @staticmethod
    def create(name, args):
        """
        Create a predicate based on its definition
        :param name: predicate name
        :type name: str
        :param args: predicate arguments (used as kwargs)
        :type args: dict
        :return: LeafPredicate instance
        :rtype: LeafPredicate
        """
        module = Config().predicate_module(name)
        return LeafPredicate(getattr(module, name), args)

