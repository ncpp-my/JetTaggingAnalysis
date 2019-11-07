import sys
import os
import glob
import ROOT
import plotter

from collections import OrderedDict 
from array import array

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import InputTree

ROOT.gROOT.SetBatch()

EOSUSER   ="root://eosuser.cern.ch/"
treeName  ="TreeFatJet"
outDir = "/eos/user/s/ssyedoma/AnaJetTagging/ANALYSIS/tagger_pt/"
outDir2 = "/eos/user/s/ssyedoma/AnaJetTagging/ANALYSIS/eff/"
massT = ["500","750","1000","1250","1500","2000","2500","3000","3500","4000","5000","6000","7000","8000"]
p = [massT,"ZprimeToTT","ZprimeToTTM"]

### DEFINE HISTOGRAMS ###
bins = 10000
### taggers ###
h_deepAK8     = ROOT.TH1F("h_deepAK8", "Top-tagging DeepAK8; DeepAK8; No.of events", bins, 0., 1.)
h_tau32       = ROOT.TH1F("h_tau32","Top-tagging #Tau32; #tau32; No. of events", bins, 0., 1.)
h_tau32_msd   = ROOT.TH1F("h_tau32_msd","Top-tagging; msd + #tau32; No. of events", bins, 0., 1.)
### taggers vs pt ###
h_pt_deepAK8   = ROOT.TH2F("h_pt_deepAK8", "Top-tagging DeepAK8 vs p_{T}; p_{T}; DeepAK8", 50, 0., 5000., 2000, 0., 1.)
h_pt_tau32     = ROOT.TH2F("h_pt_tau32", "Top-tagging #tau_{32} vs p_{T}; p_{T}; #tau_{32}", 50, 0., 5000., 2000, 0., 1.)
h_pt_msd_tau32 = ROOT.TH2F("h_pt_msd_tau32", "Top-tagging m_{SD}+#tau_{32} vs p_{T}; p_{T}; m_{SD} + #tau_{32}", 50, 0., 5000., 2000, 0., 1.)
### eta vs pt ###
h_top_eta_pt = ROOT.TH2F("h_top_eta_pt", "top quark #eta vs p_{T}; p_{T}; #eta", 50, 0., 5000., 50, -4, 4)
### matching efficiency ###
h_T_eff = ROOT.TH1F("h_T_eff", ";t quark p_{T} [GeV]; Efficiency", 18, 100., 1000.)
h_q_eff = ROOT.TH1F("h_d_eff","", 18, 100., 1000.)
h_T_den = ROOT.TH1F("h_T_den",";t quark p_{T} [GeV]; Efficiency", 18, 100., 1000.)

histoList=[
  # h_deepAK8,
  # h_tau32,
  # h_tau32_msd,
  h_pt_deepAK8,
  h_pt_tau32,
  h_pt_msd_tau32,
  # h_top_eta_pt,
]

################################################################
### check if gp is within AK8 jet ###
def inAK8(gp):
  for fj in ak8jet:
    if gp.DeltaR(fj)<0.8:
      return True
  return False

### get final decay of part using dauIdx ###
def getFinal(gp):
        for idx in gp.dauIdx:
            dau = particles[idx]
            if dau.pdgId == gp.pdgId:
                return getFinal(dau)
        return gp

### check if gp -> W -> qq in AK8 ###
def decayToW(gp):
        if len(gp.dauIdx) == 0:
            raise ValueError('Particle has no daughters!')
        for idx in gp.dauIdx:
          dp=particles[idx]
          dpart=getFinal(dp)
          if abs(dpart.pdgId) == 24 and inAK8(dpart) and isHadronic2(dpart):
            return True
        return False

### check if gp -> b in AK8 ###
def decayToB(gp):
  if len(gp.dauIdx) == 0:
      raise ValueError('Particle has no daughters!')
  for idx in gp.dauIdx:
    dpart=particles[idx]
    if abs(dpart.pdgId) == 5 and inAK8(dpart):
      return True
  return False

### check if gp decays to at least 2 quarks in AK8 ###
def isHadronic2(gp):
        if len(gp.dauIdx) == 0:
            raise ValueError('Particle has no daughters!')
        for idx in gp.dauIdx:
          dpart=particles[idx]
          if abs(dpart.pdgId) < 6 and inAK8(dpart):            
            gp.dauIdx.reverse()
            for idx in gp.dauIdx:
              dpart=particles[idx]
              if abs(dpart.pdgId)<6 and inAK8(dpart):
                return True
        return False

### check if decay products are within AK8 jets ###
def decayAK8(gp):
        if len(gp.dauIdx) == 0:
            raise ValueError('Particle has no daughters!')
        for fj in fatjet:
          if abs(fj.eta)<2.4 and fj.pt>200.:
            for idx in gp.dauIdx:
              if particles[idx].DeltaR(fj) < 0.8:
                  return True
        return False

### make sure no same part in the list ###
def checkList(gp, gpfinal):
  for p in gpfinal:
    if getFinal(gp)._index==p._index:
      return False          
  return True

