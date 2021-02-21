import sys, os, glob, ROOT
from collections import OrderedDict 
from array import array
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import InputTree

ROOT.gROOT.SetBatch()

EOSUSER = "root://eosuser.cern.ch/"
outDir  = "/eos/user/s/ssyedoma/AnaJetTagging/Histos/"
inDir   = "/eos/user/s/ssyedoma/AnaJetTagging/Ntuples_Old/"

sigName  = 'WprimeWZ'
treeName = "TreeFatJet"

masses = ["600","800","1000","1200","1400","1600","2000","2500","3000","3500","4000","4500","5000","5500","6000","6500","7000","7500","8000"]
# masses = ["600"]


#
# setup histograms
histos = OrderedDict()
histos['W_num'] = ROOT.TH1F("h_W_num", "; W boson p_{T} [GeV]; Efficiency", 10, 100., 600.)
histos['q_num'] = ROOT.TH1F("h_q_num", ""                                 , 10, 100., 600.)
histos['W_den'] = ROOT.TH1F("h_W_den", "; W boson p_{T} [GeV]; Efficiency", 10, 100., 600.)
histos['q_den'] = ROOT.TH1F("h_q_den", ""                                 , 10, 100., 600.)

histos['deepak8md'] = ROOT.TH2F("h_pt_deepak8md", "W-tagging DeepAK8-MD vs p_{T}; p_{T}; DeepAK8"                 , 50, 0., 5000., 2000, 0., 1.)
histos['deepak8']   = ROOT.TH2F("h_pt_deepak8"  , "W-tagging DeepAK8 vs p_{T}; p_{T}; DeepAK8"                    , 50, 0., 5000., 2000, 0., 1.)
histos['tau21']     = ROOT.TH2F("h_pt_tau21"    , "W-tagging #tau_{21} vs p_{T}; p_{T}; #tau_{21}"                , 50, 0., 5000., 2000, 0., 1.)
histos['sdtau21']   = ROOT.TH2F("h_pt_sdtau21", "W-tagging m_{SD}+#tau_{21} vs p_{T}; p_{T}; m_{SD} + #tau_{21}", 50, 0., 5000., 2000, 0., 1.)

outHistoList = [
  'deepak8'
]

timer = ROOT.TStopwatch()

inFileList = [EOSUSER+f for f in glob.glob(inDir+'Ntuple_%sM*.root'%sigName)]
tree = ROOT.TChain(treeName)
map(tree.Add,inFileList)

inTree  = InputTree(tree)
nEvents = inTree.GetEntries()

### LOOP OVER EVENTS ###
print "running over %d events" %nEvents
for i in xrange(0, nEvents):

  if i%10000==0: print "%d out of %d events" %(i,nEvents)
  
  evt       = Event(inTree,i)
  particles = Collection(evt, "GenPart")
  fatjet    = Collection(evt, "FatJet")
  jetak8    = Collection(evt, "GenJetAK8")

  #
  # setup daughter particles
  #
  for idx, gp in enumerate(particles):
    if not hasattr(gp, 'dauIdx'):
       gp.dauIdx = []
    if gp.genPartIdxMother >= 0:
      mom = particles[gp.genPartIdxMother]
      if not hasattr(mom, 'dauIdx'): mom.dauIdx = [idx]
      else                         : mom.dauIdx.append(idx)

  def getFinal(gp):
    for idx in gp.dauIdx:
      dau = particles[idx]
      if dau.pdgId == gp.pdgId:
        return getFinal(dau)
    return gp

  nW = [x for x in particles if (abs(x.pdgId)==24 and abs(x.eta)<2.4)]
  if len(nW)<1: continue
  
  QfromZ = [x for x in particles if (x.genPartIdxMother>=0 and abs(x.pdgId)<6 and abs(particles[x.genPartIdxMother].pdgId) == 23 and abs(x.eta)<2.4 and abs(particles[x.genPartIdxMother].eta)<2.4)]

  Wfinal = None
  for wb in nW: Wfinal = getFinal(wb)
  
  QfromW = [x for x in particles if (x.genPartIdxMother>=0 and abs(x.pdgId)<6 and x.genPartIdxMother == Wfinal._index and abs(x.eta)<2.4)]
  
  nW = []
  nW.append(Wfinal)

  for wb in nW:
    histos['W_den'].Fill(wb.pt)
    histos['q_den'].Fill(wb.pt)

  Winfj = []
  qinfj  = []
  for fj in fatjet:
    if fj.pt>200. and abs(fj.eta)<2.4:
      Winfj = [(x,x.pt) for x in nW if (len(nW)>0 and x.DeltaR(fj)<0.8)]
      Winfj.sort(key=lambda x: x[1])
  
      if len(Winfj)>0:
        W0 = Winfj[-1][0] # leading W boson
        histos['W_num'].Fill(W0.pt)
      
      qinfj = [(x,x.pt) for x in QfromW if (len(QfromW)>=2 and x.DeltaR(fj)<0.8)]
      qinfj.sort(key=lambda x: x[1])
      
      if len(qinfj)>=2:
        q0 = qinfj[-1][0] # leading quark
        q1 = qinfj[-2][0] # subleading quark
        histos['q_num'].Fill(particles[q0.genPartIdxMother].pt)
 
        if q0.DeltaR(fj)<0.8 and q1.DeltaR(fj)<0.8 and particles[q0.genPartIdxMother].DeltaR(fj)<0.8:
          histos['deepak8'].Fill(fj.pt, fj.deepTag_WvsQCD)
          # histos['deepak8md'].Fill(fj.pt, fj.deepTagMD_WvsQCD)
          histos['tau21'].Fill(fj.pt, fj.tau21)

        if fj.msoftdrop>65. and fj.msoftdrop<105.:
          histos['sdtau21'].Fill(fj.pt, fj.tau21)
timer.Print()
timer.Continue()

histos['W_eff'] = ROOT.TEfficiency(histos['W_num'], histos['W_den'])
histos['q_eff'] = ROOT.TEfficiency(histos['q_num'], histos['q_den'])

#
# output root file
#
suffix = "_tagger_pt_all"
outFile = ROOT.TFile("%s%s%s.root" %(outDir, sigName, suffix), "RECREATE")

for h in outHistoList:
  histos[h].SetStats(0)
  histos[h].SetOption("COLZ")
  histos[h].Write()

outFile.Close()