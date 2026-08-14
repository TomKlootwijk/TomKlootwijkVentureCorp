from __future__ import annotations

from pathlib import Path
import math
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Polygon, Arc, Rectangle
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
sys.path.insert(0, str(SRC))

from ugts.glyphs import loop_to_r_morph  # noqa: E402
from ugts.math2d import Vec2  # noqa: E402
from ugts.numeric import active_bit_positions, pascal_entry_is_odd  # noqa: E402

OUT = ROOT / 'diagrams'

NAVY = '#0B2638'
TEAL = '#168F9C'
GOLD = '#D8A124'
CORAL = '#D76959'
PURPLE = '#786AA3'
GREEN = '#2A8C6D'
LIGHT = '#EDF4F5'
LIGHT2 = '#F7FAFA'
MID = '#AFC6CD'
DARK = '#1A2E38'
GRAY = '#60747C'
WHITE = '#FFFFFF'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.titlesize': 14,
    'axes.labelsize': 10,
    'figure.facecolor': 'white',
    'savefig.facecolor': 'white',
})


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(OUT / f'{name}.pdf', bbox_inches='tight')
    fig.savefig(OUT / f'{name}.png', dpi=220, bbox_inches='tight')
    plt.close(fig)


def box(ax, xy, w, h, text, *, fc=LIGHT, ec=TEAL, lw=1.5, text_color=DARK, fontsize=10, radius=0.025, z=2):
    p = FancyBboxPatch(xy, w, h, boxstyle=f'round,pad=0.012,rounding_size={radius}',
                       fc=fc, ec=ec, lw=lw, zorder=z)
    ax.add_patch(p)
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha='center', va='center',
            color=text_color, fontsize=fontsize, zorder=z + 1, wrap=True)
    return p


def arrow(ax, a, b, *, color=GRAY, lw=1.6, style='-|>', curve=0.0, z=1):
    p = FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=12, lw=lw,
                        color=color, connectionstyle=f'arc3,rad={curve}', zorder=z)
    ax.add_patch(p)
    return p


def title(ax, main, sub=None):
    ax.text(0.0, 1.02, main, transform=ax.transAxes, ha='left', va='bottom',
            fontsize=17, fontweight='bold', color=NAVY)
    if sub:
        ax.text(0.0, 0.985, sub, transform=ax.transAxes, ha='left', va='top',
                fontsize=10.5, color=GRAY)


