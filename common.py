sequence = [
    '$\\alpha$-MOC-SCBDS-C-4',
    '$\\alpha$-MOC-SCBDS-C-3',
    'Heuristic SCBDS 4 hops',
    'Heuristic SCBDS 3 hops',
]

keys = ['N', 'Case', 'BDS Size', 'SCBDS Size', 'ARPL', 'Max Ratio']

header_format = '{:24} {:>8} {:>8} {:>8} {:>8} {:>8} {:>10} {:>10}'

row_format = '{:>24} {:8} {:8} {:8} {:8} {:8.3f} {:10} {:3}m{:5.2f}s'


def text(f):
    return f.replace('$', '').replace('\\', '')


def message(msg):
    print()
    print(msg)
    print()
