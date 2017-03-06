import matplotlib.pyplot as plt
import matplotlib.patches as patches

_colors = ('blue', 'yellow', 'cyan')

def print_servers(servers, cpu_metric='vcpus'):
    fig = plt.figure()

    for i in range(len(servers)):
        host_subplot = fig.add_subplot(100 + 10 * len(servers) + i + 1)
        host_subplot.set_title(servers[i].name)
        draw_server(host_subplot, servers[i], cpu_metric)

    fig.subplots_adjust(top=0.85, left=0.05, right=0.97)
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
