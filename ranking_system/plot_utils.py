import itertools


# Plot the total volatility over time
def list_line_plot(plt, data, xlabel, ylabel, title, xlim_left=None,
                   xlim_right=None, ylim_bottom=0, ylim_top=None):
    fig, ax = plt.subplots()
    ax.plot(data, marker='s', fillstyle='full', markerfacecolor='w',
            markeredgecolor='grey')
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
    plt.xlim(xlim_left, xlim_right)
    plt.ylim(ylim_bottom, ylim_top)
    plt.tick_params(direction='in', top=True, right=True)


# Plot the agent volatility over time
def dictionary_line_plot(plt, data, xlabel, ylabel, title, xlim_left=None,
                         xlim_right=None, ylim_bottom=0, ylim_top=None):
    fig, ax = plt.subplots()
    marker = itertools.cycle(('o', 's', 'h', 'd', 'p', 'v', '^', '<', '>', 'H',
                              'D', '*', '|', 'x', '1', '2', '3', '4'))
    legend_labels = []
    for label, y_values in data.items():
        legend_labels.append(label)
        ax.plot(y_values, label=label, marker=next(marker), fillstyle='full',
                markerfacecolor='w', markeredgecolor='grey')

    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
    ax.legend(labels=legend_labels, fontsize='small')
    plt.xlim(xlim_left, xlim_right)
    plt.ylim(ylim_bottom, ylim_top)
    plt.tick_params(direction='in', top=True, right=True)
