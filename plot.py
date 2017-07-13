import csv
import matplotlib.pyplot as plt
import os
import sys

from common import (
    keys,
    message,
    sequence,
    text
)
from setting import (
    nums,
    output_folder,
    rhos,
    r_mins,
)


def get_subplots(title, xlabel, ylabel):
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return fig, ax


def plot(ax, x, y, label, loc):
    ax.plot(x, y, label=label)
    ax.scatter(x, y)
    ax.legend(loc=loc)


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 3:
        message('Usage: python plot.py <r_min> <rho>')
        return

    r_min = int(sys.argv[1])
    rho = float(sys.argv[2])
    if r_min not in r_mins or rho not in rhos:
        message('Error: r_min={}, rho={} does not match setting'.format(
            r_min, rho)
        )
        return

    path = os.path.join(output_folder,
                        'r_min{}rho{}'.format(r_min, rho),
                        'nums{}-{}'.format(nums[0], nums[-1]))
    size_fig, size_ax = get_subplots(
        '$r_{{min}} = {}, \\rho = {:.2f}$'.format(r_min, rho),
        'Number of Nodes',
        'Average SCBDS Size'
    )
    length_fig, length_ax = get_subplots(
        '$r_{{min}} = {}, \\rho = {:.2f}$'.format(r_min, rho),
        'Number of Nodes',
        'Average Routing Path Length'
    )
    for c in map(text, sequence):
        data = {str(n): {k: [] for k in keys[1:]} for n in nums}
        with open(os.path.join(path, '{}.csv'.format(c))) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for k in keys[1:]:
                    data[row['N']][k].append(row[k])
        sizes = []
        lengths = []
        for n in nums:
            size = list(map(int, data[str(n)]['SCBDS Size']))
            sizes.append(sum(size) / len(size))
            length = list(map(float, data[str(n)]['ARPL']))
            lengths.append(sum(length) / len(length))
        plot(size_ax, nums, sizes, c, 'upper left')
        plot(length_ax, nums, lengths, c, 'upper right')
    plt.show()


if __name__ == '__main__':
    main()
