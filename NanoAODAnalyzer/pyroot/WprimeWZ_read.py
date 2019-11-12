import sys
import os
import glob
import ROOT
from collections import OrderedDict 
from array import array

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import InputTree

ROOT.gROOT.SetBatch()

EOSUSER   ="root://eosuser.cern.ch/"
treeName  ="TreeFatJet"
outDir = "/eos/user/s/ssyedoma/AnaJetTagging/ANALYSIS/eff/"

# massW = ["600"]
massW = ["600","800","1000","1200","1400","1600","2000","2500","3000","3500","4000","4500","5000","5500","6000","6500","7000","7500","8000"]
p = [massW,"WprimeWZ","WprimeWZM"] 

QQfromZ=[]
QQfromZ_AK8=[]
QQfromW=[]
QQfromW_AK8=[]
fjm=[]
fjmsd=[]

### DEFINE HISTOGRAMS ###
bins = 10000
h_WToQQ_pt   = ROOT.TH1F("h_WToQQ_pt", "W to QQ (pt);pt;No.of events", bins, 0., 1000.)
h_WToQQ_dr   = ROOT.TH1F("h_WToQQ_dr", "W to QQ (dR);dR;No.of events", bins, 0., .8)
h_ZToQQ_pt   = ROOT.TH1F("h_ZToQQ_pt", "Z to QQ (pt);pt;No.of events", bins, 0., 1000.)
h_ZToQQ_dr   = ROOT.TH1F("h_ZToQQ_dr", "Z to QQ (dR);dR;No.of events", bins, 0., .8)
h_deepAK8    = ROOT.TH1F("h_deepAK8", "W-tagging DeepAK8; DeepAK8; No.of events", bins, 0., 1.)
h_tau21      = ROOT.TH1F("h_tau21","W-tagging; #tau_{21}; #tau21; No. of events", bins, 0., 1.)
h_tau31      = ROOT.TH1F("h_tau31","W-tagging; #tau_{31}; #tau31; No. of events", bins, 0., 1.)
h_tau32      = ROOT.TH1F("h_tau32","W-tagging; #tau_{32}; #tau32; No. of events", bins, 0., 1.)
h_tau21_msd  = ROOT.TH1F("h_tau21_msd","W-tagging; m_{SD} + #tau_{21}; No. of events", bins, 0., 1.)
h_tau31_msd  = ROOT.TH1F("h_tau31_msd","W-tagging; m_{SD} + #tau_{31}; No. of events", bins, 0., 1.)
h_tau32_msd  = ROOT.TH1F("h_tau32_msd","W-tagging; m_{SD} + #tau_{32}; No. of events", bins, 0., 1.)

h_fj_m       = ROOT.TH1F("h_fj_m","Fatjet Mass ; Mass (GeV); No. of events", 30, 0., 500.)
h_fj_msd     = ROOT.TH1F("h_fj_msd", "", 30, 0., 500.)

h_W_eff      = ROOT.TH1F("h_W_eff", "; W boson p_{T} [GeV]; Efficiency", 10, 100., 600.)
h_q_eff      = ROOT.TH1F("h_q_eff", "", 10, 100., 600.)
h_q_eff_0    = ROOT.TH1F("h_q_eff_0", "", 10, 100., 600.)
h_q_eff_1    = ROOT.TH1F("h_q_eff_1", "", 10, 100., 600.)
h_W_den      = ROOT.TH1F("h_W_den", "; W boson p_{T} [GeV]; Efficiency", 10, 100., 600.)
h_q_den      = ROOT.TH1F("h_q_den", "", 10, 100., 600.)

h_pt_deepAK8   = ROOT.TH2F("h_pt_deepAK8", "W-tagging DeepAK8 vs p_{T}; p_{T}; DeepAK8", 50, 0., 5000., 2000, 0., 1.)
h_pt_tau21     = ROOT.TH2F("h_pt_tau21", "W-tagging #tau_{21} vs p_{T}; p_{T}; #tau_{21}", 50, 0., 5000., 2000, 0., 1.)
h_pt_msd_tau21 = ROOT.TH2F("h_pt_msd_tau21", "W-tagging m_{SD}+#tau_{21} vs p_{T}; p_{T}; m_{SD} + #tau_{21}", 50, 0., 5000., 2000, 0., 1.)

h_W_msd        = ROOT.TH1F("h_W_msd", "; m_{SD} [GeV]; A.U.", 100, 0., 200.)

