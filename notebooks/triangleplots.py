import numpy as np
import ternary
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable


def subset(motifs, duration, min_dur=0, max_dur=np.inf, limit=-1, shuffle=True):
    """Select a subset of triplets (motifs): select only those motifs whose
    duration is between the minimum and maximum duration (min_dur, max_ddur),
    limit to a certain number of motifs, and optionally shuffle the motifs.
    """
    match = (duration >= min_dur) & (duration <= max_dur)
    index = np.arange(len(motifs))[match]
    if limit == -1 or limit > len(index):
        limit = len(index)
    if shuffle: 
        index = np.random.choice(index, size=limit, replace=False)
    else:
        index = index[:limit]
    if len(index) == 0:
        raise Warning(f'The filter returns no motifs (min_dur={min_dur}, max_dur={max_dur}, limit={limit})')
    return motifs[index, :], duration[index], index


# Styling of rhythm plot
def setup_rhythm_plot(scale, subdiv=4, grid=False, grid_kws={}, label_offset=.05, ax=None):
    if ax is None: ax = plt.gca()
    kws = dict(linestyle=':')
    _grid_kws = dict(
        color='k', linewidth=0.5, 
        left_kwargs=kws, right_kwargs=kws, horizontal_kwargs=kws
    )
    _grid_kws.update(grid_kws)
    multiple = scale / subdiv

    figure, tax = ternary.figure(scale=scale, ax=ax)
    figure.dpi = 150
    ax.axis('equal')
    ax.set_axis_off()
    tax.boundary(linewidth=0.5)
    
    if grid:
        tax.gridlines(multiple=multiple, **_grid_kws)

    if subdiv > 1:
        ticks = [f'{x:.2f}' for x in np.linspace(0, 1, subdiv+1)]
        tax.ticks(axis='lbr', multiple=multiple, offset=.02, lw=0.5, ticks=ticks, fontsize=6)
        label_offset += 0.1
        
    tax.right_axis_label('interval 2', fontsize=7, offset=label_offset)
    tax.left_axis_label('interval 3', fontsize=7, offset=label_offset)
    tax.bottom_axis_label('interval 1', fontsize=7, offset=label_offset)
    return figure, tax

def show_integer_ratios(tax, scale, factors=[1, 2, 3], color='k'):
    from itertools import product
    
    points = dict()
    for a, b, c in product(factors, factors, factors):
        total = a + b + c
        point = (a/total, b/total, c/total)
        if point not in points.keys():
            points[point] = (a, b, c)

    for point, (a, b, c) in points.items():
        point = np.array(point) * scale
        tax.scatter([point], marker='+', s=8, color=color, linewidth=0.25)
        tax.annotate(f'{a}{b}{c}', point, color=color,
            ha='center', va='bottom', fontsize=4.5,
            xytext=(0, 1), textcoords='offset points')

# fig, tax = setup_rhythm_plot(scale=60, subdiv=4, grid=True)
# show_integer_ratios(tax, scale=60, factors=[1, 2, 3, 4])

# Color by cycle duration
def show_triangle_scatter(motifs, duration, 
        min_dur=0.1, max_dur=0.8, limit=30000, 
        s=1, alpha=.3, jitter=0,
        scale=60, subdiv=1, ratios=True, ratios_kws={}, 
        cmap='plasma_r', colorbar=True, vmin=None, vmax=None, ax=None,
        colorbar_label='duration (quarter)'
    ):
    if ax is None: ax = plt.gca()
    if 0 <= min_dur <= 1: min_dur = np.quantile(duration, min_dur).astype(int)
    if 0 <= max_dur <= 1: max_dur = np.quantile(duration, max_dur).astype(int)
    if vmin is None: vmin = min_dur
    if vmax is None: vmax = max_dur
    norm = Normalize(vmin=vmin, vmax=vmax)

    X, dur, _ = subset(motifs, duration, min_dur=min_dur, max_dur=max_dur, limit=limit)
    X = X + jitter * np.random.normal(0, 1, size=X.shape)
    X *= scale

    fig, tax = setup_rhythm_plot(scale, subdiv, ax=ax)
    tax.scatter(X, s=s, alpha=alpha, c=dur, norm=norm, vmin=None, vmax=None, cmap=cmap, lw=0)
    if colorbar:
        mappable = ScalarMappable(norm=norm, cmap=cmap)
        fig.colorbar(mappable, ax=ax, label=colorbar_label)
    if ratios:
        show_integer_ratios(tax, scale, [1, 2, 3], **ratios_kws)
    return fig, tax