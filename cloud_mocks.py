from sets import Set

class Server(object):
    def __init__(self, name, cpus, ram, metadata=None):
        self.name = name
        self.cpus = cpus
        self.ram = ram
        self.aggregates = Set()
        self.vms = Set()

    def get_metadata(self, key, aggregation = min, default = None):
        vals = []
        for ha in self.aggregates:
            if key in ha.metadata:
                vals.append(ha.metadata[key])
        if len(vals) == 0:
            return default
        return aggregation(vals)

    def __repr__(self):
        return "<Server " + str(self.__dict__) + "/>"


class HostAggregate(object):
    def __init__(self, metadata = {}, hosts = []):
        self.metadata = metadata
        self.hosts = Set()
        self.update(hosts)

    def add(self, host):
        self.hosts.add(host)
        host.aggregates.add(self)

    def update(self, hosts):
        for h in hosts:
            self.add(h)

    def __repr__(self):
        return "<HostAggregate " + str(self.__dict__) + "/>"


class AvailabilityZone(object):
    def __init__(self, name, aggregate):
        self.host_aggregate = aggregate
        self.host_aggregate.metadata['availability_zone'] = name

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