################################################################

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
  INDIR2 = INDIR
  INDIR2 += "_ext1"

  ### GET LIST OF FILES ###
  inFileList = [EOSUSER+f for f in glob.glob(INDIR+".root")]
  inFileList2 = [EOSUSER+f for f in glob.glob(INDIR2+".root")]
  # print inFileList

  ### SETUP TCHAIN ###
  tree = ROOT.TChain(treeName)
  for inFile in inFileList:
    tree.Add(inFile)
  for inFile in inFileList2:
    tree.Add(inFile)

  ### USE TCHAIN AND SETUP TTREEREADER ###
  inTree = InputTree(tree)
  nEvents=inTree.GetEntries()
  # nEvents=100

  ### LOOP OVER EVENTS ###
  print "Total events: ",nEvents
  for i in xrange(0,nEvents):

    if i%10000==0:
      print "Running %d out of %d" %(i, nEvents)
    
    evt       = Event(inTree,i)
    particles = Collection(evt, "GenPart")
    fatjet    = Collection(evt, "FatJet")
    jetak8    = Collection(evt, "GenJetAK8")
    # print "Event: ", i
   
    #################################
    ### efficiency wrt t quark pt ### 
    #################################
    nT=[]; WfromT=[]; QfromWfromT=[]
  
    ### define dauIdx for each part ###
    for idx, gp in enumerate(particles):
      if not hasattr(gp, 'dauIdx'): 
        gp.dauIdx = []
      if gp.genPartIdxMother >= 0:  
        mom = particles[gp.genPartIdxMother]
        if not hasattr(mom, 'dauIdx'): mom.dauIdx = [idx]
        else: mom.dauIdx.append(idx)
    
    ak8jet=[x for x in fatjet if (x.pt>200. and abs(x.eta)<2.4)]
    nT=[x for x in particles if (abs(x.eta)<2.4 and abs(x.pdgId)==6)]

    if len(nT)<1: continue
    Tfinal=[]
    for t in nT:
      if checkList(t,Tfinal): Tfinal.append(getFinal(t))
    
    if len(Tfinal)>0:
      for t in Tfinal:
        h_T_den.Fill(t.pt)

        if inAK8(t): 
          h_T_eff.Fill(t.pt)

        if decayToW(t) and decayToB(t): 
          h_q_eff.Fill(t.pt)
          
          if inAK8(t):
            for fj in ak8jet:
              h_pt_deepAK8.Fill(fj.pt, fj.deepTag_TvsQCD)
              h_pt_tau32.Fill(fj.pt, fj.tau32)

              if fj.msoftdrop>105. and fj.msoftdrop<210.:
                h_pt_msd_tau32.Fill(fj.pt, fj.tau32)

Teff = ROOT.TEfficiency(h_T_eff, h_T_den)
qeff = ROOT.TEfficiency(h_q_eff, h_T_den)

color=[ROOT.kRed,ROOT.kBlue,ROOT.kGreen]
lgd = [ROOT.kFullSquare, ROOT.kFullCircle, ROOT.kFullTriangleUp, ROOT.kFullTriangleDown, ROOT.kOpenCircle, ROOT.kOpenSquare ]

################################
### ROOT FILE ###
################################
filename=p[2]
filename+="_tagger_pt_test"
outFile = ROOT.TFile("%s%s.root" %(outDir, filename), "RECREATE")

for a in histoList:
  a.SetStats(0)
  a.SetOption("COLZ")
  a.Write()

outFile.Close()

################################
### PDF FILE ###
################################
pdfname=p[1]
pdfname+="_eff_pt_test"

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

leg_g =  0.03 * 2 #number of legend entries
leg = ROOT.TLegend( xLeg+0.2, yLeg - leg_g, xLeg-0.1, yLeg )
leg.SetNColumns(1)
leg.SetFillStyle(0)
leg.SetTextFont(43)
leg.SetTextSize(17)
leg.SetBorderSize(0)

## CANVAS ##

legname=["#bf{#DeltaR(AK8,t)<0.8}", "#bf{max#DeltaR(AK8,q)<0.8}"]
i=0
c = ROOT.TCanvas("","",877, 620)
for a in [Teff, qeff]:
  a.SetLineWidth(1)
  a.SetLineColor(color[i])
  a.SetStatisticOption(0)
  # a.SetConfidenceLevel(0.68)
  a.SetLineColor(color[i])
  a.SetMarkerColor(color[i])
  a.SetMarkerStyle(lgd[i])

  if i==0:
    a.Draw()
    leg.AddEntry(a,legname[i],"p")
  else:
    a.Draw("SAME")
    leg.AddEntry(a, legname[i], "p")
  i+=1

  c.Update() 
  graph = a.GetPaintedGraph()
  graph.GetXaxis().SetLimits(100, 1000)
  graph.SetMinimum(0)
  graph.SetMaximum(1.4) 
  c.Update()

leg.Draw()
c.SetTicks(1,1)
c.Print("%s%s.pdf" %(outDir2, pdfname))

################################
timer.Stop()
timer.Print()

