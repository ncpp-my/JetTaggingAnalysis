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
h_T_eff = ROOT.TH1F("h_T_eff", ";t quark p_{T} [GeV]; Efficiency", 20, 0., 2000.)
h_q_eff = ROOT.TH1F("h_d_eff","", 20, 0., 2000.)
h_T_den = ROOT.TH1F("h_T_den",";t quark p_{T} [GeV]; Efficiency", 20, 0., 2000.)
### no. of full hadronic/semi leptonic/full leptonic Ws ###
h_fhad_pt = ROOT.TH1F("h_fhad_pt","Z'#rightarrowt#bar{t};W boson p_{T} [GeV]; No. of events", 20, 0., 2000.)
h_slep_pt = ROOT.TH1F("h_slep_pt",";W boson p_{T} [GeV]; No. of events", 20, 0., 2000.)
h_flep_pt = ROOT.TH1F("h_flep_pt",";W boson p_{T} [GeV]; No. of events", 20, 0., 2000.)

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
    if gp.DeltaR(fj)<0.6:
      return True
  return False

### get final decay of part using dauIdx ###
def getFinal(gp):
        for idx in gp.dauIdx:
            dau = particles[idx]
            if dau.pdgId == gp.pdgId:
                return getFinal(dau)
        return gp

def decayToW(gp):
        if len(gp.dauIdx) == 0:
            raise ValueError('Particle has no daughters!')
        for idx in gp.dauIdx:
          dp=particles[idx]
          dpart=getFinal(dp)
          if abs(dpart.pdgId) == 24 and decayTo2Q(dpart):
            return True
        return False

def decayToB(gp):
  if len(gp.dauIdx) == 0:
      raise ValueError('Particle has no daughters!')
  for idx in gp.dauIdx:
    dpart=particles[idx]
    if abs(dpart.pdgId) == 5:
      return True
  return False

def decayTo2Q(gp):
        if len(gp.dauIdx) == 0:
            raise ValueError('Particle has no daughters!')
        for idx in gp.dauIdx:
          dpart=particles[idx]
          if abs(dpart.pdgId) < 6:            
            gp.dauIdx.reverse()
            for idx in gp.dauIdx:
              dpart=particles[idx]
              if abs(dpart.pdgId)<6:
                return True
        return False

### check if gp -> W -> qq in AK8 ###
def decayToWAK8(gp):
        if len(gp.dauIdx) == 0:
            raise ValueError('Particle has no daughters!')
        for idx in gp.dauIdx:
          dp=particles[idx]
          dpart=getFinal(dp)
          if abs(dpart.pdgId) == 24 and inAK8(dpart) and decayTo2QAK8(dpart):
            return True
        return False

### check if gp -> b in AK8 ###
def decayToBAK8(gp):
  if len(gp.dauIdx) == 0:
      raise ValueError('Particle has no daughters!')
  for idx in gp.dauIdx:
    dpart=particles[idx]
    if abs(dpart.pdgId) == 5 and inAK8(dpart):
      return True
  return False

### check if gp decays to at least 2 quarks in AK8 ###
def decayTo2QAK8(gp):
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

### make sure no same part in the list ###
def checkList(gp, gpfinal):
  for p in gpfinal:
    if getFinal(gp)._index==p._index:
      return False          
  return True

def isHadronic(gp):
  dautemp=[x for x in gp.dauIdx if abs(particles[x].pdgId)<6 and abs(particles[x].eta)<2.4]
  if len(dautemp)==2: #fullhadron
    return 0
  elif len(dautemp)==1: #semilept
    return 1
  elif len(dautemp)==0: #fulllept
    return 2
def BeginLeg(ll):
    ## LEGEND POSITION ##
    legpos = "Right"
    if legpos == "Left":
      xLat = 0.13
    elif legpos == "Right":
      xLat = 0.65 # move left and right
    else:
      xLat = 0.2
    yLat = 0.85 # move legend up and down, the larger( about 1 already at the edge of canvas) the higher it goes
    xLeg = xLat
    yLeg = yLat

    leg_g =  0.04 * ll # num of legend entries
    leg = ROOT.TLegend( xLeg+0.05, yLeg - leg_g, xLeg+0.15, yLeg )
    leg.SetNColumns(1)
    leg.SetFillStyle(0)
    leg.SetTextFont(43)
    leg.SetTextSize(14)
    leg.SetBorderSize(0)
    return leg

################################################################

timer = ROOT.TStopwatch()
### LOOP OVER MASS ###

