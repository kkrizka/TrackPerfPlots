"""
Plot efficiency f different samples
"""
# %%
import ROOT

from TrackPerf import config

from kkconfig import runconfig

from kkroot import style

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

    l = ROOT.TLegend(0.6,0.2+len(runcfg['inputs'])*0.05,0.9,0.2)
    l.SetBorderSize(0)

    for i in runcfg['inputs']:
        # Open file with data
        path=config.datapath+'/'+i['path']
        fh=ROOT.TFile.Open(path)

        # Create efficiency object
        ROOT.gROOT.cd()
        den=fh.Get('MyTrackPerf/all/'+v['name'])
        num=fh.Get('MyTrackPerf/real/'+v['name'])
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

    mg_eff.SetMinimum(0)
    mg_eff.SetMaximum(1)
    mg_eff.GetYaxis().SetTitle('Efficiency')

    c.Draw()
    c.SaveAs(v['name']+'.'+config.format)