def architecture_overview():
    fig, ax = plt.subplots(figsize=(12, 7.2))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    title(ax, 'UGTS-0 architecture', 'Authoritative relation/event substrate with optional projection and hardware adapters')

    # Layer bands
    ax.add_patch(Rectangle((0.02, 0.66), 0.96, 0.24, fc='#E6F2F3', ec='none'))
    ax.add_patch(Rectangle((0.02, 0.35), 0.96, 0.24, fc='#F5F1E8', ec='none'))
    ax.add_patch(Rectangle((0.02, 0.04), 0.96, 0.24, fc='#F3EEF5', ec='none'))
    ax.text(0.035, 0.875, 'AUTHORITATIVE SUBSTRATE', fontsize=10, fontweight='bold', color=TEAL)
    ax.text(0.035, 0.565, 'QUERY / RUNTIME', fontsize=10, fontweight='bold', color=GOLD)
    ax.text(0.035, 0.255, 'ADAPTERS', fontsize=10, fontweight='bold', color=PURPLE)

    xs = [0.08, 0.255, 0.43, 0.605, 0.78]
    top = [
        ('Finite grammar', 'bounded rules\nand parameters'),
        ('Typed state Q', 'x, t, phase, sheet,\norientation, lineage'),
        ('Relations R_j=0', 'implicit surfaces\nand guards'),
        ('Topology + identity', 'gluing maps, invariants,\nbranches, ancestry'),
        ('External event log', 'irreducible novelty,\nconfidence, schema'),
    ]
    for x, (a, b) in zip(xs, top):
        box(ax, (x, 0.70), 0.145, 0.14, f'{a}\n{b}', fc=WHITE, ec=TEAL, fontsize=9.2)
    for i in range(len(xs)-1):
        arrow(ax, (xs[i]+0.145, 0.77), (xs[i+1], 0.77), color=TEAL)

    runtime = [
        ('Support admission', 'local radial-angular\nspace/time scope'),
        ('Compatibility', 'phase / sheet / policy\nreason codes'),
        ('Event solver', 'earliest valid root\nanalytic or bracketed'),
        ('Transition router', 'state patch + lineage\npre/post record'),
    ]
    rxs = [0.12, 0.335, 0.55, 0.765]
    for x, (a, b) in zip(rxs, runtime):
        box(ax, (x, 0.405), 0.17, 0.125, f'{a}\n{b}', fc=WHITE, ec=GOLD, fontsize=9.2)
    for i in range(3):
        arrow(ax, (rxs[i]+0.17, 0.467), (rxs[i+1], 0.467), color=GOLD)
    arrow(ax, (0.33, 0.70), (0.205, 0.53), color=GRAY, curve=0.15)
    arrow(ax, (0.50, 0.70), (0.63, 0.53), color=GRAY, curve=-0.12)
    arrow(ax, (0.835, 0.53), (0.85, 0.70), color=GRAY, curve=-0.12)

    adapters = [
        ('Game / ECS', 'motion, CCD, sensors,\nportals, rollback'),
        ('Graphics', 'SDF, log-polar LUT,\n1-bit jitter / shader'),
        ('Hardware B.C.E.', 'liquid coupler, mode,\nmeasured guard'),
    ]
    axs = [0.16, 0.415, 0.67]
    for x, (a, b) in zip(axs, adapters):
        box(ax, (x, 0.09), 0.20, 0.12, f'{a}\n{b}', fc=WHITE, ec=PURPLE, fontsize=9.2)
        arrow(ax, (x+0.10, 0.405), (x+0.10, 0.21), color=PURPLE)

    ax.text(0.5, 0.015, 'Projection is optional and non-authoritative. One-bit values are schema-bound flags, not complete state.',
            ha='center', va='bottom', color=CORAL, fontsize=10, fontweight='bold')
    save(fig, 'architecture_overview')


def state_event_formalism():
    fig, ax = plt.subplots(figsize=(12, 7.2))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    title(ax, 'State and event formalism', 'The mature corpus becomes a typed compatibility-gated event calculus')

    box(ax, (0.05, 0.66), 0.40, 0.20,
        r'$q_e(t) = (x_e(t),\ t,\ \phi_e(t),\ \sigma_e(t),\ a_e,\ b_e)$' +
        '\n\nposition | time | phase\nsheet/orientation | lineage | branch',
        fc=LIGHT, ec=TEAL, fontsize=10.8)
    box(ax, (0.55, 0.66), 0.40, 0.20,
        r'$W=(G,\,R,\,T,\,I,\,L)$' +
        '\n\ngrammar  relations  transitions\ninvariants  external log',
        fc='#F5F1E8', ec=GOLD, fontsize=12)

    # Conditions
    box(ax, (0.05, 0.42), 0.25, 0.13, 'Relation root\n' + r'$R_j(q;\theta_j)=0$', fc=WHITE, ec=CORAL, fontsize=12)
    box(ax, (0.375, 0.42), 0.25, 0.13, 'Inside support\n' + r'$C_\alpha(q,t)\leq 0$', fc=WHITE, ec=TEAL, fontsize=12)
    box(ax, (0.70, 0.42), 0.25, 0.13, 'Compatible sector\n' + r'$\chi(e,j,t)=1$', fc=WHITE, ec=PURPLE, fontsize=12)
    for x in (0.175, 0.50, 0.825):
        arrow(ax, (x, 0.42), (0.50, 0.32), color=GRAY, curve=(x-0.5)*0.4)

    box(ax, (0.25, 0.22), 0.50, 0.11,
        r'$t^* = \min\{t>t_0:\ R_j(q_e(t))=0,\ C_\alpha\leq0,\ \chi=1\}$',
        fc=NAVY, ec=NAVY, text_color=WHITE, fontsize=13)
    arrow(ax, (0.50, 0.22), (0.50, 0.12), color=NAVY)
    box(ax, (0.20, 0.035), 0.60, 0.09,
        r'$q_e(t^{*+}) = T_j(q_e(t^{*-}),\ context)$' +
        '\npre-state + reason codes -> state patch + lineage + event record',
        fc='#E9F3EE', ec=GREEN, fontsize=11.5)

    ax.text(0.02, 0.61, 'A valid event requires all three conditions.', color=CORAL, fontweight='bold')
    ax.text(0.98, 0.61, 'Co-location alone is insufficient.', color=PURPLE, fontweight='bold', ha='right')
    save(fig, 'state_event_formalism')


