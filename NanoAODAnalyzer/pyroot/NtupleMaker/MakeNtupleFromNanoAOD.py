import sys
import os
import glob
import ROOT

from collections import OrderedDict 
from array       import array

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import InputTree
from PhysicsTools.NanoAODTools.postprocessing.framework.branchselection import BranchSelection

ROOT.gROOT.SetBatch()

#
# CHECK: Specify your path
#
XROOTDIR="root://eosuser.cern.ch/"
OUTPUTDIR="/eos/user/s/ssyedoma/AnaJetTagging/Ntuples_ULv2/"

def getUserOptions(argv):
  from optparse import OptionParser
  parser = OptionParser()

  def add_option(option, **kwargs):
    parser.add_option('--' + option, dest=option, **kwargs)

  add_option('input',        default='',        help='Name of file with list of input files')
  add_option('outputPrefix', default='Ntuple',  help='Prefix of root output file')
  add_option('maxevents',    default=-1,        help='Number of events to run. -1 is all events')

  (options, args) = parser.parse_args(argv)
  argv = []

  print '===== Command line options ====='
  print options
  print '================================'
  return options

##########################################################
#
#
# Functions for inputtree
#
#
##########################################################
def getInputFiles(inputTextFile):
  files = []
  with open(inputTextFile, 'r') as fpInput:
    for lfn in fpInput:
      lfn = lfn.strip()
      if lfn.startswith('#'):
        print('skipping file %s' %(lfn))
        continue
      pfn = 'root://xrootd-cms.infn.it/' + lfn
      # pfn = 'root://cms-xrd-global.cern.ch/' + lfn
      # print 'Adding ' + pfn
      files.append(pfn)
  return files

##########################################################
#
#
# Functions for inputtree
#
#
##########################################################
def bookIntBranch(tree, branchName):
  tmp = array('i', [0])
  tree.Branch(branchName, tmp, '%s/I' %(branchName))
  return tmp

def bookIntArrayBranch(tree, branchName, sizeBranchName, arraySize):
  tmp = array('i', arraySize*[0])
  tree.Branch(branchName, tmp, '%s[%s]/I' %(branchName,sizeBranchName))
  return tmp

def bookFloatBranch(tree, branchName):
  tmp = array('f', [0.])
  tree.Branch(branchName, tmp, '%s/F' %(branchName))
  return tmp

def bookFloatArrayBranch(tree, branchName, sizeBranchName, arraySize):
  tmp = array('f', arraySize*[0.])
  tree.Branch(branchName, tmp, '%s[%s]/F' %(branchName,sizeBranchName))
  return tmp

