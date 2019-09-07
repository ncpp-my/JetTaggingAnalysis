import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import sys

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import * #deltaR, matching etc..

class JetTaggingOneLeptonNanoSkimmer(Module):
  def __init__(self, isMC, era, doSkim=False):
    self.era = era
    self.isMC = isMC
    self.doSkim = doSkim
    self.writeHistFile=True

  def beginJob(self,histFile=None,histDirName=None):
    Module.beginJob(self,histFile,histDirName)
    self.h_cutflow_uw = ROOT.TH1F('h_cutflow_uw','h_cutflow_uw', 10, 0, 10)
    self.h_cutflow_w  = ROOT.TH1F('h_cutflow_w', 'h_cutflow_w',  10, 0, 10)
    self.h_cutflow_uw.GetXaxis().SetBinLabel(1,"Cut0:NoSelection")
    self.h_cutflow_uw.GetXaxis().SetBinLabel(2,"Cut1:>=1LooseLeptons")
    self.h_cutflow_uw.GetXaxis().SetBinLabel(3,"Cut2:>=1LooseFatJets")

    self.h_cutflow_w.GetXaxis().SetBinLabel(1,"Cut0:NoSelection")
    self.h_cutflow_w.GetXaxis().SetBinLabel(2,"Cut1:>=1LooseLeptons")
    self.h_cutflow_w.GetXaxis().SetBinLabel(3,"Cut2:>=1LooseFatJets")

    self.addObject(self.h_cutflow_uw)
    self.addObject(self.h_cutflow_w)
  
  def endJob(self):
    Module.endJob(self)

  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    pass

  def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    pass

  def RegisterCut(self, cutName, weight):
    self.h_cutflow_uw.Fill(cutName,1)
    self.h_cutflow_w.Fill(cutName, weight)

  def analyze(self, event):
    """process event, return True (go to next module) or False (fail, go to next event)"""
    electrons = list(Collection(event, "Electron"))
    muons     = list(Collection(event, "Muon"))
    fatjets   = list(Collection(event, "FatJet"))

    evtweight = 1.0
    if self.isMC:
      evtweight = event.genWeight

    #################################################
    # Register cut before ANY selection
    ##################################################
    self.RegisterCut("Cut0:NoSelection",evtweight)

    #################################################
    #
    # Lepton selection 
    #
    ##################################################
    #
    # Select electrons
    #
    electronsLoose    = []
    for el in electrons: 
      #
      # Loose selection
      #
      if el.pt < 21. or abs(el.eta) > 2.5: continue
      if el.cutBased < 1: continue
      electronsLoose.append(el)
    #
    # Select muons
    #
    muonsLoose = []
    for mu in muons:
      #
      # Loose selection
      #
      if mu.pt < 21. or abs(mu.eta) > 2.4: continue
      if mu.looseId is False: continue
      muonsLoose.append(mu) 
    #
    # Count the number of loose leptons
    #
    nElectronsLoose = len(electronsLoose)
    nMuonsLoose     = len(muonsLoose)
    nLeptonsLoose   = nMuonsLoose + nElectronsLoose

    #
    # CHECK: ATLEAST 1 Loose leptons.
    # Skip event if doSkim=True
    #
    if nLeptonsLoose < 1:
      if self.doSkim: 
        return False
    else:
      self.RegisterCut("Cut1:>=1LooseLeptons",evtweight)
    
    #################################################
    #
    # Fatjet selection 
    #
    ##################################################
    fatjetsLoose = []
    for fatjet in fatjets:
      #
      # Fatjet selection
      #
      if fatjet.pt < 180.: continue 
      if abs(fatjet.eta) > 2.5: continue 
      fatjetsLoose.append(fatjet)
    #
    # Count the number of loose fatjets
    #
    nFatjetsLoose = len(fatjetsLoose)

    #
    # CHECK: ATLEAST 1 Loose fatjet.
    # Skip event if doSkim=True
    #
    if nFatjetsLoose < 1:
      if self.doSkim: 
        return False
    else:
      self.RegisterCut("Cut2:>=1LooseFatjets",evtweight)

    return True
                
# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
JetTaggingOneLeptonNanoSkimmer_2016_mc_sig   = lambda : JetTaggingOneLeptonNanoSkimmer(isMC=True, era="2016",doSkim=False) 
JetTaggingOneLeptonNanoSkimmer_2016_mc_bkgd  = lambda : JetTaggingOneLeptonNanoSkimmer(isMC=True, era="2016",doSkim=True) 
JetTaggingOneLeptonNanoSkimmer_2016_data     = lambda : JetTaggingOneLeptonNanoSkimmer(isMC=False,era="2016",doSkim=True) 
