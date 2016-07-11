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


import yaml
import sys
import importlib


class _ConfigSingleton(type):
    """
    Singleton representation for Config
    """
    _instance = None

    def __call__(cls, *args, **kwargs):
        """
        Get singeton instance
        :return: singleton instance
        """
        if cls._instance is None:
            cls._instance = super(_ConfigSingleton, cls).__call__(*args, **kwargs)
        return cls._instance

    def set_config(cls, config):
        """
        Set config file path to be parsed
        :param config: path to a config file
        :type config: str
        """
        # set _config before the singleton is instantiated
        assert(cls._instance is None)
        cls._config = config


class Config(object):
    """
    Configuration representation
    """
    _config = None
    __metaclass__ = _ConfigSingleton

    def __init__(self):
        """
        Constructor
        """
        self._predicate_dir = None
        self._raw_config = None

        if self._config is None:
            return

        with open(self._config) as f:
            self._raw_config = yaml.load(f)

        if 'predicate-dir' in self._raw_config:
            self._predicate_dir = self._raw_config['predicate-dir']
            sys.path.append(self._predicate_dir)

    def predicate_module(self, name):
        """
        Get predicate module
        :param name: name of a predicate to import
        :return: Python module
        """
        if self._predicate_dir is None:
            # use default predicates by default
            return importlib.import_module("nodenator.predicates.%s" % name)
        else:
            return importlib.import_module(name)

    def style_node(self):
        """
        Get style for nodes in generated graph
        :return: style for nodes if defined (empty dict otherwise to use defaults)
        :rtype: dict
        """
        if self._raw_config is None or 'style' not in self._raw_config:
            return {}
        ret = self._raw_config['style'].get('node', {})
        return ret if ret is not None else {}

    def style_edge(self):
        """
        Get style for edges in generated graph
        :return: style for edge if defined (empty dict otherwise to use defaults)
        :rtype: dict
        """
        if self._raw_config is None or 'style' not in self._raw_config:
            return {}
        ret = self._raw_config['style'].get('edge', {})
        return ret if ret is not None else {}

    def style_graph(self):
        """
        Get style for graph in generated graph
        :return: style for graph if defined (empty dict otherwise to use defaults)
        :rtype: dict
        """
        if self._raw_config is None or 'style' not in self._raw_config:
            return {}
        ret = self._raw_config['style'].get('graph', {})
        return ret if ret is not None else {}