##########################################################
#
#
# HarvestNanoAOD
#
#
##########################################################
def HarvestNanoAOD(inFileList, outFilePath, sample):
  # 
  # Create the output file
  # 
  print "Create Output File: %s" %(outFilePath)
  f = ROOT.TFile(outFilePath, "RECREATE")
  f.cd()
  #
  # Initialize the tree jet
  #
  treeName = "TreeFatJet"
  
  isMC_QCD = "QCD" in sample

  print "Create Output Tree: %s" %(treeName) 
  TreeFatJet = ROOT.TTree(treeName, treeName)
  
  #
  # FatJet branch
  #
  nFatJetSizeMax = 25
  nFatJetString  = 'nFatJet'
  nFatJet                 = bookIntBranch(TreeFatJet, nFatJetString)
  FatJetPt                = bookFloatArrayBranch(TreeFatJet, 'FatJet_pt' ,  nFatJetString, nFatJetSizeMax)
  FatJetEta               = bookFloatArrayBranch(TreeFatJet, 'FatJet_eta', nFatJetString, nFatJetSizeMax)
  FatJetPhi               = bookFloatArrayBranch(TreeFatJet, 'FatJet_phi', nFatJetString, nFatJetSizeMax)
  FatJetM                 = bookFloatArrayBranch(TreeFatJet, 'FatJet_mass'  , nFatJetString, nFatJetSizeMax)
  FatJetTau21             = bookFloatArrayBranch(TreeFatJet, 'FatJet_tau21',  nFatJetString, nFatJetSizeMax)
  FatJetTau31             = bookFloatArrayBranch(TreeFatJet, 'FatJet_tau31',  nFatJetString, nFatJetSizeMax)
  FatJetTau32             = bookFloatArrayBranch(TreeFatJet, 'FatJet_tau32',  nFatJetString, nFatJetSizeMax)  
  FatJetDeepTagTvsQCD     = bookFloatArrayBranch(TreeFatJet, 'FatJet_deepTag_TvsQCD',  nFatJetString, nFatJetSizeMax)
  FatJetDeepTagWvsQCD     = bookFloatArrayBranch(TreeFatJet, 'FatJet_deepTag_WvsQCD',  nFatJetString, nFatJetSizeMax)
  FatJetDeepTagZvsQCD     = bookFloatArrayBranch(TreeFatJet, 'FatJet_deepTag_ZvsQCD',  nFatJetString, nFatJetSizeMax)
  FatJetDeepTagQCD        = bookFloatArrayBranch(TreeFatJet, 'FatJet_deepTag_QCD',  nFatJetString, nFatJetSizeMax)  
  FatJetDeepTagQCDOthers  = bookFloatArrayBranch(TreeFatJet, 'FatJet_deepTag_QCDothers',  nFatJetString, nFatJetSizeMax)
  FatJetDeepTagMDTvsQCD   = bookFloatArrayBranch(TreeFatJet, 'FatJet_deepTagMD_TvsQCD',  nFatJetString, nFatJetSizeMax)
  FatJetDeepTagMDWvsQCD   = bookFloatArrayBranch(TreeFatJet, 'FatJet_deepTagMD_WvsQCD',  nFatJetString, nFatJetSizeMax)
  FatJetDeepTagMDZvsQCD   = bookFloatArrayBranch(TreeFatJet, 'FatJet_deepTagMD_ZvsQCD',  nFatJetString, nFatJetSizeMax)
  FatJetMSoftDrop         = bookFloatArrayBranch(TreeFatJet, 'FatJet_msoftdrop',   nFatJetString, nFatJetSizeMax)
  FatJetRawFactor         = bookFloatArrayBranch(TreeFatJet, 'FatJet_rawFactor',   nFatJetString, nFatJetSizeMax)
  FatJetJetId             = bookIntArrayBranch(TreeFatJet,   'FatJet_jetId', nFatJetString, nFatJetSizeMax)
  FatJetSubJetIdx1        = bookIntArrayBranch(TreeFatJet, 'FatJet_subJetIdx1',  nFatJetString, nFatJetSizeMax)
  FatJetSubJetIdx2        = bookIntArrayBranch(TreeFatJet, 'FatJet_subJetIdx2',  nFatJetString, nFatJetSizeMax)
  FatJetGenJetAK8Idx      = bookIntArrayBranch(TreeFatJet, 'FatJet_genJetAK8Idx',nFatJetString, nFatJetSizeMax)

  # 
  # GenPart branch
  #  
  if isMC_QCD == False:
    nGenPartSizeMax = 1000
    nGenPartString = 'nGenPart'
    nGenPart                = bookIntBranch(TreeFatJet, nGenPartString)
    GenPartPt               = bookFloatArrayBranch(TreeFatJet, 'GenPart_pt', nGenPartString, nGenPartSizeMax)
    GenPartEta              = bookFloatArrayBranch(TreeFatJet, 'GenPart_eta', nGenPartString, nGenPartSizeMax)
    GenPartPhi              = bookFloatArrayBranch(TreeFatJet, 'GenPart_phi', nGenPartString, nGenPartSizeMax)
    GenPartM                = bookFloatArrayBranch(TreeFatJet, 'GenPart_mass', nGenPartString, nGenPartSizeMax)
    GenPartPdgId            = bookIntArrayBranch(TreeFatJet,   'GenPart_pdgId', nGenPartString, nGenPartSizeMax)
    GenPartStatus           = bookIntArrayBranch(TreeFatJet,   'GenPart_status', nGenPartString, nGenPartSizeMax)
    GenPartStatusFlags      = bookIntArrayBranch(TreeFatJet,   'GenPart_statusFlags', nGenPartString, nGenPartSizeMax)
    GenPartGenPartIdxMother = bookIntArrayBranch(TreeFatJet,   'GenPart_genPartIdxMother', nGenPartString, nGenPartSizeMax)
  # 
  # GenJetAK8 branch
  #     
  nGenJetAK8SizeMax = 25
  nGenJetAK8String = 'nGenJetAK8'
  nGenJetAK8                = bookIntBranch(TreeFatJet, nGenJetAK8String)
  GenJetAK8Pt               = bookFloatArrayBranch(TreeFatJet, 'GenJetAK8_pt', nGenJetAK8String, nGenJetAK8SizeMax)
  GenJetAK8Eta              = bookFloatArrayBranch(TreeFatJet, 'GenJetAK8_eta', nGenJetAK8String, nGenJetAK8SizeMax)
  GenJetAK8Phi              = bookFloatArrayBranch(TreeFatJet, 'GenJetAK8_phi', nGenJetAK8String, nGenJetAK8SizeMax)
  GenJetAK8M                = bookFloatArrayBranch(TreeFatJet, 'GenJetAK8_mass', nGenJetAK8String, nGenJetAK8SizeMax)
  GenJetAK8HadronFlavour    = bookIntArrayBranch(TreeFatJet,   'GenJetAK8_hadronFlavour', nGenJetAK8String, nGenJetAK8SizeMax)
  GenJetAK8PartonFlavour    = bookIntArrayBranch(TreeFatJet,   'GenJetAK8_partonFlavour', nGenJetAK8String, nGenJetAK8SizeMax)
  # 
  # Subjet branch
  #     
  nSubJetSizeMax = 50
  nSubJetString = 'nSubJet'
  nSubJet         = bookIntBranch(TreeFatJet, nSubJetString)
  SubJetPt        = bookFloatArrayBranch(TreeFatJet, 'SubJet_pt',        nSubJetString, nSubJetSizeMax)
  SubJetEta       = bookFloatArrayBranch(TreeFatJet, 'SubJet_eta',       nSubJetString, nSubJetSizeMax)
  SubJetPhi       = bookFloatArrayBranch(TreeFatJet, 'SubJet_phi',       nSubJetString, nSubJetSizeMax)
  SubJetM         = bookFloatArrayBranch(TreeFatJet, 'SubJet_mass',      nSubJetString, nSubJetSizeMax)
  SubJetRawFactor = bookFloatArrayBranch(TreeFatJet, 'SubJet_rawFactor', nSubJetString, nSubJetSizeMax)
  SubJetNBHadrons = bookIntArrayBranch(TreeFatJet,   'SubJet_nBHadrons', nSubJetString, nSubJetSizeMax)
  SubJetNCHadrons = bookIntArrayBranch(TreeFatJet,   'SubJet_nCHadrons', nSubJetString, nSubJetSizeMax)
  # 
  # SubGenJetAK8 branch
  #     
  nSubGenJetAK8SizeMax = 50
  nSubGenJetAK8String = 'nSubGenJetAK8'
  nSubGenJetAK8        = bookIntBranch(TreeFatJet, nSubGenJetAK8String)
  SubGenJetAK8Pt       = bookFloatArrayBranch(TreeFatJet, 'SubGenJetAK8_pt',   nSubGenJetAK8String, nSubGenJetAK8SizeMax)
  SubGenJetAK8Eta      = bookFloatArrayBranch(TreeFatJet, 'SubGenJetAK8_eta',  nSubGenJetAK8String, nSubGenJetAK8SizeMax)
  SubGenJetAK8Phi      = bookFloatArrayBranch(TreeFatJet, 'SubGenJetAK8_phi',  nSubGenJetAK8String, nSubGenJetAK8SizeMax)
  SubGenJetAK8M        = bookFloatArrayBranch(TreeFatJet, 'SubGenJetAK8_mass', nSubGenJetAK8String, nSubGenJetAK8SizeMax)

  # 
  # PV branch
  # 
  PVnpvs         = bookIntBranch(TreeFatJet, 'nPVnpvs')
  PVnpvsGood     = bookIntBranch(TreeFatJet, 'nPVnpvsGood')
  PileUpNTrueInt = bookFloatBranch(TreeFatJet, 'nPileUpNTrueInt')
  PileUpNPU      = bookIntBranch(TreeFatJet, 'nPileUpNPU')
  #
  # SetupTChain
  # 
  tree = ROOT.TChain("Events")
  for inFilePath in inFileList:
    print'Adding files: %s'%(inFilePath)
    tree.Add(inFilePath)

  tree.ls()
  #
  # Use TChain and Setup TTreeReader.
  #
  inTree  = InputTree(tree)
  
  #
  #
  #
  if isMC_QCD: branchSel = BranchSelection("branchSel_QCD.txt")
  else       : branchSel = BranchSelection("branchSel.txt")
  branchSel.selectBranches(inTree)

  numEvents = inTree.GetEntries()
  #
  # Set max number of events to process
  # Set to -1 if you want to run over all events
  #
  maxevents = -1
  # maxevents = 1000

  #
  # Loop over events
  # 
  print numEvents
  for iev in xrange(0,numEvents):
    # print iev
    if maxevents > 0 and iev > maxevents:
      break
    if (iev)%1000==0:
      print "Processing event %d out of %d" %(iev,numEvents)
    #
    # Load Event
    #
    evt = Event(inTree,iev)  
    #
    # Loop over fatjets
    #
    fatjets = Collection(evt, "FatJet")
    nFatJet[0]=0
    for i, fj in enumerate(fatjets):
      fj_p4                     = fj.p4()
      FatJetPt[i]               = fj_p4.Pt()
      FatJetEta[i]              = fj_p4.Eta()
      FatJetPhi[i]              = fj_p4.Phi()
      FatJetM[i]                = fj_p4.M()     
      if fj.tau1 > 0:
        FatJetTau21[i]          = fj.tau2/fj.tau1       
      else: 
        FatJetTau21[i]          = -1
      if fj.tau1 > 0:
        FatJetTau31[i]          = fj.tau3/fj.tau1       
      else:
        FatJetTau31[i]          = -1
      if fj.tau2 > 0:
        FatJetTau32[i]          = fj.tau3/fj.tau2       
      else:
        FatJetTau32[i]          = -1 

      FatJetDeepTagMDTvsQCD[i]  = fj.deepTagMD_TvsQCD
      FatJetDeepTagMDWvsQCD[i]  = fj.deepTagMD_WvsQCD
      FatJetDeepTagMDZvsQCD[i]  = fj.deepTagMD_ZvsQCD
      FatJetDeepTagTvsQCD[i]    = fj.deepTag_TvsQCD
      FatJetDeepTagWvsQCD[i]    = fj.deepTag_WvsQCD
      FatJetDeepTagZvsQCD[i]    = fj.deepTag_ZvsQCD
      FatJetDeepTagQCD[i]       = fj.deepTag_QCD
      FatJetDeepTagQCDOthers[i] = fj.deepTag_QCDothers
      FatJetMSoftDrop[i]        = fj.msoftdrop   
      FatJetRawFactor[i]        = fj.rawFactor
      FatJetJetId[i]            = fj.jetId
      FatJetSubJetIdx1[i]       = fj.subJetIdx1
      FatJetSubJetIdx2[i]       = fj.subJetIdx2
      FatJetGenJetAK8Idx[i]     = fj.genJetAK8Idx
      nFatJet[0]+= 1
    #
    # Loop over genparts
    #
    if isMC_QCD == False:
      particles = Collection(evt, "GenPart")
      nGenPart[0]=0
      for i, gp in enumerate(particles):
        GenPartPt[i]                = gp.pt
        GenPartEta[i]               = gp.eta
        GenPartPhi[i]               = gp.phi
        GenPartM[i]                 = gp.mass
        GenPartPdgId[i]             = gp.pdgId
        GenPartStatus[i]            = gp.status
        GenPartStatusFlags[i]       = gp.statusFlags
        GenPartGenPartIdxMother[i]  = gp.genPartIdxMother
        nGenPart[0]+=1
    # 
    # Loop over GenJetAK8
    #   
    jets = Collection(evt, "GenJetAK8")
    nGenJetAK8[0]=0
    for i, gj in enumerate(jets):
      GenJetAK8Pt[i]            = gj.pt      
      GenJetAK8Eta[i]           = gj.eta        
      GenJetAK8Phi[i]           = gj.phi       
      GenJetAK8M[i]             = gj.mass         
      GenJetAK8HadronFlavour[i] = gj.hadronFlavour
      GenJetAK8PartonFlavour[i] = gj.partonFlavour
      nGenJetAK8[0]+=1
    # 
    # Subjet over GenJetAK8
    #   
    subjets = Collection(evt, "SubJet")
    nSubJet[0]=0
    for i, sj in enumerate(subjets):
      SubJetPt[i]            = sj.pt      
      SubJetEta[i]           = sj.eta        
      SubJetPhi[i]           = sj.phi       
      SubJetM[i]             = sj.mass      
      SubJetRawFactor[i]     = sj.rawFactor
      SubJetNBHadrons[i]     = sj.nBHadrons
      SubJetNCHadrons[i]     = sj.nCHadrons
      nSubJet[0]+=1

    # 
    # Subjet over GenJetAK8
    #   
    subjets = Collection(evt, "SubGenJetAK8")
    nSubGenJetAK8[0]=0
    for i, sj in enumerate(subjets):
      SubGenJetAK8Pt[i]  = sj.pt      
      SubGenJetAK8Eta[i] = sj.eta        
      SubGenJetAK8Phi[i] = sj.phi       
      SubGenJetAK8M[i]   = sj.mass      
      nSubGenJetAK8[0]+=1
    #   
    # Loop over PV
    #   
    PVnpvs[0] = evt.PV_npvs
    PVnpvsGood[0] = evt.PV_npvsGood
    PileUpNTrueInt[0] = evt.Pileup_nTrueInt
    PileUpNPU[0] = evt.Pileup_nPU

    #
    # Fill the tree for this event
    #
    TreeFatJet.Fill()
  
  #
  # Save the output ttree in the output file
  #
  print "Write tree to file"
  f.Write()

  #
  # Gracefully close the output file
  #
  print "Closing output"
  f.Close()

#
#
#
def main(argv):
  #
  options = getUserOptions(argv)
  #
  # Get inputTextFile from options
  #
  inputTextFile = options.input
  #
  # Get sample name from inputTextFile name
  #
  sample = inputTextFile.replace('.txt', '')
  sample = sample.rsplit('/')[-1]
  #
  print "\n\n"
  print "****************************************"
  print ""
  print "START Processing sample: %s" %(sample)
  print ""
  print "****************************************"
  #
  # Get List of inputFiles 
  #
  print "List of NanoAOD input files from %s" %(inputTextFile)
  inFileList = getInputFiles(inputTextFile)

  #
  # Create output tree filename
  #
  outFilePath = "%s%s/Ntuple_%s.root" %(XROOTDIR,OUTPUTDIR,sample)
  #
  # Process each file
  #
  print 'Processing files'
  HarvestNanoAOD(inFileList,outFilePath,sample)

  print "****************************************"
  print ""
  print "END Processing sample: %s" %(sample)
  print ""
  print "****************************************"
  print "\n\n"


if __name__ == "__main__":
  main(sys.argv)