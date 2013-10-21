#
# Copyright (c) 2011 Thomas Graf <tgraf@suug.ch>
#

"""Module providing access to network addresses
"""

from __future__ import absolute_import


import netlink.core as netlink
# __version__ = '1.0'
# __all__ = [
# ]

# cacheable
class Rule(netlink.Object):

    def __init__(self, obj=None):
        # pass 
        # self._nl_route = capir.rtnl_route_alloc()

        super().__init__( "route/rule", "rule", obj )

        self._nl_rule = self._obj2type(self._nl_object)

    def _obj2type(self):
        raise NotImplementedError();
        

# class RoutingTableCache(netlink.Cache):
# 	def __init__(self):
# 		pass


# class RoutingTable:

# 	""" Can pass its id via a string or via integer """
# 	def __init__(self,id):
# 		if type(id) == int:
# 			print("")
# 	# def format()