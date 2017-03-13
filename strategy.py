import pprint
import numpy as np
import copy
import operator

from cloud_mocks import *

pp = pprint.PrettyPrinter(indent=2)


class BaseStrategy(object):
    def execute(self, cluster, goal):
        raise NotImplementedError()


def Migration(vm, source, dest):
    return {
        'vm': vm.name,
        'source': source.name,
        'dest': dest.name,
    }


class SchedulerAwareStrategy(BaseStrategy):
    def __init__(self, active_filters):
        self.filters = active_filters
        self.migrations = []

    def host_passes(self, vm, host, cluster_state):
        for f in self.filters:
            passes = f.host_passes(vm, host, cluster_state)
            if not passes:
                return False
        return True

    def get_host_util(self, host, vm_key, host_key, allocation_ratio):
        vm_sum = 0.0
        for vm in host.vms:
            vm_sum += getattr(vm, vm_key)
        return vm_sum / (allocation_ratio * getattr(host, host_key))

    def get_host_cpu_util(self, host, use_flavor = True, alloc_ratio = None):
        allocation_ratio = host.get_metadata('cpu_allocation_ratio', min, 1.0)
        if alloc_ratio:
            allocation_ratio = min(allocation_ratio, alloc_ratio)
        if use_flavor:
            vm_key = 'vcpus'
        else:
            vm_key = 'avg_cpu_util'
        return self.get_host_util(host, vm_key, 'cpus', allocation_ratio)

    def get_host_ram_util(self, host, alloc_ratio = None):
        allocation_ratio = host.get_metadata('ram_allocation_ratio', min, 1.0)
        if alloc_ratio:
            allocation_ratio = min(allocation_ratio, alloc_ratio)
        vm_key = 'vram'
        return self.get_host_util(host, vm_key, 'ram', allocation_ratio)


class ConsolidationGoal(object):
    def __init__(self, data_source = 'flavor'):
        self.data_source = data_source


class ConsolidationStrategy(SchedulerAwareStrategy):
    def __init__(self, active_filters, **kwargs):
        SchedulerAwareStrategy.__init__(self, active_filters)
        self.cpu_allocation_ratio = kwargs.get('cpu_max_util', 0.8)
        self.ram_allocation_ratio = kwargs.get('ram_max_util', 1.5)

    def execute(self, cluster, goal):
        # we'll manipulate deep copy of our cluster
        result = copy.deepcopy(cluster)
        use_flavor = goal.data_source == 'flavor'
        # get sorted by load list of hosts
        hosts_loads = self.get_hosts_loads(result, use_flavor)
        sorted_loads = sorted(hosts_loads.items(), key=lambda hl: hl[1]['total'])
        #print 'sorted hosts:'
        #pp.pprint(sorted_loads)

        # TODO: maybe we should offload vms from overloaded hosts here

        # not let's try to offload hosts starting from least loaded one
        donour_i = 0
        recipient_i = len(result) - 1
        for donour_i in range(len(result) - 1):
            for recipient_i in range(len(result) - 1, donour_i, -1):
                donour = sorted_loads[donour_i][0]
                recipient = sorted_loads[recipient_i][0]
                candidates = []
                for vm in donour.vms:
                    # TODO: cache filter outputs. Looks like N^3 complexity
                    if self.can_migrate(vm, donour, recipient, result, use_flavor):
                        candidates.append(vm)
                best_candidate = self.choose_best_candidate(candidates, donour,
                    recipient, use_flavor)
                #print 'Chosen instance for migration: ' + repr(best_candidate)
                if best_candidate:
                    # preform migration
                    self.migrate(best_candidate, donour, recipient)
                    self.migrations.append(Migration(best_candidate, donour, recipient))
                    # we need to update model
                    # TODO: we actually need to update only two hosts,
                    # so full load rebuilding feels excessive
                    hosts_loads = self.get_hosts_loads(result, use_flavor)
                    sorted_loads = sorted(hosts_loads.items(),
                                          key=lambda hl: hl[1]['total'])
                    # reset counters
                    # Probably we need more efficient solution
                    donour_i = 0
                    recipient_i = len(result) - 1
        return result

    def choose_best_candidate(self, candidates, source, dest, use_flavor):
        # choose the best vm to migrate to dest
        # at first let's choose vm that will make host utilization
        # balanced cpu-ram wise
        if len(candidates) == 0:
            return None
        resulting_loads = {}
        for vm in candidates:
            self.migrate(vm, source, dest)
            new_load = self.host_load(dest, use_flavor)
            resulting_loads[vm] = abs(new_load['cpu'] - new_load['ram'])
            self.migrate(vm, dest, source)
        sorted_results = sorted(resulting_loads.items(),
                                key=operator.itemgetter(1))
        return sorted_results[0][0]


    def can_migrate(self, vm, source, dest, cluster_state, use_flavor):
        schedulers_ok = self.host_passes(vm, dest, cluster_state)
        if not schedulers_ok:
            return False
        # now let's check our own, strategy policies: cpu and ram overbooking
        self.migrate(vm, source, dest)
        try:
            host_util = self.host_load(dest, use_flavor)
            if not use_flavor:
                if host_util['cpu'] > self.cpu_allocation_ratio:
                    return False
            if host_util['ram'] > self.ram_allocation_ratio:
                return False
        finally:
            self.migrate(vm, dest, source)      # rollback migration
        return True

    def migrate(self, vm, source, dest):
        source.vms.remove(vm)
        dest.vms.add(vm)

    def get_hosts_loads(self, cluster, use_flavor):
        res = {}
        for host in cluster:
            res[host] = self.host_load(host, use_flavor)
        return res

    def host_load(self, host, use_flavor = True):
        # get area ratio
        if not use_flavor:
            cpu_alloc_ratio = self.cpu_allocation_ratio
        else:
            cpu_alloc_ratio = None
        cpu_ratio = self.get_host_cpu_util(host, use_flavor, cpu_alloc_ratio)
        ram_ratio = self.get_host_ram_util(host, self.ram_allocation_ratio)
        return {'total': cpu_ratio * ram_ratio,
                'cpu': cpu_ratio,
                'ram': ram_ratio}