def numeric_fractal():
    fig = plt.figure(figsize=(12, 7.4))
    ax = fig.add_axes([0.05, 0.56, 0.90, 0.34])
    ax.set_xlim(-0.5, 20.5); ax.set_ylim(-0.2, 1.3); ax.axis('off')
    title(ax, 'Numeric seeds: radix thresholds, active bits and Pascal parity',
          'Exact number-system mechanisms are retained; phonetic links remain mnemonics')

    # axis thresholds
    ax.plot([0, 20], [0.32, 0.32], color=NAVY, lw=2)
    for n in range(0, 21):
        ax.plot([n, n], [0.29, 0.35], color=MID, lw=0.8)
    for p in [1, 2, 4, 8, 16]:
        ax.plot([p, p], [0.20, 0.68], color=TEAL, lw=2)
        ax.text(p, 0.72, str(p), ha='center', color=TEAL, fontweight='bold')
    ax.text(10, 0.08, 'binary digit-count thresholds: powers of 2', ha='center', color=GRAY)

    # 19 bits
    bits = f'{19:05b}'
    bx = 6.6
    for i, bit in enumerate(bits):
        c = CORAL if bit == '1' else WHITE
        ax.add_patch(Circle((bx + i*1.25, 1.02), 0.25, fc=c, ec=NAVY, lw=1.3))
        ax.text(bx+i*1.25, 1.02, bit, ha='center', va='center', color=WHITE if bit=='1' else NAVY, fontweight='bold')
    ax.text(12.0, 1.02, '19 = 10011; popcount = 3', va='center', color=NAVY, fontweight='bold')

    # lower panels
    ax2 = fig.add_axes([0.06, 0.07, 0.44, 0.42])
    ax2.set_aspect('equal'); ax2.axis('off')
    pts = np.array([[1.0, 0.0], [0.0, 0.72], [0.0, -0.72]])
    ax2.add_patch(Polygon(pts, closed=True, fc='#D7EEF0', ec=TEAL, lw=2))
    labels = [('bit 4 / weight 16', pts[0]), ('bit 1 / weight 2', pts[1]), ('bit 0 / weight 1', pts[2])]
    for label, p in labels:
        ax2.add_patch(Circle(p, 0.045, fc=CORAL, ec='none'))
        ax2.text(p[0]+0.06, p[1], label, va='center', fontsize=9)
    ax2.set_xlim(-0.35, 1.55); ax2.set_ylim(-1.0, 1.0)
    ax2.set_title('Chosen triangle embedding of three active positions', color=NAVY, fontweight='bold', fontsize=11)

    ax3 = fig.add_axes([0.54, 0.07, 0.40, 0.42])
    rows = 32
    grid = np.zeros((rows, 2*rows-1))
    for n in range(rows):
        x0 = rows - 1 - n
        for k in range(n+1):
            if pascal_entry_is_odd(n, k):
                grid[n, x0 + 2*k] = 1
    ax3.imshow(grid, cmap='binary', interpolation='nearest', aspect='auto')
    ax3.axis('off')
    ax3.set_title('Pascal odd/even parity -> Sierpinski test pattern', color=NAVY, fontweight='bold', fontsize=11)
    ax3.text(0.5, -0.07, r'Correction: zero-based rows $2^k-1$ are all odd, not generic rows $2^k$.',
             transform=ax3.transAxes, ha='center', va='top', color=CORAL, fontsize=9)
    save(fig, 'numeric_fractal')


