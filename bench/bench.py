# Dagger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Dagger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Dagger.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2012 Remik Ziemlinski
#
# ==========
# Hall of Fame
#
# 960799 nodes
# 6.22s Run allpaths=None levels=7 cross=0 hash=None width=7

import optparse
import time

import dagger


def GetOpt():
    desc = """Benchmark graph evaluation."""
    parser = optparse.OptionParser(description=desc)

    parser.add_option(
        '-a',
        '--allpaths',
        help="Find all paths in graph.",
        action="store_true"
    )
    parser.add_option('--dot', help='Output dot graph file to visualize.')
    parser.add_option(
        '--cross',
        help='Cross dependencies so inner nodes parent all node in next level.',
        action="store_true"
    )
    parser.add_option(
        '--hash',
        help='Use text based hash db.',
        action="store_true"
    )
    parser.add_option(
        '--hashsql',
        help='Use sqlite hash db.',
        action="store_true"
    )
    parser.add_option(
        "-l",
        "--levels",
        help="How many levels to make mock graph tree.",
        default='2'
    )
    parser.add_option(
        '-w',
        '--width',
        help='How many children a node should have.',
        default='2'
    )
    opts, args = parser.parse_args()
    opts = vars(opts)

    return opts


######################################################################
def children(p, width):
    """Return list of child ids for parent id p."""
    i0 = (p + 1) * width
    i1 = i0 + width
    return range(i0, i1)


######################################################################
def otherchildren(p, levels, width):
    existing = children(p, width)

    pseries = [
        sum([width**i for i in range(1, lev + 1)])
        for lev in range(1, levels + 1)
    ]

    lev = 1
    # Find level node p is in.
    for z in pseries:
        if p < z:
            break
        lev += 1

    if lev >= len(pseries):
        return []

    # Choose other children.
    out = []
    for i in range(pseries[lev - 1], pseries[lev]):
        if i not in existing:
            out.append(i)

    return out


######################################################################
opt = GetOpt()
allpaths = opt.get('allpaths')
hash = opt.get('hash')
hashsql = opt.get('hashsql')
cross = opt.get('cross')
levels = int(opt.get('levels'))
dot = opt.get('dot')
width = int(opt.get('width'))

tBuild = 0
tRun = 0

# ---------------------------------------------------------------------
# Build basic graph.
tic = time.clock()
dag = dagger.dagger()

nInner = sum([width**i for i in range(1, levels)])
nOuter = width**levels  # Leaves.
print(f'nodes: inner={nInner} outer={nOuter} total={nInner+nOuter}')

# Add nodes with children.
for p in range(0, nInner):
    dag.add(str(p), map(str, children(p, width)))

# Force last node stale to get side effects.
dag.stale(str(nInner + nOuter - 1))

# Add optional cross links so graph isn't simple k-trees.
if cross:
    for p in range(0, nInner):
        other = otherchildren(p, levels, width)
        dag.add(str(p), map(str, other))

toc = time.clock()
tBuild = toc - tic

# ---------------------------------------------------------------------
tic = toc
dag.run(allpaths=allpaths)

toc = time.clock()
tRun = toc - tic

# ---------------------------------------------------------------------
print(f'{tBuild}s Build allpaths={allpaths} levels={levels} cross={cross} hash={hash} width={width}')
print(f'{tBuild}s Run allpaths={allpaths} levels={levels} cross={cross} hash={hash} width={width}')

if dot:
    dag.dot(dot)
