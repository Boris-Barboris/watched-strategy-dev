#!/usr/bin/python2.7

from cloud_mocks import *

class HostFilter(object):
    def host_passes(self, vm, host, cluster):
        raise NotImplementedError()

class MetadataSimpleFilter(HostFilter):
    '''Allow instance scheduling only on those hosts that
    both have metadata and those values match.'''
    def __init__(self, key):
        self.key = key

    def host_passes(self, vm, host, cluster):
        if self.key in vm.metadata:
            if self.key in host.metadata:
                return vm.metadata[self.key] == host.metadata[self.key]
        return True

class RamFilter(HostFilter):
    def host_passes(self, vm, host, cluster):
        used_memory = sum([i.vram for i in host.vms])
        allocation_ratio = host.metadata.get('ram_allocation_ratio', 1.0)
        free_memory = allocation_ratio * host.ram - used_memory
        if vm.vram <= free_memory:
            return True
        return False

class CpuFilter(HostFilter):
    def host_passes(self, vm, host, cluster):
        used_cores = sum([i.vcpus for i in host.vms])
        allocation_ratio = host.metadata.get('cpu_allocation_ratio', 1.0)
        free_cores = allocation_ratio * host.cpus - used_cores
        if vm.vcpus <= free_cores:
            return True
        return False
