import os,sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
from JetTaggingAnalysis.NanoAODAnalyzer.postproc.JetTaggingOneLeptonNanoSkimmer import JetTaggingOneLeptonNanoSkimmer_2016_mc_sig
from JetTaggingAnalysis.NanoAODAnalyzer.postproc.JetTaggingOneLeptonNanoSkimmer import JetTaggingOneLeptonNanoSkimmer_2016_mc_bkgd
from JetTaggingAnalysis.NanoAODAnalyzer.postproc.JetTaggingOneLeptonNanoSkimmer import JetTaggingOneLeptonNanoSkimmer_2016_data

CMSXROOTD="root://xrootd-cms.infn.it/"


inDir="/afs/cern.ch/user/n/nbinnorj/work/AnaJetTagging/CMSSW_10_2_15/src/"
infile = [inDir+"WprimeToWZToWhadZlep_width0p1_M-1200.root"]
era="2016"
isMC=True
isSig=True

#
# inDir="/afs/cern.ch/user/n/nbinnorj/work/AnaJetTagging/CMSSW_10_2_15/src/"
# infile = [inDir+"Run2016H_SingleMuon.root"]
# era="2016"
# isMC=False
# isSig=False
#

if len(sys.argv)>2: 
  outputDir = sys.argv[2]
else:
  if isMC: 
    outputDir = "outputMC" 
  else:
    outputDir = "outputData" 
  
varTxtFileIn="/afs/cern.ch/user/n/nbinnorj/work/AnaJetTagging/CMSSW_10_2_15/src/"
varTxtFileIn+="JetTaggingAnalysis/NanoAODAnalyzer/scripts/keep_and_drop_branches.txt"

varTxtFileOut="/afs/cern.ch/user/n/nbinnorj/work/AnaJetTagging/CMSSW_10_2_15/src/"
varTxtFileOut+="JetTaggingAnalysis/NanoAODAnalyzer/scripts/keep_and_drop_branches.txt"

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


p=PostProcessor(
  outputDir, 
  infile,
  cut=selection,
  branchsel=varTxtFileIn,
  outputbranchsel=varTxtFileOut,
  modules=modules,
  provenance=False,
  fwkJobReport=False,
  histFileName="histo.root",
  histDirName="cutflow"
)
p.run()