histoList = [
  # h_WToQQ_pt,
  # h_WToQQ_dr,
  # h_ZToQQ_pt,
  # h_ZToQQ_dr,
  # h_deepAK8,
  # h_tau21,
  # h_tau31,
  # h_tau32, 
  # h_tau21_msd,
  # h_tau31_msd,
  # h_tau32_msd,    
  h_pt_deepAK8,
  h_pt_tau21, 
  h_pt_msd_tau21,
]

timer = ROOT.TStopwatch()
### LOOP OVER MASS ###
for y in p[0]:
  print ""
  print "****************************************"
  print ""
  print "START Processing sample:"
  print "%s%s"%(p[2],y)
  timer.Print()
  timer.Continue()
  print ""
  print"****************************************"
  INDIR   =  "/eos/user/s/ssyedoma/AnaJetTagging/Ntuples/Ntuple_"
  INDIR   += p[2]
  INDIR   += y

  ### GET LIST OF FILES ###
  inFileList = [EOSUSER+f for f in glob.glob(INDIR+".root")]
  # print inFileList

  ### SETUP TCHAIN ###
  tree = ROOT.TChain(treeName)
  for inFile in inFileList:
    tree.Add(inFile)

  ### USE TCHAIN AND SETUP TTREEREADER ###
  inTree = InputTree(tree)
  nEvents=inTree.GetEntries()
  nEvents=1000
  ### LOOP OVER EVENTS ###
  print "Total events: ",nEvents
  for i in xrange(0, nEvents):

    if i%10000==0:
      print "Running %d out of %d" %(i,nEvents)
    
    evt       = Event(inTree,i)
    particles = Collection(evt, "GenPart")
    fatjet    = Collection(evt, "FatJet")
    jetak8    = Collection(evt, "GenJetAK8")
    # print "Event: ", i

    QfromW=[]; QfromZ=[]; nW=[]

    for idx, gp in enumerate(particles):
      if not hasattr(gp, 'dauIdx'):
         gp.dauIdx = []
      if gp.genPartIdxMother >= 0:
        mom = particles[gp.genPartIdxMother]
        if not hasattr(mom, 'dauIdx'):
            mom.dauIdx = [idx]
        else:
            mom.dauIdx.append(idx)

    def getFinal(gp):
            for idx in gp.dauIdx:
                dau = particles[idx]
                if dau.pdgId == gp.pdgId:
                    return getFinal(dau)
            return gp

    nW=[x for x in particles if (abs(x.pdgId)==24 and abs(x.eta)<2.4)]
    QfromZ=[x for x in particles if (x.genPartIdxMother>=0 and abs(x.pdgId)<6 and abs(particles[x.genPartIdxMother].pdgId) == 23 and abs(x.eta)<2.4 and abs(particles[x.genPartIdxMother].eta)<2.4)]
      
    if len(nW)<1:
      continue
    
    Wfinal=None
    for wb in nW:
      Wfinal=getFinal(wb)
    
    QfromW=[x for x in particles if (x.genPartIdxMother>=0 and abs(x.pdgId)<6 and x.genPartIdxMother == Wfinal._index and abs(x.eta)<2.4)]
    
    nW=[]
    nW.append(Wfinal)

    for wb in nW:
      h_W_den.Fill(wb.pt)
      h_q_den.Fill(wb.pt)

    wbinfj=[]
    qinfj=[]
    for fj in fatjet:
      if fj.pt>200. and abs(fj.eta)<2.4:          
        wbinfj=[(x,x.pt) for x in nW if (len(nW)>0 and x.DeltaR(fj)<0.8)]
        wbinfj.sort(key = lambda x: x[1])
    
        if len(wbinfj)>0:
          W0=wbinfj[-1][0]
          h_W_eff.Fill(W0.pt)
        
        qinfj=[(x,x.pt) for x in QfromW if (len(QfromW)>=2 and x.DeltaR(fj)<0.8)]
        qinfj.sort(key = lambda x: x[1])
        
        if len(qinfj)>=2:
          q0=qinfj[-1][0]
          q1=qinfj[-2][0]
          h_q_eff.Fill(particles[q0.genPartIdxMother].pt)
   
          if q0.DeltaR(fj)<0.8 and q1.DeltaR(fj)<0.8 and particles[q0.genPartIdxMother].DeltaR(fj)<0.8:
            # h_deepAK8.Fill(fj.deepTag_WvsQCD)
            # h_tau21.Fill(fj.tau21)
            # h_tau31.Fill(fj.tau31)
            # h_tau32.Fill(fj.tau32)
              h_pt_deepAK8.Fill(fj.pt, fj.deepTag_WvsQCD)
              h_pt_tau21.Fill(fj.pt, fj.tau21)
              h_W_msd.Fill(fj.msoftdrop)

          if fj.msoftdrop>65. and fj.msoftdrop<105.:
              # h_tau21_msd.Fill(fj.tau21)
              # h_tau31_msd.Fill(fj.tau31)
              # h_tau32_msd.Fill(fj.tau32)
              h_pt_msd_tau21.Fill(fj.pt, fj.tau21)


