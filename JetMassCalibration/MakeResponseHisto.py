import sys
import os
import glob
import ROOT
import argparse

from collections import OrderedDict
ROOT.gROOT.SetBatch()

ROOT.gInterpreter.Declare('#include "Helpers.h"')

# treeName = "Events"
treeName = "TreeFatJet"

EOSUSER="root://eosuser.cern.ch/"
INDIR="/eos/user/n/nbinnorj/AnaJetTagging/Ntuples/"

def main():
  ROOT.gInterpreter.ProcessLine('.L def.h+')

  parser = argparse.ArgumentParser("")
  parser.add_argument('-s', '--sample', type=str, default="")
  parser.add_argument('-c', '--cores',  type=int, default=1)

  args = parser.parse_args()
  sampleName   = args.sample
  ncores       = args.cores

  if ncores > 1:
    ROOT.ROOT.EnableImplicitMT(ncores)

  # Get sample files
  #
  sampleFiles = []

  if sampleName == "WprimeWZ":
    sampleFiles = [EOSUSER+f for f in glob.glob(INDIR+"Ntuple_WprimeWZM*.root")]
  elif sampleName == "ZprimeToTT":
    sampleFiles = [EOSUSER+f for f in glob.glob(INDIR+"Ntuple_ZprimeToTTM*.root")]
  elif sampleName == "QCDPt15To7000":
    sampleFiles = [EOSUSER+f for f in glob.glob(INDIR+"Ntuple_QCDPt15To7000*.root")]
  
  print "\n"
  print "======================================================"
  print "Processing sampleName", sampleName
  #
  #
  #
  inFileListVec = ROOT.std.vector('string')()
  for sampleFile in sampleFiles:
    inFileListVec.push_back(sampleFile)
    # inFileListVec.push_back("/afs/cern.ch/work/n/nbinnorj/Samples/Nano/store/mc/RunIIAutumn18NanoAODv7/Wprime_ggF_WZ_WhadZlep_narrow_M2000_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/100000/6F3FD75A-C578-D846-9D0C-26AC28C55C83.root")
  #
  #
  #
  df = ROOT.RDataFrame(treeName, inFileListVec)
  df = df.Filter("nFatJet>=1").Filter("nGenJetAK8>=1")
  #
  #
  #
  df = df.Define("GenPart_motherPDGID",   "GetMotherPDGID(GenPart_genPartIdxMother,GenPart_pdgId)")
  df = df.Define("GenPart_isWBoson",      "abs(GenPart_pdgId)==24")
  df = df.Define("GenPart_isZBoson",      "abs(GenPart_pdgId)==23")
  df = df.Define("GenPart_isQ",           "abs(GenPart_pdgId)>=1 && abs(GenPart_pdgId)<=5")
  df = df.Define("GenPart_isQFromWBoson", "GenPart_isQ&&(abs(GenPart_motherPDGID)==24)")
  df = df.Define("GenPart_isQFromZBoson", "GenPart_isQ&&(abs(GenPart_motherPDGID)==23)")
  # df = df.Define("GenPart_p4",            "return ROOT::VecOps::Construct<ROOT::Math::PtEtaPhiMVector>(GenPart_pt,GenPart_eta,GenPart_phi,GenPart_mass);")
  #
  #
  df = df.Define("GenJetAK8_flavLabels", "FatJetGenFlavourLabels(GenJetAK8_eta,GenJetAK8_phi,GenPart_eta,GenPart_phi,GenPart_isWBoson,GenPart_isZBoson,GenPart_isQFromWBoson,GenPart_isQFromZBoson)")
  df = df.Define("GenJetAK8_isWJet",     "GenJetAK8_flavLabels[0]")
  df = df.Define("GenJetAK8_isZJet",     "GenJetAK8_flavLabels[1]")
  df = df.Define("GenJetAK8_msoftdrop",  "MSoftGenJetAK8(GenJetAK8_eta,GenJetAK8_phi,SubGenJetAK8_pt,SubGenJetAK8_eta,SubGenJetAK8_phi,SubGenJetAK8_mass)")
  #
  #
  # df = df.Define("FatJet_p4",                   "return ROOT::VecOps::Construct<ROOT::Math::PtEtaPhiMVector>(FatJet_pt,FatJet_eta,FatJet_phi,FatJet_mass);")
  df = df.Define("FatJet_flavLabels",            "FatJetGenFlavourLabels(FatJet_eta,FatJet_phi,GenPart_eta,GenPart_phi,GenPart_isWBoson,GenPart_isZBoson,GenPart_isQFromWBoson,GenPart_isQFromZBoson)")
  df = df.Define("FatJet_isWJet",                "FatJet_flavLabels[0]")
  df = df.Define("FatJet_isZJet",                "FatJet_flavLabels[1]")
  df = df.Define("FatJet_msoftdrop_raw",         "MSoftRaw(FatJet_subJetIdx1,FatJet_subJetIdx2,SubJet_pt,SubJet_eta,SubJet_phi,SubJet_mass,SubJet_rawFactor)")
  df = df.Define("FatJet_matchgenak8_kin",       "MatchedGenJetAK8Kin(FatJet_genJetAK8Idx,GenJetAK8_pt,GenJetAK8_msoftdrop)")
  df = df.Define("FatJet_matchgenak8_pt",        "FatJet_matchgenak8_kin[0]")
  df = df.Define("FatJet_matchgenak8_msoftdrop", "FatJet_matchgenak8_kin[1]")
  df = df.Define("FatJet_response_msoftdrop_raw","FatJet_msoftdrop_raw/FatJet_matchgenak8_msoftdrop")
  df = df.Define("FatJet_response_msoftdrop",    "FatJet_msoftdrop/FatJet_matchgenak8_msoftdrop")
  df = df.Define("FatJet_passPresel_WJet",       "(FatJet_pt>200)&&(abs(FatJet_eta)<2.4)&&(FatJet_matchgenak8_pt>=0.000)&&(FatJet_matchgenak8_msoftdrop>=0.00000)&&FatJet_isWJet")

  columnNames = df.GetColumnNames()
  columnNamesFinal = ROOT.vector('string')()
  for cName in columnNames:
    if "_p4" in str(cName): continue
    if "_flavLabels" in str(cName): continue
    if "_matchgenak8_kin" in str(cName): continue
    columnNamesFinal.emplace_back(cName)

  histos = OrderedDict()

  histos["h2_msoftrawresp_vs_pt"] = df.Histo2D(("h2_msoftrawresp_vs_pt",  "",  100, 0., 5000., 30,  0.,   3.),  "FatJet_pt", "FatJet_response_msoftdrop_raw", "FatJet_passPresel_WJet")
  histos["h2_msoftresp_vs_pt"]    = df.Histo2D(("h2_msoftresp_vs_pt",     "",  100, 0., 5000., 30,  0.,   3.),  "FatJet_pt", "FatJet_response_msoftdrop",     "FatJet_passPresel_WJet")

  histos["h2_msoftraw_vs_pt"]     = df.Histo2D(("h2_msoftraw_vs_pt",     "",    100, 0., 5000., 50,  0., 250.),  "FatJet_pt", "FatJet_msoftdrop_raw",  "FatJet_passPresel_WJet")
  histos["h2_msoft_vs_pt"]        = df.Histo2D(("h2_msoft_vs_pt",        "",    100, 0., 5000., 50,  0., 250.),  "FatJet_pt", "FatJet_msoftdrop",      "FatJet_passPresel_WJet")
  histos["h2_genmsoft_vs_pt"]     = df.Histo2D(("h2_genmsoft_vs_pt",     "",    100, 0., 5000.,  50,  0., 250.), "FatJet_pt", "FatJet_matchgenak8_msoftdrop", "FatJet_passPresel_WJet")

  df_count = df.Count()
  print "nevents = %d" %(df_count.GetValue())

  outHistoFile = ROOT.TFile("./rootfiles/Histo_"+sampleName+".root","RECREATE")
  for h in histos:
    histos[h].Write()
  outHistoFile.Close()


  # df.Snapshot("TreeFatJet", "./rootfiles/SkimRDF_"+sampleName+".root", columnNamesFinal)
  

if __name__ == "__main__":
  main()