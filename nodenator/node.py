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


class Node(object):
    """
    Node representation
    """
    def __init__(self, name, input_condition=None, output_condition=None, description=None,
                 input_edges=None, output_edges=None, srcpath=None, dump_node_comparison = None):
        """
        Constructor
        :param name: node name, has to be unique in the system
        :param input_condition: input condition for the node
        :param output_condition: output condition for the node
        :param description: node description
        :param input_edges: node input edges
        :param output_edges: node output edges
        :param srcpath: path to source file when dump is perfomed
        :param dump_node_comparison: distinguish node comparison when for dump (test for source node)
        """
        assert(name is not None)

        self._name = name
        self._input_condition = input_condition
        self._output_condition = output_condition
        self._description = description
        self._input_edges = input_edges if input_edges is not None else []
        self._output_edges = output_edges if output_edges is not None else []
        self._srcpath = srcpath

        if dump_node_comparison is not None:
            if not dump_node_comparison.get('type'):
                raise ValueError("dump-node-comparison expects type")

            if dump_node_comparison['type'] not in ('name', 'instance'):
                raise ValueError("dump-node-comparison should be one of %s" % str(('name', 'instance')))

            if dump_node_comparison['type'] == 'instance' and not dump_node_comparison.get('import'):
                raise ValueError("import dump-node-comparison expects import definition")
        self._dump_node_comparison = dump_node_comparison

    def name(self):
        """
        Get node name
        :return: node name
        :rtype: str
        """
        return self._name if self._name is not None else id(self)

    def ast_comparison(self, ast_body, orelse=None):
        """
        Return AST for comparison
        :param ast_body: body that should be used in IF branch
        :type ast_body: ast.Module
        :param orelse: body that should be used in ELSE branch
        :type orelse: ast.Module
        :return: AST for node comparison
        :rtype: ast.If
        """
        if not isinstance(ast_body, list):
            ast_body = [ast_body]

        if orelse is None:
            orelse = []

        if not isinstance(orelse, list):
            orelse = [orelse]

        if self._dump_node_comparison is None or self._dump_node_comparison.get('type') == 'name':
            condition = ast.Compare(left=ast.Name(id='node_from', ctx=ast.Load()), ops=[ast.Eq()],
                                    comparators=[ast.Str(s=self._name)])
        elif self._dump_node_comparison.get('type') == 'instance':
            condition = ast.Call(func=ast.Name(id='isinstance', ctx=ast.Load()),
                                 args=[ast.Name(id='node_from', ctx=ast.Load()),
                                       ast.Name(id=self._name, ctx=ast.Load())],
                                 keywords=[], starargs=None, kwargs=None)
        else:
            raise NotImplementedError("Unhandled case")

        return ast.If(test=condition, body=ast_body, orelse=orelse)

    def dump_node_comparison_instance(self):
        """
        Distinguish whether node should be distinguished by its instance
        :return: import path of Node if defined
        :rtype: None or str
        """
        if self._dump_node_comparison is not None:
            if self._dump_node_comparison.get('type') == 'instance':
                return self._dump_node_comparison.get('import')
        return None

    def dump_node_comparison_name(self):
        """
        Distinguish whether node should be distinguished by its name
        :return: True if node is distinguished by its name
        :rtype: bool
        """
        return self._dump_node_comparison is None or self._dump_node_comparison.get('type') == 'name'

    def description(self):
        """
        Get node description
        :return: node description
        :rtype: str
        """
        return self._description

    def srcpath(self):
        """
        Return source path to node when doing dump
        :return: source path
        :rtype: str
        """
        return self._srcpath

    def add_input_edge(self, edge):
        """
        Add input edge
        :param edge: edge that is treated as an input edge
        :type edge: Edge
        :return: None
        """
        self._input_edges.append(edge)

    def add_output_edge(self, edge):
        """
        Add output edge
        :param edge: edge that is treated as an output edge
        :type edge: Edge
        :return: None
        """
        self._output_edges.append(edge)

    def input_edges(self):
        """
        Get all input edges of node
        :return: input edges
        :rtype: list(Edge)
        """
        return self._input_edges

    def output_edges(self):
        """
        Get all output edges of node
        :return: output edges
        :rtype: list(Edge)
        """
        return self._output_edges

    def input_condition(self):
        """
        Input condition restriction for node
        :return: input condition restriction
        :rtype: Predicate
        """
        return self._input_condition

    def output_condition(self):
        """
        Output condition restriction for node
        :return: output condition restriction
        :rtype: Predicate
        """
        return self._output_condition
