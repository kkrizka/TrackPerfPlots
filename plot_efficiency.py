"""
Plot efficiency f different samples
"""
# %%
import ROOT

from TrackPerf import config

from kkconfig import runconfig

from kkroot import style

import mccstyle

import sys
from math import *

# %% Prepare configuration
if 'ipykernel' in sys.modules: # running in a notebook
    # %load_ext autoreload
    # %autoreload 2
    runcfgpaths=['runconfigs/data_muonGun.yaml']
else:
    if len(sys.argv)<2:
        print('usage: {} runconfig.yaml [runconfig.yaml]'.format(sys.argv[0]))
        sys.exit(1)
    runcfgpaths=sys.argv[1:]

runcfg = runconfig.load(runcfgpaths)

# %%
effs=[] # PyROOT memory management...
for v in runcfg['variables']:
    c=ROOT.TCanvas()

    mg_eff=ROOT.TMultiGraph()

    legend=v.get('legend',{})
    lx=legend.get('x',0.4)
    ly=legend.get('y',0.3)

    l = ROOT.TLegend(lx,ly+len(runcfg['inputs'])*0.05,lx+0.4,ly)
    l.SetBorderSize(0)
    l.SetFillStyle(0)

    for i in runcfg['inputs']:
        # Open file with data
        path=config.datapath+'/'+i['path']
        fh=ROOT.TFile.Open(path)

        # Create efficiency object
        ROOT.gROOT.cd()
        dname='MyTrackPerf/all/'+v['name']
        den=fh.Get(dname)
        if den==None:
            print(f"{dname} missing in {i['path']}")
            continue

        nname='MyTrackPerf/real/'+v['name']
        num=fh.Get(nname)
        if num==None:
            print(f"{nname} missing in {i['path']}")
            continue

        num.Rebin(2)
        den.Rebin(2)

        eff=ROOT.TEfficiency(num, den)
        effs.append(eff)

        # Apply styles
        style.style(eff, **i)
        eff.SetLineWidth(2)

        # Add to legend
        l.AddEntry(eff,i['title'],'l')

        # Add to multigraph
        mg_eff.Add(eff.CreateGraph())

    # Main plot
    mg_eff.Draw('AP')
    l.Draw()

    mg_eff.SetTitle(runcfg.get('title',''))

    mg_eff.SetMinimum(0)
    mg_eff.SetMaximum(1.05)
    mg_eff.GetYaxis().SetTitle('Track reconstruction efficiency')
    mg_eff.GetXaxis().SetTitle(den.GetXaxis().GetTitle())
    mg_eff.GetXaxis().SetLimits(den.GetXaxis().GetXmin(),den.GetXaxis().GetXmax())

    mccstyle.logo(xpos=0.4,ypos=0.46)

    c.Draw()
    c.SaveAs('efficiency_'+runcfg['name']+'_'+v['name']+'.'+config.format)
