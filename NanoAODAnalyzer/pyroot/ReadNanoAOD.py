import sys
import os
import glob
import ROOT

from collections import OrderedDict 
from array       import array

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import InputTree

ROOT.gROOT.SetBatch()

def getUserOptions(argv):
  from optparse import OptionParser
  parser = OptionParser()

  def add_option(option, **kwargs):
    parser.add_option('--' + option, dest=option, **kwargs)

  add_option('input',        default='',            help='Name of file with list of input files')
  add_option('outputPrefix', default='Ntuple',      help='Prefix of root output file')
  add_option('maxevents',    default=-1,            help='Number of events to run. -1 is all events')

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
      pfn = 'root://xrootd-cms.infn.it/' + lfn
      print 'Adding ' + pfn
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
  tree.Branch(branchName, tmp, '%s/I' % branchName)
  return tmp

def bookFloatBranch(tree, branchName):
  tmp = array('f', [0.])
  tree.Branch(branchName, tmp, '%s/F' %(branchName,sizeBranchName))
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
def HarvestNanoAOD(inFilePath, outFilePath):
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
  print "Create Output Tree: %s" %(treeName) 
  TreeFatJet = ROOT.TTree(treeName, treeName)
  #
  # FatJet branch
  #
  nFatJetSizeMax = 10
  nFatJetString  = 'nFatJet'
  nFatJet   = bookIntBranch(TreeFatJet, nFatJetString)
  FatJetPt  = bookFloatArrayBranch(TreeFatJet, 'FatJet_pt',  nFatJetString, nFatJetSizeMax)
  FatJetEta = bookFloatArrayBranch(TreeFatJet, 'FatJet_eta', nFatJetString, nFatJetSizeMax)
  FatJetPhi = bookFloatArrayBranch(TreeFatJet, 'FatJet_phi', nFatJetString, nFatJetSizeMax)
  FatJetM   = bookFloatArrayBranch(TreeFatJet, 'FatJet_m'  , nFatJetString, nFatJetSizeMax)

  #
  # SetupTChain
  # 
  tree = ROOT.TChain("Events")
  tree.Add(inFilePath)
  #
  # Use TChain and Setup TTreeReader.
  #
  inTree  = InputTree(tree)
  numEvents = inTree.entries
  #
  # Set max number of events to process
  # Set to -1 if you want to run over all events
  #
  maxevents = -1
  # maxevents = 5

  #
  # Loop over events
  # 
  for iev in xrange(0,numEvents):
    if maxevents > 0 and iev > maxevents:
      break
    if (iev)%250==0:
      print "Processing event %d out of %d" %(iev,numEvents)
    #
    # Load Event
    #
    evt = Event(inTree,iev)
    #
    # GenParticles
    #
    particles = Collection(evt, "GenPart")
    #
    # Loop over jets
    #
    fatjets = Collection(evt, "FatJet")
    nFatJet[0]=0
    for i, fj in enumerate(fatjets):
      fj_p4 = fj.p4()
      FatJetPt[i]  = fj_p4.Pt()
      FatJetEta[i] = fj_p4.Eta()
      FatJetPhi[i] = fj_p4.Phi()
      FatJetM[i]   = fj_p4.M()
      nFatJet[0]   += 1
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

  # maxfiles = -1
  maxfiles = -3
  #
  # Loop over files
  #
  for fNum, inFilePath in enumerate(inFileList):

    if maxfiles > 0 and fNum > maxfiles:
      break
    #
    # Create output tree filename
    #
    outFilePath = "%s_%s_%d.root" %(options.outputPrefix,sample,fNum)
    #
    # Process each file
    #
    print 'Processing file ' + inFilePath
    HarvestNanoAOD(inFilePath,outFilePath)

  print "****************************************"
  print ""
  print "END Processing sample: %s" %(sample)
  print ""
  print "****************************************"
  print "\n\n"


if __name__ == "__main__":
  main(sys.argv)