fhad=0; semilep=0; flep=0

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
      if checkList(t,Tfinal) and decayToW(t) and decayToB(t): Tfinal.append(getFinal(t))

    if len(Tfinal)<1: continue
    
    for t in Tfinal:
      h_T_den.Fill(t.pt)

    for t in Tfinal:
      if inAK8(t):
        h_T_eff.Fill(t.pt)
   
      if decayToWAK8(t) and decayToBAK8(t): 
        h_q_eff.Fill(t.pt)

        if inAK8(t):
          for fj in ak8jet:
            h_pt_deepAK8.Fill(fj.pt, fj.deepTag_TvsQCD)
            h_pt_tau32.Fill(fj.pt, fj.tau32)

            if fj.msoftdrop>105. and fj.msoftdrop<210.:
              h_pt_msd_tau32.Fill(fj.pt, fj.tau32)
    #####################################
    ##### NO. OF B, W, AND W->QQ ########
    #####     FROM T             ########
    #####################################
    # Tfinal=[]
    # nT=[x for x in particles if abs(x.pdgId)==6 and abs(x.eta)<2.4]
    # nT=[getFinal(x) for x in nT if len(nT)>0]
    
    # for n in nT:
    #   if checkList(n, Tfinal):
    #     Tfinal.append(getFinal(n))
    #   for T in Tfinal:
    #     Wfinal=[]; bfinal=[]

    #     btemp=[particles[x] for x in T.dauIdx if abs(particles[x].pdgId)==5 and abs(particles[x].eta)<2.4]
    #     if len(btemp)>0:
    #       bfinal.append(btemp[0])

    #     Wtemp=[getFinal(particles[x]) for x in T.dauIdx if abs(particles[x].pdgId)==24 and abs(particles[x].eta)<2.4]
    #     if len(Wtemp)>0:
    #       Wfinal.append(Wtemp[0])

    #     for W in Wfinal:
    #       tempval=isHadronic(W)
    #       if tempval==0:
    #         # print "Full Hadronic"
    #         h_fhad_pt.Fill(W.pt)
    #         fhad+=1
    #       elif tempval==1:
    #         # print "Semi Leptonic"
    #         h_slep_pt.Fill(W.pt)
    #         semilep+=1
    #       elif tempval==2:
    #         # print "Full Leptonic"
    #         h_flep_pt.Fill(W.pt)
    #         flep+=1

    #     qfinaltemp=[]
    #     if len(Wfinal)>0:
    #       for W in Wfinal:
    #         qtemp=[getFinal(particles[x]) for x in W.dauIdx if abs(getFinal(particles[x]).pdgId)<6]
    #         qfinaltemp.append(qtemp)
    #     qfinal=[]
    #     for qlist in qfinaltemp:
    #       for ql in qlist:
    #         qfinal.append(ql)

    #   # print len(bfinal), "|||", len(Wfinal), "|||", len(qfinal)
    #   # print fhad, semilep, flep
    #   # print "===="
    
Teff = ROOT.TEfficiency(h_T_eff, h_T_den)
qeff = ROOT.TEfficiency(h_q_eff, h_T_den)

color = [46,42,30,36,38]
lgd = [ROOT.kFullSquare, ROOT.kFullCircle, ROOT.kFullTriangleUp, ROOT.kFullTriangleDown, ROOT.kOpenCircle, ROOT.kOpenSquare ]

################################
### ROOT FILE ###
################################
# filename=p[2]
# filename+="_tagger_pt_test"
# outFile = ROOT.TFile("%s%s.root" %(outDir, filename), "RECREATE")

# for a in histoList:
#   a.SetStats(0)
#   a.SetOption("COLZ")
#   a.Write()

# outFile.Close()

################################
### PDF FILE ###
################################
pdfname=p[1]
pdfname+="_eff_pt"

## CANVAS ##
# legname=["#bf{Full Hadronic W}", "#bf{Full Leptonic W}", "#bf{Semi Leptonic W}"]
legname=["#bf{#DeltaR(AK8,t)<0.8}", "#bf{max#DeltaR(AK8,q)<0.8}"]
leg=BeginLeg(len(legname))
i=0
c = ROOT.TCanvas("","",877, 620)
# for a in [h_fhad_pt, h_flep_pt, h_slep_pt]:
for a in [Teff, qeff]:
  # a.SetStats(0)
  a.SetStatisticOption(0)
  a.SetLineWidth(1)
  a.SetLineColor(color[i])
  a.SetLineColor(color[i])
  a.SetMarkerColor(color[i])
  a.SetMarkerStyle(lgd[i])
  # a.SetFillColor(color[i])

  if i==0:
    a.Draw()
    leg.AddEntry(a,legname[i],"p")
  else:
    a.Draw("SAME")
    leg.AddEntry(a, legname[i], "p")
  i+=1

  c.Update() 
  graph = a.GetPaintedGraph()
  graph.GetXaxis().SetLimits(0, 2000)
  graph.SetMinimum(0)
  graph.SetMaximum(1.4) 
  c.Update()

leg.Draw()
c.SetTicks(1,1)
c.Print("%s%s.pdf" %(outDir2, pdfname))

################################
timer.Stop()
timer.Print()

