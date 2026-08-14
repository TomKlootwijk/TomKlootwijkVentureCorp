from pathlib import Path
from io import BytesIO
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from PIL import Image, ImageOps, ImageDraw
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import rdMolDraw2D

BASE = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
DATA = BASE / '04_Data'
ORIGINAL_PDF = BASE / '01_Original_and_Translation' / 'SE301717B_original_Swedish.pdf'
US_PDF = BASE / '02_Patent_Family' / 'US3364178A.pdf'
OUT.mkdir(parents=True, exist_ok=True)
NAVY='#15384D'; TEAL='#207887'; GOLD='#D39B2A'; RED='#A84B44'; GREEN='#4D7C5B'; SLATE='#61727C'; PALE='#EDF4F6'; LIGHT='#F7F5EF'; DARK='#1E252A'
plt.rcParams.update({'font.family':'DejaVu Sans','axes.titlesize':14,'axes.labelsize':11,'xtick.labelsize':9,'ytick.labelsize':9})

def savefig(path, fig, dpi=220):
    fig.savefig(path, dpi=dpi, bbox_inches='tight', facecolor='white')
    plt.close(fig)

# 1. Reaction concept with chemical structures
bps_smiles='Oc1ccc(cc1)S(=O)(=O)c2ccc(O)cc2'
dgebps_smiles='O=S(=O)(c1ccc(OCC2CO2)cc1)c3ccc(OCC4CO4)cc3'

def mol_png(smiles, path, size=(850,330)):
    mol=Chem.MolFromSmiles(smiles)
    AllChem=None
    drawer=rdMolDraw2D.MolDraw2DCairo(size[0],size[1])
    opts=drawer.drawOptions(); opts.bondLineWidth=2.2; opts.baseFontSize=0.8
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    path.write_bytes(drawer.GetDrawingText())

mol_png(bps_smiles, OUT/'_bps.png')
mol_png(dgebps_smiles, OUT/'_dgebps.png', size=(1000,330))
img1=Image.open(OUT/'_bps.png').convert('RGBA')
img2=Image.open(OUT/'_dgebps.png').convert('RGBA')
fig=plt.figure(figsize=(11.5,6.2))
ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
ax.add_patch(FancyBboxPatch((0.02,0.54),0.39,0.36,boxstyle='round,pad=0.012,rounding_size=0.02',fc=PALE,ec=TEAL,lw=1.6))
ax.add_patch(FancyBboxPatch((0.59,0.54),0.39,0.36,boxstyle='round,pad=0.012,rounding_size=0.02',fc=PALE,ec=TEAL,lw=1.6))
ax.imshow(img1, extent=(0.055,0.375,0.61,0.82), aspect='auto', zorder=3)
ax.imshow(img2, extent=(0.62,0.95,0.61,0.82), aspect='auto', zorder=3)
ax.text(0.215,0.865,"Bisphenol S (BPS)\ndihydric phenol",ha='center',va='center',fontsize=12,fontweight='bold',color=NAVY)
ax.text(0.785,0.865,"Diglycidyl ether of BPS\n(DGE-BPS; diepoxide)",ha='center',va='center',fontsize=12,fontweight='bold',color=NAVY)
ax.text(0.50,0.72,'+',fontsize=28,ha='center',va='center',color=GOLD,fontweight='bold')
ax.add_patch(FancyArrowPatch((0.5,0.53),(0.5,0.42),arrowstyle='-|>',mutation_scale=22,lw=2,color=GOLD))
ax.text(0.5,0.49,'anhydrous base catalyst • polar nonreactive solvent • high conversion',ha='center',va='center',fontsize=10,color=DARK)
ax.add_patch(FancyBboxPatch((0.08,0.08),0.84,0.28,boxstyle='round,pad=0.016,rounding_size=0.025',fc=LIGHT,ec=NAVY,lw=1.8))
ax.text(0.5,0.29,'Sulfone-containing linear poly(hydroxy ether)',ha='center',va='center',fontsize=14,fontweight='bold',color=NAVY)
ax.text(0.5,0.205,r'$[-\mathrm{Ar{-}O{-}CH_2{-}CH(OH){-}CH_2{-}O{-}Ar^\prime}-]_n$',ha='center',va='center',fontsize=19,color=DARK)
ax.text(0.5,0.125,"Ar and/or Ar' contains Ar-SO2-Ar. Each epoxide opening creates an ether bond and a pendant secondary OH.\nWith two difunctional feeds and near-equivalent functionality, the intended product is linear and thermoplastic.",ha='center',va='center',fontsize=10.5,color=SLATE)
ax.text(0.02,0.97,'The chemistry actually claimed',fontsize=17,fontweight='bold',color=NAVY,va='top')
savefig(OUT/'figure_01_reaction_concept.png',fig)

