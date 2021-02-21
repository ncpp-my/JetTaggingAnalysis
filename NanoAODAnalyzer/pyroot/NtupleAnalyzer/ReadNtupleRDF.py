import sys, os, glob, ROOT, argparse
from collections import OrderedDict 
from array import array

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import InputTree

ROOT.gROOT.SetBatch()
ROOT.ROOT.EnableImplicitMT(4)

class MyDict(OrderedDict):
  def __missing__(self, key):
    val = self[key] = MyDict()
    return val

# ROOT.gInterpreter.Declare("""
# float DeltaR(float obj1_Eta, float obj1_Phi, float obj2_Eta, float obj2_Phi) {
#   return sqrt(pow(abs(obj1_Phi - obj2_Phi),2) + pow(abs(obj1_Eta - obj2_Eta),2));
# }

# """)

EOSUSER   = "root://eosuser.cern.ch/"
ntupleDir = "/eos/user/s/ssyedoma/AnaJetTagging/Ntuples_Old/"
outDir    = "/eos/user/s/ssyedoma/AnaJetTagging/Histos/"
if not os.path.exists(outDir): os.makedirs(outDir)

treeName = 'TreeFatJet'
signal = "WprimeWZ" #, "ZprimeToTT"

timer = ROOT.TStopwatch()

#
# declare signal dataframes
#
df_filter = MyDict()

sigFiles = glob.glob(ntupleDir+"*"+signal+"M*")
signalTree = ROOT.TChain(treeName)
map(signalTree.Add, sigFiles)
df = ROOT.ROOT.RDataFrame(signalTree)

#
# declare QCD background dataframes
#
bkgFiles = glob.glob(ntupleDir+"*QCDPt15To7000_part*")
bkgdTree = ROOT.TChain(treeName)
map(bkgdTree.Add, bkgFiles)
df_bkgd = ROOT.ROOT.RDataFrame(bkgdTree)

def main():
  ProcessDataFrame(df)

def ProcessDataFrame(df):

  gpList = {"W":24, "Z":23, "t":6, "b":5}

  df = df.Filter("nGenPart>0 && nFatJet>0") 
  df = df.Define("GenPart_BaseSel", "abs(GenPart_eta)<2.4").Filter("Sum(GenPart_BaseSel)>=1")
  df = df.Define("FatJet_BaseSel", "FatJet_pt>200 && abs(FatJet_eta)<2.4").Filter("Sum(FatJet_BaseSel)>=1")

  for gp in gpList:
    df = df.Define("%s_pdgId"%gp, "abs(GenPart_pdgId)==%s" %gpList[gp])
    df = df.Define("decayFrom%s"%gp, "abs(GenPart_pdgId[GenPart_genPartIdxMother])==%d" %gpList[gp])
  df   = df.Define("q_pdgId", "abs(GenPart_pdgId)<6")
  df = df.Define("inFatJet", "All(DeltaR(GenPart_eta, FatJet_eta, GenPart_phi, FatJet_phi)<0.8)")

  if "Zprime" in signal: df = recoTop(df)
  if "Wprime" in signal: df = recoW(df)

  histograms = MyDict()

  xbin, xmin, xmax = 50, 0, 5000
  ybin, ymin, ymax = 2000, 0, 1

  if "Zprime" in signal:
    df = df.Filter("pass_2qFromW_inFatJet")
    histograms["pt_deepAK8"] = df.Histo2D(("h_pt_deepAK8", "h_pt_deepAK8", xbin, xmin, xmax, ybin, ymin, ymax), "FatJet_pt", "FatJet_deepTag_TvsQCD")
    histograms["pt_tau32"]   = df.Histo2D(("h_pt_tau32", "h_pt_tau32", xbin, xmin, xmax, ybin, ymin, ymax), "FatJet_pt", "FatJet_tau32")
    histograms['qcd_pt_T_deepak8']   = df_bkgd.Histo2D(('hqcd_pt_T_deepak8', '', xbin, xmin, xmax, ybin, ymin, ymax), 'FatJet_pt', 'FatJet_deepTag_TvsQCD')
    # histograms['qcd_pt_T_deepak8md'] = df_bkgd.Histo2D(('hqcd_pt_T_deepak8md', '', xbin, xmin, xmax, ybin, ymin, ymax), 'FatJet_pt', 'FatJet_deepTagMD_TvsQCD')
    histograms['qcd_pt_tau32']       = df_bkgd.Histo2D(('hqcd_pt_tau32', '', xbin, xmin, xmax, ybin, ymin, ymax), 'FatJet_pt', 'FatJet_tau32')

  if "Wprime" in signal:
    histograms["pt_deepak8"]   = df.Histo2D(("h_pt_deepak8", "W-tagging DeepAK8 vs p_{T}; ;DeepAK8 score", xbin, xmin, xmax, ybin, ymin, ymax), "FatJet_pt", "FatJet_deepTag_WvsQCD")
    # histograms["pt_deepak8md"] = df.Histo2D(("h_pt_deepak8md", "h_pt_deepak8md", xbin, xmin, xmax, ybin, ymin, ymax), "FatJet_pt", "FatJet_deepTagMD_WvsQCD")
    histograms["pt_tau21"]     = df.Histo2D(("h_pt_tau21", "h_pt_tau21", xbin, xmin, xmax, ybin, ymin, ymax), "FatJet_pt", "FatJet_tau21")
    histograms['qcd_pt_W_deepak8']   = df_bkgd.Histo2D(('hqcd_pt_W_deepak8', '', xbin, xmin, xmax, ybin, ymin, ymax), 'FatJet_pt', 'FatJet_deepTag_WvsQCD')
    # histograms['qcd_pt_W_deepak8md'] = df_bkgd.Histo2D(('hqcd_pt_W_deepak8md', '', xbin, xmin, xmax, ybin, ymin, ymax), 'FatJet_pt', 'FatJet_deepTagMD_WvsQCD')
    histograms['qcd_pt_tau21']       = df_bkgd.Histo2D(('hqcd_pt_tau21', '', xbin, xmin, xmax, ybin, ymin, ymax), 'FatJet_pt', 'FatJet_tau21')
    
  histograms['qcd_pt_qcd_deepak8'] = df_bkgd.Histo2D(('hqcd_pt_qcd_deepak8', '', xbin, xmin, xmax, ybin, ymin, ymax), 'FatJet_pt', 'FatJet_deepTag_QCD')
  # histograms['qcd_pt_Z_deepak8']   = df_bkgd.Histo2D(('hqcd_pt_Z_deepak8', '', xbin, xmin, xmax, ybin, ymin, ymax), 'FatJet_pt', 'FatJet_deepTag_ZvsQCD')
  # histograms['qcd_pt_Z_deepak8md']   = df_bkgd.Histo2D(('hqcd_pt_Z_deepak8md', '', xbin, xmin, xmax, ybin, ymin, ymax), 'FatJet_pt', 'FatJet_deepTagMD_ZvsQCD')

  #
  # output root files
  #
  outFile = ROOT.TFile(outDir+"Histos_"+signal+".root", "RECREATE")
  outFile.cd("")

  for h in histograms:
    print h
    histograms[h].SetStats(0)
    histograms[h].SetOption("COLZ")
    histograms[h].Write()
  outFile.Close()


