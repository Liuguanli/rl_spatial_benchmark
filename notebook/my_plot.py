import json
import os
import sys

import numpy as np
from matplotlib.lines import Line2D    

# from constants import *

import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman']
rcParams['text.usetex'] = False 

rcParams['pdf.fonttype'] = 42
rcParams['ps.fonttype'] = 42

# colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#C2C2F0','#FFA07A', '#B0E0E6', '#FFD700', '#D3D3D3']

patterns = ['/', 'x', 'o', 
            '\\', '+', '.', 
            '|', '-', '*']

colors = ['#A9A9F5', '#FFD700', '#88CCEE', '#FFCC99', '#FFA07A', '#FF6F61', '#B0E0E6', '#2CA02C', '#AA4499']


colors = ['#B0E0E6', '#88CCEE', '#5599CC', '#2A4A99',
          '#FFD1B3', '#FF9966', '#FF6347', '#CC4F36',
          '#B0E6B0', '#88DDAA', '#559966', '#2E664D']

patterns = [None, '/', 'o', None, '\\', '.', None, '+', '*']
patterns = [None, '-|', 'o', '-', None, '\\', '.', '*', None, '/', '+', 'x']
patterns = [None, '/', 'o', '-', None, '\\', '.', '*', None, 'xx', '+', 'x']



folder= "../../../../../应用/Overleaf/" + "Benchmarking RL Spatial Index"

label_size = 24
legend_size = 20
width_total = 0.8
spacing = 0.0
fig_width = 13.5
fig_height_no_legend = 3.2
fig_height_legend = 4



