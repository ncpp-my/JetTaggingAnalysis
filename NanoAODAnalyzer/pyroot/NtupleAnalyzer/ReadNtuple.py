import os, glob, ROOT, optparse
from collections import OrderedDict 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import InputTree

ROOT.gROOT.SetBatch()

usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("--sample",  action="store",        default="QCDPt15To7000_part17",  dest="sample", type="str")
parser.add_option("--batch",   action="store_true",   default=False,            dest="batch")
(options, args) = parser.parse_args()

doBatch = options.batch
sample = options.sample
doQCD = 'QCD' in sample
treeName = "TreeFatJet"

#
# CHECK !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
version = "ULv2"
EOSUSER = "root://eosuser.cern.ch/"
inDir   = "/eos/user/s/ssyedoma/AnaJetTagging/Ntuples/%s/"%version
outDir  = "/eos/user/s/ssyedoma/AnaJetTagging/Histos/%s/"%version

#
# setup histograms
#
histos = OrderedDict()
histos['W_num'] = ROOT.TH1F("h_W_num", "; W boson p_{T} [GeV]; Efficiency", 10, 100., 600.)
histos['q_num'] = ROOT.TH1F("h_q_num", ""                                 , 10, 100., 600.)
histos['W_den'] = ROOT.TH1F("h_W_den", "; W boson p_{T} [GeV]; Efficiency", 10, 100., 600.)
histos['q_den'] = ROOT.TH1F("h_q_den", ""                                 , 10, 100., 600.)

if not doQCD:
  histos['deepak8md'] = ROOT.TH2F("h_pt_deepak8md", "W-tagging DeepAK8-MD vs p_{T}; p_{T}; DeepAK8"                 , 50, 0., 5000., 2000, 0., 1.)
  histos['deepak8']   = ROOT.TH2F("h_pt_deepak8"  , "W-tagging DeepAK8 vs p_{T}; p_{T}; DeepAK8"                    , 50, 0., 5000., 2000, 0., 1.)
  histos['sdtau21']   = ROOT.TH2F("h_pt_sdtau21", "W-tagging m_{SD}+#tau_{21} vs p_{T}; p_{T}; m_{SD} + #tau_{21}", 50, 0., 5000., 2000, 0., 1.)
else:
  histos['deepak8md'] = ROOT.TH2F("h_pt_deepak8md", "QCD DeepAK8-MD vs p_{T}; p_{T}; DeepAK8"                 , 50, 0., 5000., 2000, 0., 1.)
  histos['deepak8']   = ROOT.TH2F("h_pt_deepak8"  , "QCD DeepAK8 vs p_{T}; p_{T}; DeepAK8"                    , 50, 0., 5000., 2000, 0., 1.)
  histos['sdtau21']    = ROOT.TH2F("h_pt_sdtau21", "QCD m_{SD}+#tau_{21} vs p_{T}; p_{T}; m_{SD} + #tau_{21}", 50, 0., 5000., 2000, 0., 1.)

outHistoList = ['deepak8', 'deepak8md', 'sdtau21']
timer = ROOT.TStopwatch()

if doBatch:
  inFileList = [EOSUSER+inDir+'Ntuple_%s.root'%sample]
else:
  inFileList = [EOSUSER+f for f in glob.glob(inDir+'Ntuple_%s*.root'%sample)]
tree = ROOT.TChain(treeName)
map(tree.Add, inFileList)

inTree  = InputTree(tree)
nEvents = inTree.GetEntries()
# nEvents = 1000

""" LOOP OVER EVENTS """
print "running over sample %s with %d events" %(sample, nEvents)
for i in xrange(0, nEvents):

  if i%10000==0: print "%d out of %d events" %(i,nEvents)
  
  evt       = Event(inTree,i)
  fatjet    = Collection(evt, "FatJet")

  if doQCD:
    for fj in fatjet:
      histos['deepak8md'].Fill(fj.pt, fj.deepTagMD_WvsQCD)
      histos['deepak8'].Fill(fj.pt, fj.deepTag_WvsQCD)
            
      if fj.msoftdrop>65. and fj.msoftdrop<105.:
        histos['sdtau21'].Fill(fj.pt, fj.tau21)
  
  else:
    particles = Collection(evt, "GenPart")

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
    
    # QfromZ = [x for x in particles if (x.genPartIdxMother>=0 and abs(x.pdgId)<6 and abs(particles[x.genPartIdxMother].pdgId) == 23 and abs(x.eta)<2.4 and abs(particles[x.genPartIdxMother].eta)<2.4)]

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
            histos['deepak8md'].Fill(fj.pt, fj.deepTagMD_WvsQCD)

          if fj.msoftdrop>65. and fj.msoftdrop<105.:
            histos['sdtau21'].Fill(fj.pt, fj.tau21)

timer.Print()
timer.Continue()
if doBatch: print "Process_Read::DONE"

if not doQCD:
  histos['W_eff'] = ROOT.TEfficiency(histos['W_num'], histos['W_den'])
  histos['q_eff'] = ROOT.TEfficiency(histos['q_num'], histos['q_den'])

#
# output root file
#
suffix = "_tag_pt"
outFile = ROOT.TFile("%sHisto_%s%s.root" %(outDir, sample, suffix), "RECREATE")

for h in outHistoList:
  histos[h].SetStats(0)
  histos[h].SetOption("COLZ")
  histos[h].Write()

outFile.Close()