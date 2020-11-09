#!/usr/bin/env python
#
# InspiredBy https://github.com/vhbb/vhbb-nano/blob/master/postproc.py
#
import os,sys
import ROOT
import argparse
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
from JetTaggingAnalysis.NanoAODAnalyzer.postproc.JetTaggingOneLeptonNanoSkimmer import JetTaggingOneLeptonNanoSkimmer_2016_mc_sig
from JetTaggingAnalysis.NanoAODAnalyzer.postproc.JetTaggingOneLeptonNanoSkimmer import JetTaggingOneLeptonNanoSkimmer_2016_mc_bkgd
from JetTaggingAnalysis.NanoAODAnalyzer.postproc.JetTaggingOneLeptonNanoSkimmer import JetTaggingOneLeptonNanoSkimmer_2016_data

print "args are: ",sys.argv

isMC = True
isSig = True
era = "2016"

parser = argparse.ArgumentParser("")
parser.add_argument('-jobNum', '--jobNum', type=int, default=1, help="") #NOTE: This will be given by  condor on the grid. not by us
parser.add_argument('-isMC', '--isMC',  type=int, default=1, help="")
parser.add_argument('-isSig','--isSig', type=int, default=1, help="")
parser.add_argument('-era', '--era', type=str, default="2017", help="")

args = parser.parse_args()
print "args = ",args

isMC    = args.isMC
isSig   = args.isSig
era     = args.era

print "isMC = ",isMC," isSig = ",isSig, "era = ",era

CMSXROOTD="root://xrootd-cms.infn.it/"
files = [CMSXROOTD+"/store/mc/RunIISummer16NanoAODv5/WprimeToWZToWhadZlep_width0p1_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8/NANOAODSIM/PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/120000/AC02C99D-0436-024D-A8F4-90EBC1CB5C39.root"]

varTxtFileIn="keep_and_drop_branches.txt"
varTxtFileOut="keep_and_drop_branches.txt"

selection=""
modules = []

if era == "2016":
  if isMC: 
    if isSig: 
      modules=[JetTaggingOneLeptonNanoSkimmer_2016_mc_sig()]
    else:     
      modules=[JetTaggingOneLeptonNanoSkimmer_2016_mc_bkgd()]
  else:              
    modules=[JetTaggingOneLeptonNanoSkimmer_2016_data()]


# 
#this takes care of converting the input files from CRAB
#
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis

if isMC:
  p=PostProcessor(
    ".", 
    inputFiles(),
    cut=selection,
    branchsel=varTxtFileIn,
    outputbranchsel=varTxtFileOut,
    modules=modules,
    provenance=True,
    fwkJobReport=True,
    histFileName="histo.root",
    histDirName="cutflow"
  )
else:
  p=PostProcessor(
    ".", 
    inputFiles(),
    cut=selection,
    branchsel=varTxtFileIn,
    outputbranchsel=varTxtFileOut,
    modules=modules,
    provenance=True,
    fwkJobReport=True,
    histFileName="histo.root",
    histDirName="cutflow",
    jsonInput=runsAndLumis(),
  )

p.run()

print "DONE"
os.system("ls -lR")

