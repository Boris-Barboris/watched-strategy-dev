import pprint

from cloud_mocks import *
from filters import *
from plot_cloud import *
import strategy


pp = pprint.PrettyPrinter(indent=2)


def case_simple1():
    '''Simple case with three hosts and intersecting host aggregates'''
    server1 = Server('server1', 32, 65536)
    server2 = Server('server2', 32, 65536)
    server3 = Server('server3', 32, 65536)
    ha1 = HostAggregate({'ha': 'ha1'}, [server1, server2])
    ha2 = HostAggregate({'ha': 'ha2'}, [server2, server3])
    vm1 = Instance('vm1', 8, 4096, {'ha': 'ha1'})
    vm2 = Instance('vm2', 8, 4096)
    vm3 = Instance('vm3', 8, 4096, {'ha': 'ha2'})
    server1.vms.add(vm1)
    server2.vms.add(vm2)
    server3.vms.add(vm3)
    filters = [MetadataSimpleFilter('ha'), RamFilter(), CpuFilter()]
    cluster = [server1, server2, server3]
    consol = strategy.ConsolidationStrategy(filters)
    print '=====Initial cluster state:'
    pp.pprint(cluster)
    result = consol.execute(cluster, strategy.ConsolidationGoal('flavor'))
    print '=====Resulting cluster state:'
    pp.pprint(result)
    print '=====Migrations:'
    pp.pprint(consol.migrations)
    print_servers2(cluster, result)


def case_uniform_cpu():
    '''Simple case with three hosts and no host aggregates. CPU-oriented'''
    server1 = Server('server1', 32, 65536)
    server2 = Server('server2', 32, 65536)
    server3 = Server('server3', 32, 65536)
    # simulate overbook quotas
    ha1 = HostAggregate({'cpu_allocation_ratio': 1.5},
        [server1, server2, server3])
    vm1 = Instance('vm1', 4, 4096)
    vm2 = Instance('vm2', 8, 4096)
    vm3 = Instance('vm3', 8, 4096)
    vm4 = Instance('vm4', 16, 4096)
    vm5 = Instance('vm5', 4, 4096)
    server1.vms.add(vm1)
    server1.vms.add(vm5)
    server2.vms.add(vm2)
    server3.vms.add(vm3)
    server3.vms.add(vm4)
    filters = [MetadataSimpleFilter('ha'), RamFilter(), CpuFilter()]
    cluster = [server1, server2, server3]
    consol = strategy.ConsolidationStrategy(filters)
    print '=====Initial cluster state:'
    pp.pprint(cluster)
    result = consol.execute(cluster, strategy.ConsolidationGoal('flavor'))
    print '=====Resulting cluster state:'
    pp.pprint(result)
    print '=====Migrations:'
    pp.pprint(consol.migrations)
    print_servers2(cluster, result)


def case_uniform_ram():
    '''Simple case with three hosts and no host aggregates. RAM-oriented'''
    server1 = Server('server1', 32, 65536)
    server2 = Server('server2', 32, 65536)
    server3 = Server('server3', 32, 65536)
    # simulate overbook quotas
    ha1 = HostAggregate({'cpu_allocation_ratio': 1.5},
        [server1, server2, server3])
    vm1 = Instance('vm1', 4, 4 * 4096)
    vm2 = Instance('vm2', 8, 4 * 4096)
    vm3 = Instance('vm3', 8, 3 * 4096)
    vm4 = Instance('vm4', 16, 4 * 4096)
    vm5 = Instance('vm5', 4, 5 * 4096)
    server1.vms.add(vm1)
    server1.vms.add(vm5)
    server2.vms.add(vm2)
    server3.vms.add(vm3)
    server3.vms.add(vm4)
    filters = [MetadataSimpleFilter('ha'), RamFilter(), CpuFilter()]
    cluster = [server1, server2, server3]
    consol = strategy.ConsolidationStrategy(filters)
    print '=====Initial cluster state:'
    pp.pprint(cluster)
    result = consol.execute(cluster, strategy.ConsolidationGoal('flavor'))
    print '=====Resulting cluster state:'
    pp.pprint(result)
    print '=====Migrations:'
    pp.pprint(consol.migrations)
    print_servers2(cluster, result)


def case_isolated_simple():
    '''Two isolated host aggregates need to be internally grouped'''
    server1 = Server('server1', 32, 65536 / 2)
    server2 = Server('server2', 32, 65536 / 2)
    server3 = Server('server3', 32, 65536 / 2)
    server4 = Server('server4', 32, 65536 / 2)
    ha1 = HostAggregate({'ha': 'ha1'}, [server1, server2])
    ha2 = HostAggregate({'ha': 'ha2'}, [server3, server4])
    vm1 = Instance('vm1', 8, 4096, {'ha': 'ha1'})
    vm2 = Instance('vm2', 8, 4096, {'ha': 'ha1'})
    vm3 = Instance('vm3', 4, 4096, {'ha': 'ha1'})
    vm4 = Instance('vm4', 16, 4096, {'ha': 'ha1'})
    vm5 = Instance('vm5', 8, 4096, {'ha': 'ha2'})
    vm6 = Instance('vm6', 8, 4096, {'ha': 'ha2'})
    vm7 = Instance('vm7', 4, 4096, {'ha': 'ha2'})
    vm8 = Instance('vm8', 16, 4096, {'ha': 'ha2'})
    server1.vms.add(vm1)
    server1.vms.add(vm2)
    server2.vms.add(vm3)
    server2.vms.add(vm4)
    server3.vms.add(vm5)
    server3.vms.add(vm6)
    server3.vms.add(vm8)
    server4.vms.add(vm7)
    filters = [MetadataSimpleFilter('ha'), RamFilter(), CpuFilter()]
    cluster = [server1, server2, server3, server4]
    consol = strategy.ConsolidationStrategy(filters)
    print '=====Initial cluster state:'
    pp.pprint(cluster)
    result = consol.execute(cluster, strategy.ConsolidationGoal('flavor'))
    print '=====Resulting cluster state:'
    pp.pprint(result)
    print '=====Migrations:'
    pp.pprint(consol.migrations)
    print_servers2(cluster, result)
