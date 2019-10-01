#! /usr/bin/env python
import ROOT, copy, sys, logging
from array import array

# load FWLite C++ libraries
# ROOT.gSystem.Load("libFWCoreFWLite.so");
# ROOT.gSystem.Load("libDataFormatsFWLite.so");
# ROOT.FWLiteEnabler.enable()

from DataFormats.FWLite import Events, Handle

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

def bookFloatArrayBranch(tree, branchName, sizeBranchName, arraySize):
  tmp = array('f', arraySize*[0.])
  tree.Branch(branchName, tmp, '%s[%s]/F' %(branchName,sizeBranchName))
  return tmp

##########################################################
#
#
# HarvestMiniAOD
#
#
##########################################################
def HarvestMiniAOD(inFilePath, outFilePath):
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
  FatJetPt  = bookFloatArrayBranch(TreeFatJet, 'FatJet_Pt',  nFatJetString, nFatJetSizeMax)
  FatJetEta = bookFloatArrayBranch(TreeFatJet, 'FatJet_Eta', nFatJetString, nFatJetSizeMax)
  FatJetPhi = bookFloatArrayBranch(TreeFatJet, 'FatJet_Phi', nFatJetString, nFatJetSizeMax)
  FatJetM   = bookFloatArrayBranch(TreeFatJet, 'FatJet_M'  , nFatJetString, nFatJetSizeMax)
  #
  # 
  #
  ak8jetLabel = "slimmedJetsAK8"
  ak8jets = Handle("std::vector<pat::Jet>")

  # 
  # Read in the MiniAOD file
  # 
  events = Events (inFilePath)
  
  #
  # Get number of events in MiniAOD file
  #
  numEvents = events.size()
  
  #
  # Set max number of events to process
  # Set to -1 if you want to run over all events
  #
  maxevents = -1
  
  #
  # The Event Loop
  #
  print "Looping over %d events " %(numEvents)

  for iev, event in enumerate(events):
    #
    # 
    #
    if maxevents > 0 and iev > maxevents:
      break
    if (iev+1)%100==0:
      print "Processing event %d out of %d" %(iev,numEvents)

    #
    # Get jets
    #
    event.getByLabel (ak8jetLabel, ak8jets)  
    
    #
    # Loop over jets
    #
    nFatJet[0]=0
    for i,jet in enumerate(ak8jets.product()):
      jetP4 = ROOT.TLorentzVector( jet.px(), jet.py(), jet.pz(), jet.energy() )

      FatJetPt[i]  = jetP4.Pt()
      FatJetEta[i] = jetP4.Eta()
      FatJetPhi[i] = jetP4.Phi()
      FatJetM[i]   = jetP4.M()

      nFatJet[0] += 1
    
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
  print "Closing output file"
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
  print "List of MiniAOD input files from %s" %(inputTextFile)
  inFileList = getInputFiles(inputTextFile)
  #
  # Loop over files
  #
  for fNum, inFilePath in enumerate(inFileList):
    #
    # Create output tree filename
    #
    outFilePath = "%s_%s_%d.root" %(options.outputPrefix,sample,fNum)
    #
    # Process each file
    #
    print 'Processing file ' + inFilePath
    HarvestMiniAOD(inFilePath,outFilePath)

  print "****************************************"
  print ""
  print "END Processing sample: %s" %(sample)
  print ""
  print "****************************************"
  print "\n\n"

if __name__ == "__main__":
  main(sys.argv)

  