def glyph_morph():
    fig, axes = plt.subplots(1, 5, figsize=(12.5, 3.4))
    fig.suptitle('Loop/stem to R: boundary edit plus continuous field morph', x=0.04, ha='left',
                 color=NAVY, fontsize=16, fontweight='bold')
    fig.text(0.04, 0.89, 'Source trick: cut/unroll the lower loop into a diagonal leg; topology and interpolation are kept explicit.',
             color=GRAY, fontsize=10)
    xs = np.linspace(-1.1, 1.1, 180)
    ys = np.linspace(-1.1, 1.1, 180)
    X, Y = np.meshgrid(xs, ys)
    for ax, alpha in zip(axes, np.linspace(0, 1, 5)):
        field = loop_to_r_morph(float(alpha))
        Z = np.empty_like(X)
        for iy in range(Y.shape[0]):
            for ix in range(X.shape[1]):
                Z[iy, ix] = field.value(Vec2(float(X[iy, ix]), float(Y[iy, ix])))
        ax.contourf(X, Y, Z, levels=[-10, 0], colors=['#D7EEF0'])
        ax.contour(X, Y, Z, levels=[0], colors=[NAVY], linewidths=2.2)
        ax.axvline(-0.30, color=GOLD, lw=1, ls='--', alpha=0.65)
        ax.set_aspect('equal'); ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.axis('off')
        ax.set_title(f'morph {alpha:.2f}', fontsize=10, color=TEAL)
    fig.text(0.50, 0.02, 'The intermediate blend is a transition field; it is not guaranteed to remain an exact signed-distance function.',
             ha='center', color=CORAL, fontsize=9.5)
    save(fig, 'glyph_morph')


def topology_maps():
    fig, axes = plt.subplots(1, 3, figsize=(13, 5.1))
    fig.suptitle('Topology as explicit state gluing and routing', x=0.04, ha='left', fontsize=16, fontweight='bold', color=NAVY)
    fig.text(0.04, 0.91, 'Non-orientable motifs become quotient maps; double vacuum becomes compatibility-separated co-location.', color=GRAY, fontsize=10)

    # Double vacuum
    ax = axes[0]; ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    ax.set_title('Double vacuum', color=TEAL, fontweight='bold')
    ax.add_patch(Rectangle((0.12,0.16),0.76,0.26,fc='#E8F3F4',ec=TEAL,lw=1.5))
    ax.add_patch(Rectangle((0.12,0.58),0.76,0.26,fc='#F1ECF5',ec=PURPLE,lw=1.5))
    ax.text(0.16,0.79,'sheet 1 / phase B',color=PURPLE,fontweight='bold')
    ax.text(0.16,0.37,'sheet 0 / phase A',color=TEAL,fontweight='bold')
    for y,c in [(0.29,TEAL),(0.71,PURPLE)]:
        ax.add_patch(Circle((0.50,y),0.065,fc=c,ec=NAVY,lw=1.3))
        ax.text(0.50,y,'x',ha='center',va='center',color=WHITE,fontweight='bold')
    ax.plot([0.50,0.50],[0.355,0.645],color=CORAL,lw=2,ls='--')
    ax.text(0.54,0.50,'same coordinate\nno coupling',va='center',color=CORAL,fontweight='bold')
    ax.text(0.50,0.07,'Requires explicit phase/sheet/orientation/address compatibility',ha='center',fontsize=8.7,color=GRAY)

    # Quotient rectangles
    ax = axes[1]; ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    ax.set_title('Mobius and Klein quotient maps', color=TEAL, fontweight='bold')
    # Mobius
    ax.add_patch(Rectangle((0.10,0.57),0.80,0.25,fc=LIGHT2,ec=NAVY,lw=1.4))
    arrow(ax,(0.10,0.79),(0.90,0.79),color=TEAL); arrow(ax,(0.90,0.60),(0.10,0.60),color=TEAL)
    ax.text(0.50,0.695,'Mobius: left/right gluing flips orientation',ha='center',va='center',fontsize=8.7)
    ax.text(0.07,0.80,'+',ha='right',color=TEAL,fontweight='bold'); ax.text(0.93,0.60,'-',ha='left',color=TEAL,fontweight='bold')
    # Klein
    ax.add_patch(Rectangle((0.10,0.18),0.80,0.25,fc=LIGHT2,ec=NAVY,lw=1.4))
    arrow(ax,(0.10,0.40),(0.90,0.40),color=PURPLE); arrow(ax,(0.90,0.21),(0.10,0.21),color=PURPLE)
    arrow(ax,(0.13,0.18),(0.13,0.43),color=GOLD); arrow(ax,(0.87,0.43),(0.87,0.18),color=GOLD)
    ax.text(0.50,0.305,'Klein quotient: one axis flips, the other closes',ha='center',va='center',fontsize=8.7)
    ax.text(0.50,0.08,'Software gluing map; no physical self-assembly claim',ha='center',fontsize=8.7,color=CORAL)

    # Hourglass
    ax = axes[2]; ax.set_xlim(-1,1); ax.set_ylim(-1,1); ax.axis('off'); ax.set_aspect('equal')
    ax.set_title('Four-chamber hourglass router', color=TEAL, fontweight='bold')
    polys = [
        (np.array([[0,0],[0.95,0.25],[0.95,0.95]]),'A','#D9EEF0'),
        (np.array([[0,0],[-0.95,0.25],[-0.95,0.95]]),'B','#E8E1F0'),
        (np.array([[0,0],[-0.95,-0.25],[-0.95,-0.95]]),'C','#F8E8E2'),
        (np.array([[0,0],[0.95,-0.25],[0.95,-0.95]]),'D','#F7EECF'),
    ]
    for pts,label,fc in polys:
        ax.add_patch(Polygon(pts,closed=True,fc=fc,ec=NAVY,lw=1.1))
        c=pts.mean(axis=0); ax.text(c[0],c[1],label,ha='center',va='center',fontweight='bold',color=NAVY)
    ax.add_patch(Circle((0,0),0.07,fc=CORAL,ec=NAVY,lw=1.3))
    ax.text(0,0,'0',ha='center',va='center',color=WHITE,fontweight='bold')
    arrow(ax,(0.55,0.55),(-0.55,-0.55),color=CORAL,curve=0.05)
    ax.text(0,-0.88,'parity=1 can route A -> C; table is explicit',ha='center',fontsize=8.7,color=GRAY)

    fig.tight_layout(rect=[0.02,0.03,0.98,0.88])
    save(fig, 'topology_maps')