def recoTop(df):
  # at least 2q from W
  df = df.Define("pass_2qFromW"          ,"Sum(q_pdgId)>=2 && Sum(decayFromW)>=2")
  df = df.Define("pass_2qFromW_inFatJet" ,"Sum(q_pdgId)>=2 && Sum(decayFromW)>=2 && inFatJet")

  # at least 1 b from t
  df = df.Define("pass_bFromt"          , "Sum(b_pdgId)>=1 && Sum(decayFromt)>=1")
  df = df.Define("pass_bFromt_inFatJet" , "Sum(b_pdgId)>=1 && Sum(decayFromt)>=1 && inFatJet")

  # at least 1 W from t
  df = df.Define("pass_WFromt"           , "Sum(W_pdgId)>=1 && Sum(decayFromt)>=1 && pass_2qFromW")
  df = df.Define("pass_WFromt_inFatJet"  , "Sum(W_pdgId)>=1 && Sum(decayFromt)>=1 && pass_2qFromW_inFatJet && inFatJet && pass_2qFromW_inFatJet")
  
  # t -> bW -> bqq
  df = df.Define("pass_t"          , "Sum(t_pdgId)>=1 && pass_WFromt && pass_bFromt")
  df = df.Define("pass_t_inFatJet" , "Sum(t_pdgId)>=1 && pass_WFromt_inFatJet && pass_bFromt_inFatJet && inFatJet")

  return df

def recoW(df):
  # light quarks
  df = df.Define("qFromW"                , "q_pdgId && decayFromW")
  df = df.Define("pass_2qFromW"          , "Sum(qFromW)>=2")
  df = df.Define("pass_2qFromW_inFatJet" , "Sum(qFromW && inFatJet)>=2")

  # W -> qq
  df = df.Define("WTo2q"          , "W_pdgId && pass_2qFromW")
  df = df.Define("WTo2q_inFatJet" , "W_pdgId && pass_2qFromW_inFatJet")
  df = df.Define("pass_W"         , "Sum(WTo2q)>=1")

  return df

if __name__ == '__main__':
  main()

timer.Stop()
timer.Print()