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




class RoutingTable:

    """ Can pass its id via a string or via integer """
    def __init__(self, tableId):

        if type(tableId) == int:
            print("Table loaded from integer")
        elif isinstance(tableId,str):
            tableId = capir.rtnl_route_str2table(tableId)
            # TODO check id is ok 
        else:
            raise ValueError("Invalid table id.")

        self._tableId = tableId
        # super() route/route

    # rtnl_route_table2str 
    @property
    def name(self, maxLength=40):
        """ retrieve table name """
        # forget about  maxLength
        return capir.route_table2str( self._tableId );



    @staticmethod
    def read_names(filename="/etc/iproute2/rt_tables"):

        """ file with format 
            "/etc/iproute2/rt_tables"
            # reserved values
            255 local
            254 main

        """
        err = capir.rtnl_route_read_table_names( filename)
        return err

    @property
    def id(self):
        """ Returns table Id """
        return self._tableId



    """ expects a RoutingEntry """
    def add( self, route, sock=None ):

        if not isinstance(route,RoutingEntry):
            raise ValueError("Wrong argument. Expecting RoutingEntry")

        if not sock:
            sock = netlink.lookup_socket( netlink.NETLINK_ROUTE)


        capir.rtnl_route_set_table( route._nl_route, self._tableId )

        # Set table 
        ret = capir.rtnl_route_add(sock._sock, route._nl_route, 0)
        # if ret == -6:
        #     raise NlExists(ret)
        if ret < 0:
            raise nl.NetlinkError(ret)

    # def __del__(self):
    #     if not self._nl_object:
    #         raise ValueError()
    #     capi.nl_object_put(self._nl_object)



    def __str__(self):
        return "Routing table <{id}> '{name}'".format(id=self._tableId, name=self.name )

    def __repr__(self):
        return __str__(self);

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
    # def format(self):
    #     """Return route as formatted text"""
    #     # fmt = util.MyFormatter(self, indent)
    #     return ('Route %s'%self._nl_route  )
    def format(self, details=False, stats=False, indent=''):
        
        """Return link as formatted text"""
        fmt = util.MyFormatter(self, indent)

        buf = fmt.format('{a|ifindex} {a|name} {a|arptype} {a|address} '\
                 '{a|_state} <{a|_flags}> {a|_brief}')

        if details:
            buf += fmt.nl('\t{t|mtu} {t|txqlen} {t|weight} '\
                      '{t|qdisc} {t|operstate}')
            buf += fmt.nl('\t{t|broadcast} {t|alias}')

            buf += self._foreach_af('details', fmt)



            buf += '\n\t%s%s%s%s\n' % (33 * ' ', util.title('RX'),
                           15 * ' ', util.title('TX'))

        return buf


        
    def set_scope(self):
        pass

    def install(self, sock=None):
        if not sock:
            sock = netlink.lookup_socket( netlink.NETLINK_ROUTE)

        # last param = flags . what does it mean ?
        ret = capir.rtnl_route_add(sock._sock, self._nl_route, 0)
        print("Tried to install route. Result",ret)
        # TODO
        # if ret == -6:
        #     raise nl.NetlinkError(ret)
        if ret < 0:
            raise nl.NetlinkError(ret)

    @property
    def table(self):
        return capir.rtnl_route_get_table(self._nl_route)
    
    # @table.setter
    # def table(self, value):
    #     """ Expects an integer """
    #     capir.rtnl_route_set_table(self._nl_route, self._tableId )

    @property
    def src(self):
        return nladdr.Address( capir.rtnl_route_get_src(self._nl_route) )

    @property
    def dst(self):
        return nladdr.Address( capir.rtnl_route_get_dst(self._nl_route) )

    @dst.setter
    def dst(self, address):
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


    @property
    def dev(self):
        return capir.rtnl_route_get_iif ( self._nl_route)

    @dev.setter    
    def dev (self,interface):

        """ 
        Expects interface name, either integer, str, or dev 

        """
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