# 2. Carothers Xn vs conversion
fig,ax=plt.subplots(figsize=(8.4,5.5))
ps=np.linspace(0.90,0.9995,500)
for r,c,label in [(1.0,NAVY,'r = 1.000'),(0.99,TEAL,'r = 0.990'),(0.9804,GOLD,'r = 0.9804 (1.02:1)'),(0.97,RED,'r = 0.970')]:
    xn=(1+r)/(1+r-2*r*ps)
    ax.plot(ps*100,xn,lw=2.4,color=c,label=label)
ax.set_yscale('log'); ax.set_ylim(5,2500); ax.set_xlim(90,100)
ax.set_xlabel('Conversion of limiting functional groups, p (%)')
ax.set_ylabel('Ideal number-average degree of polymerization, Xn (log scale)')
ax.set_title('Why the final fractions of conversion and the 1:1 balance dominate chain length',loc='left',fontweight='bold',color=NAVY)
ax.grid(True,which='both',alpha=.22); ax.legend(frameon=False,loc='upper left')
ax.axvline(99,color=SLATE,lw=1,ls='--',alpha=.6); ax.text(99.03,7.2,'99%',fontsize=8,color=SLATE)
ax.text(90.2,7.1,'Ideal AA + BB model; cyclization, impurities and branching omitted.',fontsize=8.5,color=SLATE)
savefig(OUT/'figure_02_carothers_conversion.png',fig)

# 3. Stoichiometric ceiling
ratios=np.array([1.04,1.03,1.02,1.01,0.99,0.98,0.97,0.96])
rs=np.minimum(ratios,1/ratios); xmax=(1+rs)/(1-rs)
fig,ax=plt.subplots(figsize=(8.4,4.9))
colors=[RED,RED,GOLD,TEAL,TEAL,GOLD,RED,RED]
bars=ax.bar([f'{x:.2f}' for x in ratios],xmax,color=colors,alpha=.9)
for b,v in zip(bars,xmax): ax.text(b.get_x()+b.get_width()/2,v+4,f'{v:.0f}',ha='center',va='bottom',fontsize=9)
ax.set_ylim(0,230); ax.set_ylabel('Ideal Xn ceiling at complete limiting-group conversion')
ax.set_xlabel('Dihydroxy : diepoxy molecular ratio')
ax.set_title('A 1-4% feed imbalance is a molecular-weight dial, not vague wording',loc='left',fontweight='bold',color=NAVY)
ax.grid(axis='y',alpha=.2)
ax.text(0.0,-0.22,'Patent preferred range: about 1.02 to 0.99.  The exact 1.00 point is omitted because the ideal ceiling diverges.',transform=ax.transAxes,fontsize=8.5,color=SLATE)
savefig(OUT/'figure_03_stoichiometric_ceiling.png',fig)

# 4. U.S. Table 1 sulfone effect, 3 metrics
us=pd.read_csv(DATA / 'us3364178_table1.csv').iloc[:3]
fig,axes=plt.subplots(1,3,figsize=(11,4.2))
metrics=[('yield_stress_MPa','Yield stress (MPa)'),('tensile_impact_historical','Tensile impact\n(historical units)'),('vicat_C','Vicat softening (C)')]
for ax,(col,label) in zip(axes,metrics):
    vals=us[col].astype(float).values
    ax.plot([0,1,2],vals,marker='o',lw=2.6,ms=7,color=TEAL)
    for x,v in zip([0,1,2],vals): ax.text(x,v+(max(vals)-min(vals))*0.06,f'{v:g}',ha='center',fontsize=9,fontweight='bold',color=NAVY)
    ax.set_xticks([0,1,2]); ax.set_xticklabels(['0\nBPA/BPA','1\nBPS/BPA','2\nBPS/BPS'])
    ax.set_xlabel('Sulfone-bearing feed components')
    ax.set_ylabel(label); ax.grid(axis='y',alpha=.2)
fig.suptitle('U.S. counterpart: the first three comparison polymers show a strong sulfone-content trend',x=.04,ha='left',fontsize=15,fontweight='bold',color=NAVY)
fig.text(.04,.01,'Intrinsic viscosity also rises (0.57 -> 0.67 -> 0.70), so a modern matched-molecular-weight series is still needed.',fontsize=8.5,color=SLATE)
fig.tight_layout(rect=[0,0.05,1,.91])
savefig(OUT/'figure_04_us_table1_sulfone_effect.png',fig)

# 5. IV vs impact
points=[('Ex.2',0.35,110),('Ex.1',0.43,650),('Ex.3A',0.46,650),('Ex.3B',0.50,620),('Ex.4 pressed',1.29,690)]
fig,ax=plt.subplots(figsize=(8.2,4.8))
for name,x,y in points:
    ax.scatter(x,y,s=75,color=(RED if x<=.35 else TEAL),zorder=3)
    ax.annotate(name,(x,y),xytext=(5,7),textcoords='offset points',fontsize=9)