def plot_hist(datasets, baseline_names, result, y_label="", is_legend=True, is_log=False, title="", output_file_paths=None, bottom=1, top=None, legend_location="right"):

    fig_height = fig_height_legend if is_legend else fig_height_no_legend
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    width = width_total / len(baseline_names)
    x = np.arange(len(datasets))

    # plt.minorticks_on()
    ax.minorticks_on() # Enable minor ticks only on the y-axis

    group_width = len(baseline_names) * width 
    
    for i, baseline in enumerate(baseline_names):
        offset = int(i / 4) * spacing
        adjusted_x = x - int(len(baseline_names) / 2) * width + i * width + offset
        if sum(result[i]) == 0:
            # ax.bar(adjusted_x, 1, "Not Available", width=width, label=baseline, color=colors[i % len(colors)], hatch=patterns[i % len(patterns)], edgecolor='black', linestyle='--')
            not_available_bottom_1 = bottom * 2 if is_log else bottom * 1.1
            not_available_bottom_2 = bottom * 3 if is_log else bottom * 1.2
            for j in range(len(datasets)):  # Iterate over datasets
                ax.scatter(adjusted_x[j], not_available_bottom_1, marker='x', color=colors[i % len(colors)], s=100)  # Add cross marker
                ax.text(adjusted_x[j], not_available_bottom_2, "Not Available", 
                        ha='center', va='bottom', color='red', fontsize=10, rotation=90)

        ax.bar(adjusted_x, result[i], width=width, label=baseline, color=colors[i % len(colors)], hatch=patterns[i % len(patterns)], edgecolor='black', linestyle='--')

    # if not is_log:
    #     bottom = 0
    ax.set_ylim(bottom=bottom)
    if top:
        ax.set_ylim(top=top)
    ax.set_ylabel(y_label, fontsize=label_size)
    ax.set_xticks(x + spacing * (len(baseline_names) // 4 - 1) / 2) 
    ax.set_xticklabels(datasets, fontsize=label_size)
    ax.tick_params(axis='x', labelsize=label_size)
    ax.tick_params(axis='y', labelsize=label_size)

    ax.set_title(title, fontsize=label_size)
    
    if is_log:
        ax.set_yscale('log')
    
    if is_legend:
        if legend_location == 'right':
            legend = ax.legend(
                loc='upper center',
                bbox_to_anchor=(1.11, 1.05),
                fontsize=legend_size,
                ncol=1,
                borderaxespad=0.5,  # Border padding
                handletextpad=0.5,  # Padding between legend marker and text
                labelspacing=0.3    # Vertical space between legend entries
            )
        if legend_location == 'top':
            legend = plt.legend(
                loc='upper center',          
                bbox_to_anchor=(0.5, 1.37),  
                ncol=6,                      
                frameon=False,     
                fontsize=legend_size,
                handlelength=1.4,               # Adjusts the length of the legend handles
                handletextpad=1,            # Reduces the space between handle and text
                columnspacing=1,
                labelspacing=0.1    # Vertical space between legend entries
            )
        plt.setp(legend.get_title(), fontsize=legend_size)
        
    plt.tight_layout()
    
    if output_file_paths:
        for output_file_path in output_file_paths:
            if output_file_path.endswith(".pdf"):
                plt.savefig(output_file_path, format='pdf', bbox_inches='tight')
            if output_file_path.endswith(".png"):
                plt.savefig(output_file_path, format='png', bbox_inches='tight')
    
    plt.show()
    plt.close(fig)

def plot_hist_stack(datasets, baseline_names, result, y_label=None, is_log=False, title="", output_file_paths=None, bottom=1, top=None, legend_labels=[], legend_location="left"):
    
    fig_height = fig_height_legend

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    width = width_total / len(baseline_names)
    x = np.arange(len(datasets))
    
    group_width = len(baseline_names) * width 
    bars = []
    
    for i, baseline in enumerate(baseline_names):
        offset = int(i / 4) * spacing
        adjusted_x = x - int(len(baseline_names) / 2) * width + i * width + offset
        # ax.bar(adjusted_x, result[i], width=width, label=baseline, color=colors[i % len(colors)], hatch=patterns[i % len(patterns)])

        # bar1 = ax.bar(adjusted_x, [res[0] for res in result[i]], width=width, color=colors[i % len(colors)], hatch=patterns[i % len(patterns)], alpha=0.5, edgecolor='black', linestyle='--')
        bar1 = ax.bar(adjusted_x, [res[0] for res in result[i]], width=width, color=colors[i % len(colors)], hatch=patterns[4], alpha=1.0, edgecolor='black', linestyle='-.')

        bar2 = ax.bar(adjusted_x, [res[1] for res in result[i]], width=width, bottom=[res[0] for res in result[i]], color=colors[i % len(colors)], hatch=patterns[5], edgecolor='black', linestyle='-')
        bars.append(bar2)  

    ax.set_ylim(bottom=bottom)
    if top:
        ax.set_ylim(top=top)
    if y_label:
        ax.set_ylabel(y_label, fontsize=label_size)
    ax.set_xticks(x + spacing * (len(baseline_names) // 4 - 1) / 2) 
    ax.set_xticklabels(datasets, fontsize=label_size)
    ax.tick_params(axis='x', labelsize=label_size)
    ax.tick_params(axis='y', labelsize=label_size)
    ax.set_title(title, fontsize=label_size)
    
    if is_log:
        ax.set_yscale('log')
    
    # legend = ax.legend([bar[0] for bar in bars], loc='upper center', bbox_to_anchor=(1.1, 1), fontsize=legend_size, ncol=1)
    
    from matplotlib.patches import Patch
    io_legend_elements = [Patch(facecolor="white", alpha=1.0, edgecolor='black', hatch=patterns[4], linestyle='-', label=legend_labels[0]),
                          Patch(facecolor="white", alpha=1.0, edgecolor='black', hatch=patterns[5], linestyle='-.', label=legend_labels[1])]
    # IO_legend = ax.legend(handles=io_legend_elements, loc='upper left', bbox_to_anchor=(0.1, 1), fontsize=legend_size, title="I/O Type")
    IO_legend = ax.legend(handles=io_legend_elements, loc='upper left', bbox_to_anchor=(0.01, 1), fontsize=legend_size, ncol=2, frameon=False)
    if legend_location == "right":
        IO_legend = ax.legend(handles=io_legend_elements, loc='upper right', bbox_to_anchor=(1.01, 1), fontsize=legend_size, ncol=2, frameon=False)
        
    ax.add_artist(IO_legend)

    # legend = ax.legend([bar[0] for bar in bars], baseline_names, loc='upper center', bbox_to_anchor=(1.1, 1), fontsize=legend_size, ncol=1)
    # ax.add_artist(legend)
    
    bar_legend_elements = [Patch(facecolor=colors[i % len(colors)], alpha=1.0, label=baseline_names[i]) for i in range(len(baseline_names))]
    legend = ax.legend(
        # [bar[0] for bar in bars],
        bar_legend_elements,
        baseline_names,
        loc='upper center',
        bbox_to_anchor=(1.11, 1.05),
        fontsize=legend_size,
        ncol=1,
        borderaxespad=0.5,  # Border padding
        handletextpad=0.5,  # Padding between legend marker and text
        labelspacing=0.3    # Vertical space between legend entries
    )
    
    plt.setp(legend.get_title(), fontsize=legend_size)
    
    plt.tight_layout()
    
    if output_file_paths:
        for output_file_path in output_file_paths:
            if output_file_path.endswith(".pdf"):
                plt.savefig(output_file_path, format='pdf', bbox_inches='tight')
            if output_file_path.endswith(".png"):
                plt.savefig(output_file_path, format='png', bbox_inches='tight')

    
    plt.show()
    plt.close(fig)



def plot_hist_stack_mirrored(datasets, baseline_names, result, y_label="", is_legend=True, is_log=False, title="", output_file_paths=None, bottom1=None, top1=None, bottom2=None, top2=None,legend_labels=[], legend_location="top"):
    
    fig_height = fig_height_legend if is_legend else fig_height_no_legend

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(fig_width, fig_height), sharex=True, gridspec_kw={'height_ratios': [1, 1], 'hspace': 0})
    
    width = width_total / len(baseline_names)
    x = np.arange(len(datasets))
    group_width = len(baseline_names) * width 
    bars = []

    plt.minorticks_on()
    ax1.minorticks_on()
    ax2.minorticks_on()
    
    # Top plot (ax1)
    for i, baseline in enumerate(baseline_names):
        offset = int(i / 4) * spacing
        adjusted_x = x - int(len(baseline_names) / 2) * width + i * width + offset
        bar1 = ax1.bar(adjusted_x, [res[0] for res in result[i]], width=width, color=colors[i % len(colors)], hatch=patterns[i], alpha=1.0, edgecolor='black', linestyle='-.')
        # bar2 = ax1.bar(adjusted_x, [res[1] for res in result[i]], width=width, bottom=[res[0] for res in result[i]], color=colors[i % len(colors)], hatch=patterns[5], edgecolor='black', linestyle='-')
        # bars.append(bar2)  

    ax1.set_ylabel(legend_labels[0], fontsize=label_size)
    ax1.set_title(title, fontsize=label_size)
    ax1.tick_params(axis='x', labelsize=label_size)
    ax1.tick_params(axis='y', labelsize=label_size)
    if bottom1:
        ax1.set_ylim(bottom=bottom1)
    if top1:
        ax1.set_ylim(top=top1)
    

    # Bottom plot (ax2) with inverted y-axis
    for i, baseline in enumerate(baseline_names):
        offset = int(i / 4) * spacing
        adjusted_x = x - int(len(baseline_names) / 2) * width + i * width + offset
        # bar1 = ax2.bar(adjusted_x, [res[0] for res in result[i]], width=width, color=colors[i % len(colors)], hatch=patterns[4], alpha=1.0, edgecolor='black', linestyle='-.')
        bar2 = ax2.bar(adjusted_x, [res[1] for res in result[i]], width=width, color=colors[i % len(colors)], hatch=patterns[i], edgecolor='black', linestyle='-')
        # bars.append(bar2)  

    ax2.invert_yaxis()  # Invert the y-axis for the mirrored effect
    if bottom2:
        ax2.set_ylim(bottom=top2)
    if top2:
        ax2.set_ylim(top=bottom2)
    # ax2.set_ylim(bottom2, top2)
    ax2.set_ylabel(legend_labels[1], fontsize=label_size)
    # ax2.set_xlabel("Datasets", fontsize=label_size)
    ax2.tick_params(axis='x', labelsize=label_size)
    ax2.tick_params(axis='y', labelsize=label_size)
    ax2.set_xticks(x)
    ax2.set_xticklabels(datasets, fontsize=label_size)

    if is_log:
        ax1.set_yscale('log')
        ax2.set_yscale('log')

    from matplotlib.patches import Patch
    # io_legend_elements = [Patch(facecolor="white", alpha=1.0, edgecolor='black', hatch=patterns[4], linestyle='-', label=legend_labels[0]),
                        #   Patch(facecolor="white", alpha=1.0, edgecolor='black', hatch=patterns[5], linestyle='-.', label=legend_labels[1])]
    # IO_legend = ax1.legend(handles=io_legend_elements, loc='upper left', bbox_to_anchor=(0.01, 1), fontsize=legend_size, ncol=2, frameon=False)
    # if legend_location == "right":
    #     IO_legend = ax1.legend(handles=io_legend_elements, loc='upper right', bbox_to_anchor=(1.01, 1), fontsize=legend_size, ncol=2, frameon=False)
        
    # ax1.add_artist(IO_legend)
    
    if is_legend:
        bar_legend_elements = [Patch(facecolor=colors[i % len(colors)], alpha=1.0, hatch=patterns[i], label=baseline_names[i]) for i in range(len(baseline_names))]
        if legend_location == 'right':
            legend = ax1.legend(
                bar_legend_elements,
                baseline_names,
                loc='upper center',
                bbox_to_anchor=(1.11, 1.05),
                fontsize=legend_size,
                ncol=1,
                borderaxespad=0.5,  # Border padding
                handletextpad=0.5,  # Padding between legend marker and text
                labelspacing=0.3    # Vertical space between legend entries
            )
        if legend_location == 'top':
            legend = plt.legend(
                loc='upper center',           # Place the legend at the top
                bbox_to_anchor=(0.5, 1.15),   # Adjust position to move it outside the plot area if needed
                ncol=6,                       # Number of columns
                frameon=False,                # Optional: remove the border around the legend
                handlelength=1,               # Adjusts the length of the legend handles
                handletextpad=0.3,            # Reduces the space between handle and text
                columnspacing=0.5   
            )
    
        plt.setp(legend.get_title(), fontsize=legend_size)
    
    plt.tight_layout()
    
    if output_file_paths:
        for output_file_path in output_file_paths:
            if output_file_path.endswith(".pdf"):
                plt.savefig(output_file_path, format='pdf', bbox_inches='tight')
            if output_file_path.endswith(".png"):
                plt.savefig(output_file_path, format='png', bbox_inches='tight')

    plt.show()
    plt.close(fig)


def plot_line(datasets, baseline_names, result, x_label="", y_label="", is_log=False, title="", output_file_paths=None, bottom=None, top=None):
    label_size = 24
    legend_size = 20
    
    fig, ax = plt.subplots(figsize=(12, 4))
    x = np.arange(len(datasets))
    
    spacing = 0.02

    markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'x', '+']
    linestyles = ['-', '--', '-.']
    combinations = [(m, ls) for m in markers for ls in linestyles]
    for i, baseline in enumerate(baseline_names):
        offset = int(i / 4) * spacing
        adjusted_x = x + offset
        ax.plot(adjusted_x, result[i], label=baseline, marker=markers[i], linestyle=linestyles[i%len(linestyles)], color=colors[i % len(colors)], markersize=10)

    # colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#C2C2F0','#FFA07A', '#B0E0E6', '#FFD700', '#D3D3D3']

    if bottom:
        ax.set_ylim(bottom=bottom)
    if top:
        ax.set_ylim(top=top)
    ax.set_ylabel(y_label, fontsize=label_size)
    ax.set_xlabel(x_label, fontsize=label_size)
    ax.set_xticks(x + spacing * (len(baseline_names) // 4 - 1) / 2)
    ax.set_xticklabels(datasets, fontsize=label_size)
    ax.tick_params(axis='x', labelsize=label_size)
    ax.tick_params(axis='y', labelsize=label_size)

    ax.set_title(title, fontsize=label_size)
    
    if is_log:
        ax.set_yscale('log')
    
    # legend = ax.legend(loc='upper center', bbox_to_anchor=(1.1, 1), fontsize=legend_size, ncol=1)
    
    legend = ax.legend(
        loc='upper center',
        bbox_to_anchor=(1.12, 1.05),
        fontsize=legend_size,
        ncol=1,
        borderaxespad=0.5,  # Border padding
        handletextpad=0.5,  # Padding between legend marker and text
        labelspacing=0.3    # Vertical space between legend entries
    )
    
    plt.setp(legend.get_title(), fontsize=legend_size)
    
    plt.tight_layout()
    
    if output_file_paths:
        for output_file_path in output_file_paths:
            if output_file_path.endswith(".pdf"):
                plt.savefig(output_file_path, format='pdf', bbox_inches='tight')
            if output_file_path.endswith(".png"):
                plt.savefig(output_file_path, format='png', bbox_inches='tight')
    
    plt.show()
    plt.close(fig)


def plot_scatter(sizes, baseline_names, x, y, highlight_x=[], highlight_y=[], ax=None, x_label="", y_label="", yticks=[], is_log=False, title="", output_file_paths=None, x_bottom=None, x_top=None, y_bottom=None, y_top=None, show_legend=False, is_x_ticks=False, is_y_ticks=True):
    label_size = 28
    legend_size = 22

    # if show_legend:
    #     # fig, ax = plt.subplots(figsize=(8, 4))
    #     fig, ax = plt.subplots(figsize=(8 * 0.75, 4))
    # else:
    #     fig, ax = plt.subplots(figsize=(8 * 0.75, 4))
    if ax is None:
        fig, ax = plt.subplots(figsize=(8 * 0.75, 4))

    markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'x', '+']
    colors = plt.cm.tab10.colors  # Add a color palette
    for i, baseline in enumerate(baseline_names):
        # print(i, x[i], sizes)
        for j in range(len(x[i])):
            # marker_size = 40 * np.log(sizes[j] / 1000)
            marker_size = 100
            ax.scatter(x[i][j], y[i][j], label=baseline, marker=markers[i % len(markers)], color=colors[i % len(colors)], facecolors='none', s=marker_size)

        for j in range(len(highlight_x[i])):
            # marker_size = 40 * np.log(sizes[j] / 1000)
            marker_size = 100
            ax.scatter(highlight_x[i][j], highlight_y[i][j], label=baseline, marker=markers[i % len(markers)], color=colors[i % len(colors)], s=marker_size)

    if x_bottom is not None:
        ax.set_xlim(left=x_bottom)
    if x_top is not None:
        ax.set_xlim(right=x_top)
    if y_bottom is not None:
        ax.set_ylim(bottom=y_bottom)
    if y_top is not None:
        ax.set_ylim(top=y_top)
        
    ax.set_ylabel(y_label, fontsize=label_size)
    ax.set_xlabel(x_label, fontsize=label_size)
    ax.tick_params(axis='x', labelsize=label_size + 2)
    ax.tick_params(axis='y', labelsize=label_size + 2)

    ax.set_title(title, fontsize=label_size + 2)
    
    if is_log:
        ax.set_yscale('log')
        ax.set_xscale('log')
    
    if show_legend:
        scatter_legend_element_1 = Line2D([0], [0], marker=markers[0], color=colors[0], label=baseline_names[0],
                                          markerfacecolor='none', markersize=10, linestyle='None', markeredgewidth=2)
        
        scatter_legend_element_2 = Line2D([0], [0], marker=markers[1], color=colors[1], label=baseline_names[1],
                                          markerfacecolor='none', markersize=10, linestyle='None', markeredgewidth=2)
        
        scatter_legend_element_3 = Line2D([0], [0], marker=markers[2], color=colors[2], label=baseline_names[2],
                                          markerfacecolor='none', markersize=10, linestyle='None', markeredgewidth=2)
        
        scatter_legend_elements = [scatter_legend_element_1, scatter_legend_element_2, scatter_legend_element_3]
        
        # scatter_legend = ax.legend(
        #     handles=scatter_legend_elements, loc='center left', bbox_to_anchor=(0.95, 0.75), fontsize=legend_size, 
        #     borderaxespad=0.5,  # Border padding
        #     handletextpad=0.5,  # Padding between legend marker and text
        #     labelspacing=0.3,    # Vertical space between legend entries
        #     ncol=1, frameon=False)

        # plt.tight_layout(rect=[0, 0, 0.85, 1])
        legend = ax.legend(
            handles=scatter_legend_elements, 
            loc='upper right',
            # bbox_to_anchor=(1.24, 1.05),
            fontsize=legend_size,
            ncol=1,
            borderaxespad=0.2,  # Border padding
            handletextpad=0.2,  # Padding between legend marker and text
            labelspacing=0.3,    # Vertical space between legend entries
            # frameon=False
        )
    
        plt.setp(legend.get_title(), fontsize=legend_size)

    if yticks:
        ax.set_yticks(yticks)
    if not is_y_ticks:
        ax.set_yticklabels(['' for _ in range(len(yticks))])
    if not is_x_ticks:
        # ax.set_xticklabels(['',''])
        ax.tick_params(labelbottom=False)

    ax.grid(True)  # Add grid
    
    # plt.tight_layout()
    
    if output_file_paths:
        for output_file_path in output_file_paths:
            if output_file_path.endswith(".pdf"):
                plt.savefig(output_file_path, format='pdf', bbox_inches='tight')
            if output_file_path.endswith(".png"):
                plt.savefig(output_file_path, format='png', bbox_inches='tight')
    
    # plt.show()
    # plt.close(fig)

def plot_line_small(datasets, baseline_names, result, x_label="", y_label="", yticks=[], is_log=False, title="", output_file_paths=None, bottom=None, top=None, show_legend=False):
    label_size = 24
    legend_size = 20

    fig, ax = plt.subplots(figsize=(8, 4))
    
    
    # if show_legend:
    #     fig, ax = plt.subplots(figsize=(9, 4))
    # else:
    #     fig, ax = plt.subplots(figsize=(6, 4))
    x = np.arange(len(datasets))
    
    spacing = 0.02

    markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'x', '+']
    linestyles = ['-', '--', '-.']
    combinations = [(m, ls) for m in markers for ls in linestyles]
    for i, baseline in enumerate(baseline_names):
        offset = int(i / 4) * spacing
        adjusted_x = x + offset
        ax.plot(adjusted_x, result[i], label=baseline, marker=markers[i], linestyle=linestyles[i%len(linestyles)], color=colors[i % len(colors)], markersize=10)

    # colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#C2C2F0','#FFA07A', '#B0E0E6', '#FFD700', '#D3D3D3']

    if bottom:
        ax.set_ylim(bottom=bottom)
    if top:
        ax.set_ylim(top=top)
    ax.set_ylabel(y_label, fontsize=label_size + 2)
    ax.set_xlabel(x_label, fontsize=label_size + 2)
    ax.set_xticks(x + spacing * (len(baseline_names) // 4 - 1) / 2)
    ax.set_xticklabels(datasets, fontsize=label_size + 2)
    ax.tick_params(axis='x', labelsize=label_size + 2)
    ax.tick_params(axis='y', labelsize=label_size + 2)

    ax.set_title(title, fontsize=label_size + 2)
    
    if is_log:
        ax.set_yscale('log')
    
    # legend = ax.legend(loc='upper center', bbox_to_anchor=(1.1, 1), fontsize=legend_size, ncol=1)

    # if show_legend:
    #     legend = ax.legend(
    #         loc='upper center',
    #         bbox_to_anchor=(1.24, 1.05),
    #         fontsize=legend_size,
    #         ncol=1,
    #         borderaxespad=0.5,  # Border padding
    #         handletextpad=0.5,  # Padding between legend marker and text
    #         labelspacing=0.3    # Vertical space between legend entries
    #     )

    #     plt.setp(legend.get_title(), fontsize=legend_size)
    #     plt.tight_layout(rect=[0, 0, 0.97, 1])
        
    # else:
    #     plt.tight_layout()
    if show_legend:
        legend = ax.legend(
            loc='upper right',
            # bbox_to_anchor=(1.24, 1.05),
            fontsize=legend_size,
            ncol=4,
            borderaxespad=0.5,  # Border padding
            handletextpad=0.5,  # Padding between legend marker and text
            labelspacing=0.3,    # Vertical space between legend entries
            # frameon=False
        )
    
        plt.setp(legend.get_title(), fontsize=legend_size)

    plt.tight_layout()
    
    if output_file_paths:
        for output_file_path in output_file_paths:
            if output_file_path.endswith(".pdf"):
                plt.savefig(output_file_path, format='pdf', bbox_inches='tight')
            if output_file_path.endswith(".png"):
                plt.savefig(output_file_path, format='png', bbox_inches='tight')
    
    plt.show()
    plt.close(fig)


# def plot_percentail(QueryPercentage, baselines, display_baselines, xlabel, ylabel, is_log, is_legend, output_file_paths):
#     # Sample data
#     markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'x', '+']
#     x = np.arange(1, 100)  # X-axis from 1 to 100
    
#     # Create plot
#     plt.figure(figsize=(14, 4))
    
#     # Plot each baseline with a unique marker and color
#     for i, baseline in enumerate(baselines):
#         baseline_on_us = QueryPercentage[baseline][0]
        
#         # Plot the full line without markers
#         plt.plot(x, baseline_on_us, color=colors[i], linewidth=4, label=display_baselines[i])
    
#         # Add markers at every 10th point
#         plt.plot(x[::10], baseline_on_us[::10], color=colors[i], marker=markers[i % len(markers)], 
#                  linestyle='None', markersize=10)  # Only markers, no line
    
#         # Add marker at the last point
#         plt.plot(x[-1:], baseline_on_us[-1:], color=colors[i], marker=markers[i % len(markers)], 
#                  linestyle='None', markersize=10)  # Only marker at the last point
#     if is_log:
#         plt.yscale('log')
#     if xlabel:
#         plt.xlabel(xlabel, fontsize=label_size)
#     if ylabel:
#         plt.ylabel(ylabel, fontsize=label_size)
#     plt.tick_params(axis='x', labelsize=label_size)
#     plt.tick_params(axis='y', labelsize=label_size)
    
#     # Show legend
#     if is_legend:
#         # plt.legend(ncol=3, 
#         #         loc='upper left',
#         #         # bbox_to_anchor=(1.24, 1.05),
#         #         fontsize=legend_size,
#         #         borderaxespad=0.3,  # Border padding
#         #         handletextpad=0.3,  # Padding between legend marker and text
#         #         labelspacing=0.3,    # Vertical space between legend entries
#         #         frameon=False
#         #         )
#         plt.legend(
#             loc='upper center',          
#             bbox_to_anchor=(0.5, 1.37),  
#             ncol=6,                      
#             frameon=False,     
#             fontsize=legend_size,
#             borderaxespad=0.2,
#             handletextpad=0.2,
#             labelspacing=0.2,
#         )
    
#     # Show grid
#     plt.grid(True, linestyle="--")
    
#     if output_file_paths:
#         for output_file_path in output_file_paths:
#             if output_file_path.endswith(".pdf"):
#                 plt.savefig(output_file_path, format='pdf', bbox_inches='tight')
#             if output_file_path.endswith(".png"):
#                 plt.savefig(output_file_path, format='png', bbox_inches='tight')
    
#     plt.show()

def plot_percentail(QueryPercentage, baselines, display_baselines, xlabel, ylabel, is_log, is_legend, output_file_paths):
    # Sample data
    # markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'x', '+']
    markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'x', '+', 'h', 'H', '|']
    linestyles = ['-', '--', ':', '-.']
    x = np.arange(1, 100)  # X-axis from 1 to 100
    
    fig_height = fig_height_legend if is_legend else fig_height_no_legend

    plt.figure(figsize=(16, fig_height))
    handles = []  # Store handles for legend
    
    for i, baseline in enumerate(baselines):
        baseline_on_us = QueryPercentage[baseline][0]
        
        # Plot the line without markers
        linestyle = linestyles[i % len(linestyles)]
        line, = plt.plot(x, baseline_on_us, color=colors[i], linewidth=2)
        
        # Add markers at every 10th point
        plt.plot(x[::10], baseline_on_us[::10], color=colors[i], marker=markers[i % len(markers)], 
                 linestyle='None', markersize=10)
        
        # Add marker at the last point
        plt.plot(x[-1:], baseline_on_us[-1:], color=colors[i], marker=markers[i % len(markers)], 
                 linestyle='None', markersize=10)
        
        # Create a handle for the legend using the line and marker
        handles.append(plt.Line2D([0], [0], color=colors[i], marker=markers[i % len(markers)], 
                                  linewidth=4, markersize=10, label=display_baselines[i]))
    
    if is_log:
        plt.yscale('log')
    if xlabel:
        plt.xlabel(xlabel, fontsize=label_size)
    if ylabel:
        plt.ylabel(ylabel, fontsize=label_size)
    plt.tick_params(axis='x', labelsize=label_size)
    plt.tick_params(axis='y', labelsize=label_size)
    
    if is_legend:
        # Use custom handles with markers for the legend
        plt.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.465, 1.25), 
                   ncol=6, frameon=False, fontsize=legend_size - 2, 
                   borderaxespad=0.15, handletextpad=0.15, labelspacing=0.15)
    
    plt.grid(True, linestyle="--")
    
    if output_file_paths:
        for output_file_path in output_file_paths:
            if output_file_path.endswith(".pdf"):
                plt.savefig(output_file_path, format='pdf', bbox_inches='tight')
            if output_file_path.endswith(".png"):
                plt.savefig(output_file_path, format='png', bbox_inches='tight')
    
    plt.show()
