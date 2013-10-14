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
            print("Table loaded from integer")
        elif isinstance(tableId,str):
            tableId = capir.rtnl_route_str2table(tableId)
            # TODO check id is ok 
        else:
            raise ValueError("Invalid table id.")

        # super() route/route


    # def __del__(self):
    #     if not self._nl_object:
    #         raise ValueError()
    #     capi.nl_object_put(self._nl_object)

    # def format()
    def list_entries(self):
        pass

    def addEntry(self, route):
    # def add(self, dst, gw=None):
        """ add a new route """
        # nh = capi.rtnl_route_nh_alloc()
        # route = capi.rtnl_route_alloc()

        addr_dst = netlink.AbstractAddress(dst)
        ifidx = self._link.ifindex

        capi.rtnl_route_set_dst(route, addr_dst._nl_addr)
        capi.rtnl_route_nh_set_ifindex(nh, ifidx)
        if gw is not None:
            addr_gw = netlink.AbstractAddress(gw)
            capi.rtnl_route_nh_set_gateway(nh, addr_gw._nl_addr)
        capi.rtnl_route_add_nexthop(route, nh)
        ret = capi.rtnl_route_add(self._sock._sock, route, 0)
        if ret == -6:
            raise NlExists(ret)
        if ret < 0:
            raise NlError(ret)


    def delEntry(self, route):
        pass
        # rtnl_route_delete(self._sock._sock, route, 0)

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

class NextHop(netlink.Object):

    # def __init__(self, addr, interface, gw=None):
    def __init__(self, obj=None):
        # pass 
        # self._nl_route = capir.rtnl_route_alloc()

        super().__init__( "route/route", "myRoute", obj )
        # super().__init__( "route/route", "myRoute", self._nl_route )
        
        self._nl_route = self._obj2type(self._nl_object)
        # nh stands for nexthop
        self._nl_nh = None

# flnl_request
# TODO should be created elsewhere and not instantiated directly
# rtnl_route_nh_set_gateway
# rename into Route
# TODO add constructors
class RoutingEntry(netlink.Object):

    # def __init__(self, addr, interface, gw=None):
    def __init__(self, obj=None):
        # pass 
        # self._nl_route = capir.rtnl_route_alloc()

        super().__init__( "route/route", "myRoute", obj )
        # super().__init__( "route/route", "myRoute", self._nl_route )
        
        self._nl_route = self._obj2type(self._nl_object)
        # nh stands for nexthop
        self._nl_nh = None

    # TODO 
    def __del__(self):
        if self._nl_nh:
            pass

    @staticmethod
    def _obj2type(obj):
        return capir.obj2route(obj)

    # def __getitem__():
    def format(self):
        """Return route as formatted text"""
        # fmt = util.MyFormatter(self, indent)
        return ('Route %s'%self._nl_route  )

    def set_scope(self):
        pass


    #
    def set_table(self,tableId):
        """ Expects an integer """
        capir.rtnl_route_set_table(self._nl_route, int(tableId) )

    def get_table(self):
        return capir.rtnl_route_get_table(self._nl_route)

    def get_src(self):
        return nladdr.Address( capir.rtnl_route_get_src(self._nl_route) )

    def get_dst(self):
        return nladdr.Address( capir.rtnl_route_get_dst(self._nl_route) )

    def set_dst(self, address):
        # nladdr.Address(
        # print( "ROUTE", )
        return  capir.rtnl_route_set_dst(self._nl_route, address )

    def get_gw(self):
        return nladdr.Address( capir.rtnl_route_nh_get_gateway( self._nl_nh) )

    """
    A route towards the gateway should be available before 
    setting that gateway 
    """
    def set_gw(self,gw, check_route_is_available=False):
        """ if no nexthop allocated yet, allocate one"""
        if not self._nl_nh:
            self._nl_nh = capir.rtnl_route_nh_alloc()

        if check_route_is_available:
            #TODO check 
            pass

        # set address
        capir.rtnl_route_nh_set_gateway(self._nl_nh, gw)

    """ Returns scope as a string """
    def get_scope(self):
        # extern char * rtnl_scope2str(int, char *buf, size_t len);
        return capir.rtnl_route_get_scope ( self._nl_route );

    def get_if (self):
        return capir.rtnl_route_get_iif ( self._nl_route)
    
    """ 
    Expects interface name, either integer, str, or dev 

    """
    def set_if (self,interface):

        if isinstance(interface, str):
            # convert it 
            # int rtnl_link_name2i (struct nl_cache *cache, const char *name);
            pass

        return capir.rtnl_route_set_iif ( self._nl_route, interface)
        


if __name__ == '__main__': 

    # Tries to install, do a lookup of the route 
    # and finally delete that same route

    route = RoutingEntry()
    route.set_gw()

    exit(0)