def graphics_adapter():
    fig, ax = plt.subplots(figsize=(12.5, 7.2))
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    title(ax, 'Optional graphics adapter', 'The authoritative substrate emits geometry/state; a replaceable adapter projects it to pixels or print')

    stages = [
        ('World query', 'state / relation /\nsupport selection'),
        ('Log-polar chart', r'$\rho=\ln(r/r_0)$'+'\n'+r'$\theta=\mathrm{atan2}(y,x)$'),
        ('1-bit LUT', 'admission mask\nwith explicit core'),
        ('Implicit field', 'SDF / CSG\nzero boundary'),
        ('Phasor coverage', 'oriented subpixel\naccumulation'),
        ('Projection', 'gray / 1-bit /\nPDM / prepress'),
    ]
    xs = np.linspace(0.03,0.82,6)
    colors=[TEAL,TEAL,GOLD,CORAL,PURPLE,GREEN]
    for x,(a,b),c in zip(xs,stages,colors):
        box(ax,(float(x),0.68),0.145,0.15,f'{a}\n{b}',fc=WHITE,ec=c,fontsize=8.8)
    for i in range(5):
        arrow(ax,(xs[i]+0.145,0.755),(xs[i+1],0.755),color=GRAY)

    # Log-polar grid drawing
    axg = fig.add_axes([0.07,0.11,0.28,0.43]); axg.set_aspect('equal'); axg.axis('off')
    for r in np.geomspace(0.08,1.0,8):
        axg.add_patch(Circle((0,0),r,fill=False,ec=TEAL,lw=0.8,alpha=0.8))
    for th in np.linspace(0,2*np.pi,16,endpoint=False):
        axg.plot([0,math.cos(th)],[0,math.sin(th)],color=MID,lw=0.7)
    axg.add_patch(Circle((0,0),0.075,fc=CORAL,ec=NAVY,lw=1))
    axg.text(0,0,'core',ha='center',va='center',fontsize=6.8,color=WHITE)
    axg.set_xlim(-1.08,1.08); axg.set_ylim(-1.08,1.08)
    axg.set_title('Local log-polar address space',fontsize=10,color=NAVY,fontweight='bold')

    # SDF example
    axs = fig.add_axes([0.39,0.11,0.25,0.43]); axs.set_aspect('equal'); axs.axis('off')
    xx=np.linspace(-1.2,1.2,160); yy=np.linspace(-1.2,1.2,160); X,Y=np.meshgrid(xx,yy)
    Z=np.minimum(np.sqrt((X+0.35)**2+Y**2)-0.55, np.maximum(np.abs(X-0.35)-0.35,np.abs(Y)-0.65))
    axs.contourf(X,Y,Z,levels=[-10,0],colors=['#DDEFF0'])
    axs.contour(X,Y,Z,levels=[0],colors=[NAVY],linewidths=2)
    axs.quiver([0.1,0.65,-0.75],[0.65,0.2,-0.1],[0.2,0.25,-0.2],[0.1,0.0,-0.1],color=CORAL,scale=1.8,width=0.012)
    axs.set_xlim(-1.1,1.1); axs.set_ylim(-1.1,1.1)
    axs.set_title('Implicit boundary and gradient',fontsize=10,color=NAVY,fontweight='bold')

    # 1-bit output
    axb = fig.add_axes([0.70,0.11,0.24,0.43]); axb.axis('off')
    n=36; yy,xx=np.mgrid[0:n,0:n]; cx=cy=(n-1)/2; rr=np.sqrt((xx-cx)**2+(yy-cy)**2)
    image=((rr<13)&(((xx*17+yy*29)%31)/31 < np.clip((14-rr)/8,0,1))).astype(float)
    axb.imshow(image,cmap='binary',interpolation='nearest')
    axb.set_title('Static 1-bit posterization',fontsize=10,color=NAVY,fontweight='bold')
    axb.text(0.5,-0.10,'Display may instead use temporal pulse density.',transform=axb.transAxes,ha='center',fontsize=8.5,color=GRAY)

    ax.text(0.5,0.035,'Normalization: source "Feynman vectors" -> ordinary complex-phasor/oriented supersampling. No quantum claim.',
            ha='center',color=CORAL,fontweight='bold',fontsize=9.5)
    save(fig, 'graphics_adapter')


