class Server(object):
    def __init__(self, name, cpus, ram, metadata=None):
        self.name = name
        self.cpus = cpus
        self.ram = ram
        if metadata:
            self.metadata = metadata
        else:
            self.metadata = {}
        self.vms = []

    def __repr__(self):
        return "<Server " + str(self.__dict__) + "/>"


class HostAggregate(list):
    def __init__(self, metadata = {}, hosts = []):
        list.__init__(self)
        self.metadata = metadata
        self.extend(hosts)

    def append(self, host):
        list.append(self, host)
        host.metadata.update(self.metadata)

    def extend(self, hosts):
        for h in hosts:
            self.append(h)

    def __repr__(self):
        return "<HostAggregate " + str(self.__dict__) + "/>"


class AvailabilityZone(object):
    def __init__(self, name, aggregate):
        self.host_aggregate = aggregate
        self.host_aggregate.metadata['az'] = name

    def __repr__(self):
        return "<AvailabilityZone " + str(self.__dict__) + "/>"


class Instance(object):
    def __init__(self, name, vcpus, vram, metadata=None):
        self.vcpus = vcpus
        self.vram = vram
        self.name = name
        if metadata:
            self.metadata = metadata
        else:
            self.metadata = {}
        self.avg_cpu_util = 0.0

    def cpu_metric(self, mname = 'vcpus'):
        if mname == 'vcpus':
            return self.vcpus
        else:
            return self.vcpus * self.avg_cpu_util

    def __repr__(self):
        return "<Instance " + str(self.__dict__) + "/>"
