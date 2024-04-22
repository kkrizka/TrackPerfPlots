# Muon Collider Detector Track Reconstruction Studies
Scripts for studying the tranck reconstruction performance of the Muon Collider Detector.

All inputs and resulting plots are archived on CERN's EOS storage:
```
/eos/user/k/kkrizka/public/MuonCollider/TrackPerfPlots
```

## Installation
Local installation of PyROOT is required. All other packages are installable via pip.

```shell
python -m venv .venv --system-site-packages
source .venv/bin/activate
pip install .
```

Then in any subsequent session, run the following.
```shell
source .venv/bin/activate
```

## Making Plots

## Global Configuration
Global aspects of the plotting code can be configured using a configuration file
called `.config.yaml`. This is loaded automatically and overrides input values
inside the `TrackPerf.config` module.

Configuration keys:
- `datapath`: path to geantino scan ROOT files
- `format`: image format to use for output plots (ie: `png`)

## Run Configuration
The steering of a plotting script is done through run configurations. Examples are
provided inside the `runconfig` directory.

A script takes multiple run configs as arguments. They are first merged before
used by the script.

## Plotting Efficiencies
The plot efficiency run configs define two fields:

- `inputs`: list of input files containing the output of TrackPerf
- `variables`: list of variables to plot

Each input is a dictionary with the following keys:

- `path`: input ROOT file path relative to `config.datapath`
- `title`: title to use in the legend
- `linecolor`: color to use for the file

Each variable is a dictionary with the following keys:

- `name`: name of the histogram

For example, to compare the different particle guns:

```shell
plot_efficiencies.py 
```