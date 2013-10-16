#
# Copyright (c) 2011 Thomas Graf <tgraf@suug.ch>
#

"""Module providing access to network routes
"""

from __future__ import absolute_import


import netlink.route.capi as capir
import netlink.route.address as nladdr
import netlink.core as netlink
import netlink.util as util

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
    def __init__(self, routingTable):

        tableId = None
        if isinstance(routingTable, int ):
            print("Table loaded from integer")
            tableId=routingTable
        elif isinstance(tableId, str):
            tableId = capir.rtnl_route_str2table(tableId)
            # TODO check id is ok 
        elif isinstance(tableId, RoutingTable):
            tableId = routingTable.id
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

        print ("Setting table to %d"%self._tableId)
        capir.rtnl_route_set_table( route._nl_route, self._tableId )

        # Set table
        ret = capir.rtnl_route_add(sock._sock, route._nl_route, 0)

        print("Ret value %d"%ret )
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
        # TODO do FIb lookup
        pass



    def delEntry(self, route,sock=None):

        if not sock:
            sock = netlink.lookup_socket( netlink.NETLINK_ROUTE)

        ret = capir.rtnl_route_delete(self._sock._sock, route._nl_route, 0)

        if ret < 0:
            raise netlink.NetlinkError(ret)

        return ret 

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

# not cacheable
class NextHop:

#     # def __init__(self, addr, interface, gw=None):
    def __init__(self, ifidx=None):
        self._nh = capir.rtnl_route_nh_alloc()

    def __del__(self):
        if self._nh:
            capir.rtnl_route_nh_free( self._nh )

    @property
    def interface(self):
        return capir.rtnl_route_nh_get_ifindex( self._nh )

    @interface.setter
    def interface(self, iid):
        # TODO accept a link iid could be a link
        capir.rtnl_route_nh_set_ifindex( self._nh, iid)

    @property
    def gateway(self):
        return capir.rtnl_route_nh_get_gateway( self._nh )
    
    @gateway.setter
    def gateway(self,gw):
        addr_gw = netlink.AbstractAddress(gw)
        capir.rtnl_route_nh_set_gateway( self._nh, addr_gw._nl_addr)



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
        # self._nexthops = None

    # TODO 
    def __del__(self):
        # if self._nl_nh:
        pass        

    @staticmethod
    def _obj2type(obj):
        return capir.obj2route(obj)


    def add_nexthop(self,nh):

        if not isinstance(nh,NextHop):
            raise ValueError("Invalid next hop")

        # capi.rtnl_route_add_nexthop
        capir.rtnl_route_add_nexthop( self._nl_route, nh._nh)
        pass


    # def __getitem__():
    # def format(self):
    #     """Return route as formatted text"""
    #     # fmt = util.MyFormatter(self, indent)
    #     return ('Route %s'%self._nl_route  )
    def format(self, details=False, stats=False, indent=''):
        
        """Return link as formatted text"""
        buf = "Src:"+ str(self.src) + ", dst:" + str(self.dst)
        # fmt = util.MyFormatter(self, indent)

        # buf = fmt.format('{a|ifindex} {a|name} {a|arptype} {a|address} '
        #          )
        # #'{a|_state} <{a|_flags}> {a|_brief}'

        # if details:
        #     buf += fmt.nl('\t{t|mtu} {t|txqlen} {t|weight} '\
        #               '{t|qdisc} {t|operstate}')
        #     buf += fmt.nl('\t{t|broadcast} {t|alias}')

        #     buf += self._foreach_af('details', fmt)



        #     buf += '\n\t%s%s%s%s\n' % (33 * ' ', util.title('RX'),
        #                    15 * ' ', util.title('TX'))

        return buf


    @property
    def scope(self):
        
        """ Returns scope as a string """
        # extern char * rtnl_scope2str(int, char *buf, size_t len);
        return capir.rtnl_route_get_scope ( self._nl_route );


    # TODO remove ?
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
        # rtnl_route_get_src
        # get_src returns a nl_addr
        addr = netlink.AbstractAddress( capir.rtnl_route_get_src(self._nl_route) )
        return addr

    @property
    def dst(self):
        # return nladdr.Address( capir.rtnl_route_get_dst(self._nl_route) )
        addr = netlink.AbstractAddress( capir.rtnl_route_get_dst(self._nl_route) ) 
        return addr

    @dst.setter
    def dst(self, address):
        # nladdr.Address(
        # print( "ROUTE", )
        return  capir.rtnl_route_set_dst(self._nl_route, address )

    @property
    def gw(self):
        return nladdr.Address( capir.rtnl_route_nh_get_gateway( self._nl_nh) )

    @gw.setter
    def gw(self, gw, check_route_is_available=False):
        """
        A route towards the gateway should be available before 
        setting that gateway 
        """        
        """ if no nexthop allocated yet, allocate one"""
        if not self._nl_nh:
            self._nl_nh = capir.rtnl_route_nh_alloc()

        if check_route_is_available:
            #TODO check 
            pass

        # set address
        capir.rtnl_route_nh_set_gateway(self._nl_nh, gw)



    @property
    def dev(self):
        return capir.rtnl_route_get_iif ( self._nl_route)


    @dev.setter    
    def dev(self,interface):

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