ax.axvline(.35,color=GOLD,ls='--',lw=1.6); ax.text(.36,155,'patent-observed\nimpact threshold',color=GOLD,fontsize=9)
ax.set_xlabel('Intrinsic viscosity in DMF (historical value)'); ax.set_ylabel('Impact tensile strength (historical units)')
ax.set_title('Swedish examples: impact performance changes abruptly above IV about 0.35',loc='left',fontweight='bold',color=NAVY)
ax.set_ylim(0,780); ax.grid(alpha=.2)
ax.text(.01,-.20,'Sparse, non-replicated historical data. Ex.4 is plotted using post-pressing IV 1.29.',transform=ax.transAxes,fontsize=8.5,color=SLATE)
savefig(OUT/'figure_05_intrinsic_viscosity_impact.png',fig)

# 6. Application confidence matrix
apps=pd.read_csv(DATA / 'application_assessment.csv')
score={'High':4,'Medium-high':3.5,'Medium':3,'Medium-low':2,'Low':1,'Unsupported':0}
apps['score']=apps['confidence'].map(score)
apps=apps.iloc[::-1]
fig,ax=plt.subplots(figsize=(9,6.8))
y=np.arange(len(apps)); cols=[RED if s<=1 else GOLD if s<3 else TEAL for s in apps['score']]
ax.barh(y,apps['score'],color=cols,alpha=.9)
ax.set_yticks(y); ax.set_yticklabels(apps['application'],fontsize=9)
ax.set_xlim(0,4.2); ax.set_xticks([0,1,2,3,4]); ax.set_xticklabels(['unsupported','low','medium-low','medium','high'])
ax.grid(axis='x',alpha=.2); ax.set_xlabel('Evidence-weighted confidence')
ax.set_title('Application map: strongest value is in reactive engineering films, coatings and composites',loc='left',fontweight='bold',color=NAVY)
for yi,s,lab in zip(y,apps['score'],apps['confidence']): ax.text(s+.06,yi,lab,va='center',fontsize=8.5,color=DARK)
fig.tight_layout()
savefig(OUT/'figure_06_application_confidence.png',fig)

# 7. Timeline
fig,ax=plt.subplots(figsize=(11,4.3)); ax.set_xlim(1956,2028); ax.set_ylim(-1.1,1.1); ax.axis('off')
ax.hlines(0,1959,2025,color=NAVY,lw=2)
events=[(1959,'NL priority\nKlootwijk et al.',1),(1963,'GB 915,767\npublished',-1),(1968,'US 3,364,178\nand SE 301,717',1),(1978,'Fully aromatic\npolyarylene polyethers',-1),(1987,'Shell linear units\nlightly crosslinked',1),(1991,'PES/phenoxy\nfiltration membranes',-1),(2002,'BPS high-MW epoxy\nfor PCB film',1),(2004,'PHES paper:\nBPS + epichlorohydrin',-1),(2023,'BPS female repro\nlisting (California)',1),(2025,'Male + developmental\nendpoints added',-1)]
for year,label,side in events:
    ax.plot(year,0,'o',ms=7,color=GOLD)
    ax.vlines(year,0,0.55*side,color=SLATE,lw=1.2)
    ax.text(year,0.62*side,label,ha='center',va=('bottom' if side>0 else 'top'),fontsize=8.3,color=DARK)
ax.text(1956,1.02,'A technological lineage - not proof of one continuous product, but repeated validation of the design logic',fontsize=14,fontweight='bold',color=NAVY,ha='left')
ax.text(1959,-.02,'1959',ha='center',va='top',fontsize=8,color=SLATE)
ax.text(2025,.02,'2025',ha='center',va='bottom',fontsize=8,color=SLATE)
savefig(OUT/'figure_07_timeline.png',fig)

# 8. Evidence ladder / hypothesis filter
fig,ax=plt.subplots(figsize=(8.5,5.2)); ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
levels=[(0.8,0.8,8.4,2.1,TEAL,'DIRECTLY SUPPORTED','Linear high-MW poly(hydroxy ether); sulfone raises thermal/impact metrics;\nthermoplastic shaping; stoichiometry/solubility/dryness control.'),(1.45,3.25,7.1,2.1,GOLD,'SUPPORTED EXTRAPOLATION','Reactive films, coatings, adhesives, PCB dielectric, epoxy toughener,\nthermoplastic-to-thermoset conversion, selected membrane blends.'),(2.1,5.7,5.8,2.1,RED,'RESEARCH HYPOTHESIS','Biosensor surfaces, affinity membranes, additive manufacturing,\npost-sulfonated ion conductors - each requires new evidence.')]
for x,y,w,h,c,title,text in levels:
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.02,rounding_size=.12',fc=c,ec='none',alpha=.92))
    ax.text(x+w/2,y+h*.68,title,ha='center',va='center',fontsize=12,fontweight='bold',color='white')
    ax.text(x+w/2,y+h*.31,text,ha='center',va='center',fontsize=9,color='white')
