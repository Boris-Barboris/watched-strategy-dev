import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

_colors = ('blue', 'yellow', 'cyan')

def _maximize():
    mng = plt.get_current_fig_manager()
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        mng.window.state('zoomed')
    elif backend == 'wxAgg':
        mng.frame.Maximize(True)
    elif backend == 'Qt4Agg':
        mng.window.showMaximized()

def print_servers(servers, cpu_metric='vcpus'):
    fig = plt.figure()

    for i in range(len(servers)):
        host_subplot = plt.subplot2grid((1, len(servers)), (0, i))
        host_subplot.set_title(servers[i].name)
        draw_server(host_subplot, servers[i], cpu_metric)

    _maximize()
    plt.tight_layout()
    plt.show()

def print_servers2(servers1, servers2, cpu_metric='vcpus'):
    fig = plt.figure()

    for i in range(len(servers1)):
        host_subplot = plt.subplot2grid((2, len(servers1)), (0, i))
        host_subplot.set_title(servers1[i].name)
        draw_server(host_subplot, servers1[i], cpu_metric)

    for i in range(len(servers2)):
        host_subplot = plt.subplot2grid((2, len(servers2)), (1, i))
        host_subplot.set_title(servers2[i].name)
        draw_server(host_subplot, servers2[i], cpu_metric)

    _maximize()
    plt.tight_layout()
    plt.show()

def draw_server(sp, server, cpu_metric='vcpus'):
    # at last, draw rectangle that represents capabilities
    sp.add_patch(
        patches.Rectangle((0, 0), server.ram, server.cpus,
                        facecolor='none', edgecolor='black', hatch='/'))
    total_vcpus = sum([vm.cpu_metric(cpu_metric) for vm in server.vms])
    total_vram = sum([vm.vram for vm in server.vms])
    max_cpu = max(total_vcpus, server.cpus)
    max_ram = max(total_vram, server.ram)
    offset = (0, 0)
    for index, vm in enumerate(server.vms):
        color = _colors[index % len(_colors)]
        vcpu = vm.cpu_metric(cpu_metric)
        sp.add_patch(
            patches.Rectangle(offset, vm.vram, vcpu,
                        color=color))
        sp.annotate(vm.name, offset, color='red')
        offset = (offset[0] + vm.vram, offset[1] + vcpu)
    sp.set_xlim([0,max_ram])
    sp.set_ylim([0,max_cpu])
    #sp.set_xlabel('vram')
    #sp.set_ylabel('vcpu')