def game_engine_stack():
    fig, ax=plt.subplots(figsize=(12,7.2)); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    title(ax,'Game-technology integration','A hybrid engine keeps UGTS-0 authoritative while conventional rendering, audio and tooling remain available')

    # entity components left
    ax.text(0.08,0.85,'ENTITY COMPONENTS',color=TEAL,fontweight='bold')
    components=[
        ('Analytic trajectory','p0, v0, a, t0'),
        ('Phase / sheet / orientation','typed small state'),
        ('Branch + tags','routing / policy'),
        ('Lineage + uncertainty','identity / confidence'),
    ]
    for i,(a,b) in enumerate(components):
        box(ax,(0.06,0.68-i*0.13),0.25,0.09,f'{a}\n{b}',fc=WHITE,ec=TEAL,fontsize=9)

    ax.text(0.39,0.85,'QUERY SYSTEMS',color=GOLD,fontweight='bold')
    queries=[
        ('Sensor support','FOV, radius, time window'),
        ('Continuous event solver','TOI / trigger / portal'),
        ('Compatibility gate','sheet, phase, policy'),
        ('Transition + event log','patch, rollback, replication'),
    ]
    for i,(a,b) in enumerate(queries):
        box(ax,(0.37,0.68-i*0.13),0.26,0.09,f'{a}\n{b}',fc=WHITE,ec=GOLD,fontsize=9)
        arrow(ax,(0.31,0.725-i*0.13),(0.37,0.725-i*0.13),color=GRAY)

    ax.text(0.72,0.85,'ENGINE ADAPTERS',color=PURPLE,fontweight='bold')
    adapters=[
        ('Render preview','mesh/SDF/raymarch as desired'),
        ('Physics bridge','rigid bodies for fallback cases'),
        ('Networking','seed + authoritative event records'),
        ('Editor / telemetry','inspect supports, roots, lineage'),
    ]
    for i,(a,b) in enumerate(adapters):
        box(ax,(0.69,0.68-i*0.13),0.25,0.09,f'{a}\n{b}',fc=WHITE,ec=PURPLE,fontsize=9)
        arrow(ax,(0.63,0.725-i*0.13),(0.69,0.725-i*0.13),color=GRAY)

    box(ax,(0.08,0.075),0.84,0.12,
        'Frame loop is a scheduler, not the ontology\nstate_at(t) may skip elapsed frames for fixed expressions.\nnext_event still pays compatibility, root-solving and branch costs.',
        fc=NAVY,ec=NAVY,text_color=WHITE,fontsize=9.8)
    ax.text(0.50,0.025,'Exit criterion: pruning + event solving must cost less than the world materialization avoided.',ha='center',color=CORAL,fontweight='bold')
    save(fig,'game_engine_stack')