Weff = ROOT.TEfficiency(h_W_eff, h_W_den)
qeff = ROOT.TEfficiency(h_q_eff, h_q_den)

color=[ROOT.kRed,ROOT.kBlue,ROOT.kGreen]
lgd = [ROOT.kFullSquare, ROOT.kFullCircle, ROOT.kFullTriangleUp, ROOT.kFullTriangleDown, ROOT.kOpenCircle, ROOT.kOpenSquare ]

### ROOT FILE ####
##################################
# filename="_deepAK8_tau_msd"
# outFile = ROOT.TFile("%s%s%s.root" %(outDir, p[2], filename),"RECREATE")

# i=0
# for a in histoList:
#   a.SetLineColor(ROOT.kRed)
#   a.SetLineWidth(2)
#   # a.SetMarkerColor(color[0])
#   a.SetStats(0)
#   # a.SetMarkerStyle(lgd[1])
#   a.SetOption("COLZ")
#   a.Write()
#   i+=1
# outFile.Close()

###################################
# filename="_tagger_pt"
# outFile = ROOT.TFile("%s%s%s.root" %(outDir, p[2], filename), "RECREATE")

# for a in histoList:
#   a.SetStats(0)
#   a.SetOption("COLZ")
#   a.Write()

# outFile.Close()

### PDF FILE ###
####################################
# pdfname=["_pt_deepAK8", "_pt_tau21", "_pt_msd_tau21"]
# # histopdflist=[h_deepAK8_pt, h_tau21_pt]

# c=ROOT.TCanvas("","",877,620)
# for i, a in enumerate(histoList):
#   a.SetStats(0)
#   a.SetOption("COLZ")
#   a.Draw()
#   c.Print("%s%s%s.pdf" %(outDir, p[2], pdfname[i]))

#####################################
# pdfname="_eff_pt"
pdfname="_W_msd"

legname=["W boson"]
# legname=["#bf{#DeltaR(AK8,W)<0.8}", "#bf{max#DeltaR(AK8,q)<0.8}"]

## SETUP LEGENDARY ##
legpos = "Right"
if legpos == "Left":
  xLat = 0.2
elif legpos == "Right":
  xLat = 0.7 # move left and right
else:
  xLat = 0.2
  
yLat = 0.85 # move legend up and down, the larger( about 1 already at the edge of canvas) the higher it goes
xLeg = xLat
yLeg = yLat

leg_g =  0.03 * len(legname) #number of legend entries
leg = ROOT.TLegend( xLeg+0.2, yLeg - leg_g, xLeg-0.1, yLeg )
leg.SetNColumns(1)
leg.SetFillStyle(0)
leg.SetTextFont(43)
leg.SetTextSize(17)
leg.SetBorderSize(0)

## CANVAS ##

i=0
c = ROOT.TCanvas("","",877, 620)
# for a in [Weff, qeff]:
for a in [h_W_msd]:

  a.SetStats(0)
  # a.SetStatisticOption(0)
  a.SetLineWidth(1)
  a.SetLineColor(color[i])
  a.SetLineColor(color[i])
  a.SetMarkerColor(color[i])
  a.SetMarkerStyle(lgd[i])

  if i==0:
    a.DrawNormalized()
    leg.AddEntry(a,legname[i],"p")
  else:
    a.Draw("SAME")
    leg.AddEntry(a, legname[i], "p")
  i+=1

  # c.Update() 
  # graph = a.GetPaintedGraph()
  # graph.GetXaxis().SetLimits(100, 600)
  # graph.SetMinimum(0)
  # graph.SetMaximum(1.4)
  # c.Update()

leg.Draw()
c.SetTicks(1,1)
c.Print("%s%s%s.pdf" %(outDir, p[1], pdfname))

#####################################
timer.Stop()
timer.Print()