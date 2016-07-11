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


from node import Node


class Edge(object):
    """
    Edge representation
    """
    def __init__(self, node_to, node_from, condition, description=None, name=None):
        """
        Constructor
        :param node_to: a node in which edge ends
        :param node_from: a node in which edge starts
        :param condition: condition on edge transition
        :param description: node description
        :param name: node name
        :return:
        """
        self._name = name
        self._node_to = node_to
        self._node_from = node_from
        self._description = description
        self._condition = condition

    def name(self):
        """
        Get a name of the node
        :return: name of node
        :rtype: str
        """
        return self._name if self._name is not None else id(self)

    def node_to(self):
        """
        Get a node where the edge ends
        :return: return node where the edge ends
        :rtype: Node
        """
        return self._node_to

    def node_from(self):
        """
        Get a node where the edge starts
        :return: return node where the edge starts
        :rtype: Node
        """
        return self._node_from

    def condition(self):
        """
        Return edge transition condition
        :return: edge condition
        :rtype: Predicate
        """
        return self._condition

    def description(self):
        """
        Get node description
        :return: node description
        :rtype: str
        """
        return self._description