def bce_hardware():
    fig, ax=plt.subplots(figsize=(12.5,7.2)); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    title(ax,'Bounded Compatibility Event hardware endpoint','A disciplined optofluidic translation: measured guard crossings, not topological magic')

    stages=[
        ('Spherical support','r, theta, phi\nfield of view'),
        ('Liquid lens / overclad','curvature, n_eff,\nphase tuning'),
        ('Mode coupler','overlap eta\nwavelength/polarization'),
        ('Waveguide / MZI','phase and\ninterference'),
        ('Detector guard','g(y,t)=0\nand chi=1'),
        ('Verified output','event + uncertainty\nlineage + calibration'),
    ]
    xs=np.linspace(0.035,0.825,6)
    colors=[TEAL,TEAL,GOLD,PURPLE,CORAL,GREEN]
    for x,(a,b),c in zip(xs,stages,colors):
        box(ax,(float(x),0.68),0.14,0.16,f'{a}\n{b}',fc=WHITE,ec=c,fontsize=8.7)
    for i in range(5): arrow(ax,(xs[i]+0.14,0.76),(xs[i+1],0.76),color=GRAY)

    ax.text(0.06,0.58,'REFERENCE CONTROL LOOP',color=NAVY,fontweight='bold')
    code='support = admit(theta, phi, r)\nlens_u = tune(target_mode)\ny = detector_read()\nchi = mode_ok and phase_ok and time_ok and policy_ok\nif support and chi and guard_crossed(y):\n    parity ^= 1\n    emit(event, confidence, lineage)\nelse: reject_or_hold()'
    box(ax,(0.05,0.20),0.43,0.34,code,fc='#F5F8F8',ec=NAVY,fontsize=9.3)

    ax.text(0.55,0.58,'REQUIRED METRICS',color=NAVY,fontweight='bold')
    metrics=[
        ('verified events / second','primary throughput at declared error'),
        ('verified events / joule','includes source, actuator, detector, control'),
        ('miss / false-event probability','certification boundary'),
        ('median / tail latency','includes settling and electronics'),
        ('loss and routing efficiency','admitted -> compatible -> verified'),
        ('drift / calibration interval','temperature, bubbles, aging'),
    ]
    for i,(a,b) in enumerate(metrics):
        box(ax,(0.54,0.47-i*0.055),0.41,0.045,f'{a}: {b}',fc=WHITE,ec=GOLD,fontsize=8.2,radius=0.012)

    ax.text(0.50,0.08,'One-bit parity is only a route/latch flag. Optical amplitude, threshold, uncertainty and lineage remain separate.',
            ha='center',color=CORAL,fontweight='bold',fontsize=9.5)
    ax.text(0.50,0.035,'Prototype is killed if calibration, loss, actuation bandwidth or energy erases the measured advantage.',
            ha='center',color=GRAY,fontsize=9.2)
    save(fig,'bce_hardware')


