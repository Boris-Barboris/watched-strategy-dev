#!/usr/bin/python2.7

import pprint
import numpy as np

from cloud_mocks import *

pp = pprint.PrettyPrinter(indent=2)


class BaseStrategy(object):
    def execute(self, cluster, goal):
        raise NotImplementedError()


class SchedulerAwareStrategy(BaseStrategy):
    def __init__(self, active_filters):
        self.filters = active_filters


class ConsolidationStrategy(SchedulerAwareStrategy):
    def __init__(self, active_filters, **kwargs):
        SchedulerAwareStrategy.__init__(self, active_filters)
        self.cpu_ratio = kwargs.get('cpu_max_util', 0.8)
        self.ram_ratio = kwargs.get('ram_max_util', 1.5)

    def execute(self, cluster, goal):
        return cluster
