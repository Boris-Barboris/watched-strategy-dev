#!/usr/bin/python2.7

import pprint
import numpy as np
import matplotlib.pyplot as plt

from plot_cloud import print_servers
from cloud_mocks import *

pp = pprint.PrettyPrinter(indent=2)

host_count = 5
servers = []
cpu_powers = np.random.randint(4, size=host_count)
memory_powers = np.random.randint(4, size=host_count)
for i in range(host_count):
    servers.append(
        Server(
            name = "host" + str(i),
            cpus = 2 ** (3 + cpu_powers[i]),
            ram = 2 ** (12 + memory_powers[i])))

vm_count = 20

vm_host_map = np.random.randint(host_count, size=vm_count)

vms = []
vcpu_powers = np.random.randint(4, size=vm_count)
vmemory_powers = np.random.randint(4, size=vm_count)
for i in range(vm_count):
    vm = Instance(
            vcpus = 2 ** (1 + vcpu_powers[i]),
            vram = 2 ** (8 + vmemory_powers[i]))
    vms.append(vm)
    servers[vm_host_map[i]].vms.append(vm)

pp.pprint(servers)
print_servers(servers)