def evidence_filter():
    fig, ax=plt.subplots(figsize=(11.5,7)); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    title(ax,'Evidence and claim filter','Every source motif receives a disposition before entering the technical substrate')

    levels=[
        (0.05,0.82,0.62,0.10,'SOURCE MOTIFS','geometry, graphics, topology, analogies, narrative',MID,NAVY),
        (0.08,0.65,0.56,0.10,'RETAIN','sound mathematical or operational mechanism',TEAL,WHITE),
        (0.11,0.48,0.50,0.10,'TRANSLATE','keep operator; replace metaphor with typed implementation',GOLD,NAVY),
        (0.14,0.31,0.44,0.10,'DEMOTE / CORRECT','heuristic, analogy, or corrected special case',PURPLE,WHITE),
        (0.17,0.14,0.38,0.10,'REJECT','unsupported totalizing or physical claim',CORAL,WHITE),
    ]
    for x,y,w,h,a,b,fc,tc in levels:
        box(ax,(x,y),w,h,f'{a}\n{b}',fc=fc,ec=fc,text_color=tc,fontsize=9.8)
    for i in range(len(levels)-1):
        x,y,w,h,*_=levels[i]; x2,y2,w2,h2,*_=levels[i+1]
        arrow(ax,(x+w/2,y),(x2+w2/2,y2+h2),color=GRAY)

    box(ax,(0.70,0.24),0.26,0.53,
        'EXAMPLES REJECTED\n\n- universal O(1)\n- zero memory / heat / latency\n- one bit as full state\n- physical Klein self-assembly\n- geometry replaces general AI\n- topology eliminates all broad phase',
        fc='#F9ECE9',ec=CORAL,text_color=DARK,fontsize=9.1)
    ax.text(0.83,0.73,'claims ledger',ha='center',color=CORAL,fontweight='bold',fontsize=9.5)
    ax.text(0.05,0.035,'Rule: source-derived content and engineering normalization remain visibly distinct in the report, inventory and code comments.',
            color=NAVY,fontweight='bold')
    save(fig,'evidence_filter')

def prototype_flow():
    fig, ax=plt.subplots(figsize=(12.3,6.6)); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    title(ax,'Equation World Zero: minimum falsifiable prototype','Six queries and explicit exit criteria test the core without turning it into a renderer benchmark')

    flow=[('Finite grammar','bounded depth'),('State evaluator','state_at(t)'),('Compatibility','reason codes'),('Event solver','next valid root'),('Transition router','patch + lineage'),('Query outputs','event log')]
    xs=np.linspace(0.03,0.83,6)
    for x,(a,b) in zip(xs,flow):
        box(ax,(float(x),0.66),0.14,0.13,f'{a}\n{b}',fc=WHITE,ec=TEAL,fontsize=9)
    for i in range(5): arrow(ax,(xs[i]+0.14,0.725),(xs[i+1],0.725),color=TEAL)
    arrow(ax,(0.90,0.66),(0.17,0.66),color=GRAY,curve=-0.35,style='-|>')
    ax.text(0.54,0.57,'external events and schema updates feed the authoritative log',ha='center',color=GRAY,fontsize=9)

    queries=[
        '1  state at time',
        '2  next event',
        '3  events in local support',
        '4  phase/sheet coupling',
        '5  hourglass/portal routing',
        '6  identity reconstruction',
    ]
    ax.text(0.06,0.47,'REQUIRED QUERIES',color=GOLD,fontweight='bold')
    for i,q in enumerate(queries):
        box(ax,(0.05+(i%2)*0.25,0.38-(i//2)*0.10),0.22,0.065,q,fc='#FCF7E8',ec=GOLD,fontsize=8.8)

    criteria=[
        ('Horizon skipping','cost tracks expression size, not skipped frames'),
        ('Sparse event solving','compatibility removes enough candidates'),
        ('Stable lineage','splits/merges are detectable and reconstructable'),
        ('Numerical status','tangencies and degeneracies return bounded uncertainty'),
        ('Memory discipline','storage scales with parameters + novelty, not image extent'),
    ]
    ax.text(0.57,0.47,'EXIT CRITERIA',color=CORAL,fontweight='bold')
    for i,(a,b) in enumerate(criteria):
        box(ax,(0.56,0.39-i*0.072),0.39,0.054,f'{a}: {b}',fc='#F9ECE9',ec=CORAL,fontsize=8.2,radius=0.012)

    ax.text(0.50,0.045,'Failure is useful: event explosion, grammar growth, poor conditioning or weak compatibility directly falsifies the claimed advantage.',
            ha='center',color=NAVY,fontweight='bold',fontsize=9.5)
    save(fig,'prototype_flow')


if __name__ == '__main__':
    architecture_overview()
    state_event_formalism()
    numeric_fractal()
    glyph_morph()
    topology_maps()
    graphics_adapter()
    game_engine_stack()
    bce_hardware()
    evidence_filter()
    prototype_flow()
    print('generated diagrams in', OUT)
