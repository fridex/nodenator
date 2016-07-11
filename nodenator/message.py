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


class Message(object):
    """
    Message representation
    """
    def __init__(self, message, node_from=None, node_to=None):
        """
        Constructor
        :param message: message that is received
        :type message: dict
        :param node_from: node that sent message
        :type node_from: Node
        :param node_to: node that will receive the message
        :type node_to: Node
        """
        self._node_from = node_from
        self._node_to = node_to
        self._message = message

    @staticmethod
    def create(raw_message, system):
        """
        Construct Message instance based on its raw representation
        :param raw_message: raw message representation
        :param system: system where the message occurred
        :return: Message instance
        :rtype: Message
        """
        if 'node_from' not in raw_message:
            raise KeyError('No node specified in message description')
        if 'message' not in raw_message:
            raise KeyError('No message content specified in message description')
        node_to = system.node_by_name(raw_message.get('node_to')) if raw_message.get('node_to') else None
        return Message(raw_message['message'], system.node_by_name(raw_message['node_from']), node_to)

    def node_from(self):
        """
        Get node that outputted the message
        :return: node
        :rtype: Node
        """
        return self._node_from

    def node_to(self):
        """
        Get node that will receive the message
        :return: node
        :rtype: Node
        """
        return self._node_to

    def message(self):
        """
        Get message representation
        :return: node
        :rtype: Node
        """
        return self._message