ax.text(5,9.35,'How this review separates evidence from imagination',ha='center',fontsize=15,fontweight='bold',color=NAVY)
ax.text(5,8.75,'The "hidden revolution" survives only where chemistry and later records support it.',ha='center',fontsize=10.5,color=SLATE)
ax.text(5,.25,'Rejected: SO2 release, secret biological signaling, intrinsic ion exchange, or implant claims.',ha='center',fontsize=10,color=RED,fontweight='bold')
savefig(OUT/'figure_08_evidence_ladder.png',fig)

# 9. Process window diagram
fig,ax=plt.subplots(figsize=(9,5.6)); ax.set_xlim(0,12); ax.set_ylim(0,8); ax.axis('off')
inputs=[(1.7,6.4,'Near-equivalent\nfunctional groups'),(4.5,6.4,'Very high\nconversion'),(7.3,6.4,'Growing chain\nkept dissolved'),(10.1,6.4,'Dry, pure,\nnonreactive system')]
for x,y,t in inputs:
    ax.add_patch(FancyBboxPatch((x-1.25,y-.65),2.5,1.3,boxstyle='round,pad=.02,rounding_size=.15',fc=PALE,ec=TEAL,lw=1.5))
    ax.text(x,y,t,ha='center',va='center',fontsize=10,fontweight='bold',color=NAVY)
    ax.add_patch(FancyArrowPatch((x,y-.7),(6,4.55),arrowstyle='-|>',mutation_scale=14,lw=1.2,color=SLATE,alpha=.8))
ax.add_patch(FancyBboxPatch((4.25,3.2),3.5,1.35,boxstyle='round,pad=.03,rounding_size=.18',fc=GOLD,ec='none'))
ax.text(6,3.88,'High molecular weight\nlinear thermoplastic',ha='center',va='center',fontsize=13,fontweight='bold',color='white')
outcomes=[(2.2,1.2,'Toughness'),(4.7,1.2,'Thermal\nperformance'),(7.3,1.2,'Melt/solution\nprocessing'),(9.8,1.2,'Pendant-OH\nreactivity')]
for x,y,t in outcomes:
    ax.add_patch(FancyArrowPatch((6,3.15),(x,y+0.65),arrowstyle='-|>',mutation_scale=14,lw=1.2,color=SLATE))
    ax.add_patch(FancyBboxPatch((x-1.15,y-.55),2.3,1.1,boxstyle='round,pad=.02,rounding_size=.15',fc=NAVY,ec='none'))
    ax.text(x,y,t,ha='center',va='center',fontsize=10,color='white',fontweight='bold')
ax.text(.35,7.7,'The true inventive unit is a coupled process window',fontsize=15,fontweight='bold',color=NAVY)
ax.text(.35,7.25,'The patent does not rely on one magic group; it integrates chemistry, phase behavior and metrology.',fontsize=10.3,color=SLATE)
savefig(OUT/'figure_09_process_window.png',fig)

# 10. Patent crops for documentary appendix.
# PyMuPDF is optional; when unavailable, the bundled documentary PNGs are retained.
def render_pdf_page(pdf_path, page_number, zoom=2.5):
    import fitz
    doc = fitz.open(pdf_path)
    try:
        page = doc.load_page(page_number)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        return Image.open(BytesIO(pix.tobytes('png'))).convert('RGB')
    finally:
        doc.close()

try:
    orig = render_pdf_page(ORIGINAL_PDF, 0)
    w,h=orig.size
    crop=orig.crop((int(.08*w),int(.03*h),int(.93*w),int(.48*h)))
    crop=ImageOps.expand(crop,border=3,fill=NAVY)
    crop.save(OUT/'document_01_swedish_front_matter.png',quality=95)

    uspage = render_pdf_page(US_PDF, 1)
    w,h=uspage.size
    crop=uspage.crop((int(.07*w),int(.05*h),int(.54*w),int(.42*h)))
    crop=ImageOps.expand(crop,border=3,fill=NAVY)
    crop.save(OUT/'document_02_us_table1_crop.png',quality=95)
except Exception as exc:
    print(f'warning: documentary patent crops were not regenerated: {exc}')

# clean temporary molecular images
for p in [OUT/'_bps.png',OUT/'_dgebps.png']:
    try: p.unlink()
    except: pass
print('generated',len(list(OUT.glob('*.png'))),'figures')
