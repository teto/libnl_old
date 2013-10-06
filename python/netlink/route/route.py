#
# Copyright (c) 2011 Thomas Graf <tgraf@suug.ch>
#

"""Module providing access to network routes
"""

from __future__ import absolute_import


import netlink.route.capi as capir
import netlink.route.address as nladdr
import netlink.core as netlink

__version__ = '1.0'
# __all__ = [
# 'RoutingTablesCache',
# 'RoutingTable',
# 'RoutingEntry'
# ]

def read_table_names(self,filename):
    err = capir.rtnl_route_read_table_names( "/etc/iproute2/rt_tables")
    return err



class RoutingTablesCache(netlink.Cache):
    def __init__(self, cache=None):

        # TODO use capi.rtnl_route_alloc_cache  
        super().__init__(cache) 




class RoutingTable(netlink.Object):

    """ Can pass its id via a string or via integer """
    def __init__(self, tableId):
        if type(tableId) == int:
            print("")
        elif isinstance(tableId,str):
            tableId = capir.rtnl_route_str2table(tableId)
            # TODO check id is ok 
        else:
            raise ValueError("Invalid table id.")

        self._nl_route = capir.rtnl_route_alloc()

    # def __del__(self):
    #     if not self._nl_object:
    #         raise ValueError()
    #     capi.nl_object_put(self._nl_object)

    # def format()
    def list_entries(self):
        pass

    def lookup(self, address):

        address = nladdr.Address(address)
        
        # build request
        req = request.capir.flnl_request_alloc()
        capir.flnl_request_set_table(req)
        # flnl_request_set_scope(req, )
        # TODO get object of address
        capir.flnl_request_set_addr(req, address)




    #     int flnl_lookup     (   struct nl_sock *    sk,
    #     struct flnl_request *   req,
    #     struct nl_cache *   cache 
    # )   




# flnl_request
# TODO should be created elsewhere and not instantiated directly
# rtnl_route_nh_set_gateway
# rename into Route
class RoutingEntry(netlink.Object):

    def __init__(self, obj=None):
        # pass 
        self._nl_route = None

    def set_scope(self):
        pass

    def get_scope(self):
        pass

    def get_table(self):
        return capir.rtnl_route_get_table(self._nl_route)

    def get_src(self):
        return nladdr.Address( capir.rtnl_route_get_src(self._nl_route) )

    def get_dst(self):
        return nladdr.Address( capir.rtnl_route_get_dst(self._nl_route) )

    def get_scope(self):
        pass

    def get_iif (self):
        return capir.rtnl_route_get_iif ( self._nl_route)
        