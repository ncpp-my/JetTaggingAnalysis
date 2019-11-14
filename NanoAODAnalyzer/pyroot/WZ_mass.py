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

massZ = ["800","1400","1800","2000","3000","4000"]
massW = ["600","800","1000","1200","1400","1600","2000","2500","3000","3500","4000","4500","5000","5500","6000","6500","7000","7500","8000"]

nQCD  = range(0,75)

sample = [(massW,"WprimeWZ","WprimeWZM"), (massZ,"GToZZ","GToZZM"), (nQCD,"QCD","QCDPt15To7000")]

### DEFINE HISTOGRAMS ###
bins=100
h_W_msd        = ROOT.TH1F("h_W_msd", "; m_{SD} [GeV]; A.U.", bins, 0., 200.)
h_Z_msd        = ROOT.TH1F("h_Z_msd", "; m_{SD} [GeV]; A.U.", bins, 0., 200.)
h_QCD_msd      = ROOT.TH1F("h_QCD_msd", "; m_{SD} [GeV]; A.U.", bins, 0., 200.)

timer = ROOT.TStopwatch()
### LOOP OVER MASS ###
for ip,p in enumerate(sample):
  for y in p[0]:
    print ""
    print "****************************************"
    print ""
    print "START Processing sample:"
    if ip==0 or ip==1:
      print "%s%s"%(p[2],y)
    elif ip==2:
      print "%s_%s"%(p[2],y)
    timer.Print()
    timer.Continue()
    print ""
    print"****************************************"
    INDIR   =  "/eos/user/s/ssyedoma/AnaJetTagging/Ntuples/Ntuple_"
    INDIR   += p[2]
    if ip==0 or ip==1:
      INDIR += y
    elif ip==2:
      INDIR   += "_%s" %(y)

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
    # nEvents=100
    ### LOOP OVER EVENTS ###
    print "Total events: ",nEvents
    for i in xrange(0, nEvents):

      if i%10000==0:
        print "Running %d out of %d" %(i,nEvents)
      
      evt       = Event(inTree,i)
      particles = Collection(evt, "GenPart")
      fatjet    = Collection(evt, "FatJet")
      jetak8    = Collection(evt, "GenJetAK8")

      fjInak8=[x for x in fatjet if (x.pt>500. and x.pt<1000. and abs(x.eta)<2.4)]
      
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

      if ip==0:
        nW=[x for x in particles if (abs(x.pdgId)==24 and abs(x.eta)<2.4)]

        if len(nW)<1: continue
        Wfinal=[]
        for wb in nW:
          Wfinal.append(getFinal(wb))
        for j in Wfinal:
         QfromW=[x for x in particles if (x.genPartIdxMother>=0 and abs(x.pdgId)<6 and x.genPartIdxMother == j._index and abs(x.eta)<2.4)]
        wbinfj=[]
        qinfj=[]
        for fj in fatjet:
          if fj.pt>200. and abs(fj.eta)<2.4:          
            wbinfj=[(x,x.pt) for x in Wfinal if (len(Wfinal)>0 and x.DeltaR(fj)<0.8)]
            wbinfj.sort(key = lambda x: x[1])
        
            if len(wbinfj)>0:
              W0=wbinfj[-1][0]
           
            qinfj=[(x,x.pt) for x in QfromW if (len(QfromW)>=2 and x.DeltaR(fj)<0.8)]
            qinfj.sort(key = lambda x: x[1])
            
            if len(qinfj)>=2:
              q0=qinfj[-1][0]
              q1=qinfj[-2][0]
       
              if q0.DeltaR(fj)<0.8 and q1.DeltaR(fj)<0.8 and particles[q0.genPartIdxMother].DeltaR(fj)<0.8:
                h_W_msd.Fill(fj.msoftdrop)

      elif ip==1:
        nZ=[x for x in particles if abs(x.pdgId)==23 and abs(x.eta)<2.4]

        if len(nZ)<1: continue
        Zfinal=[]
        for Z in nZ:
          Zfinal.append(getFinal(Z))
        for j in Zfinal:
          QfromZ=[x for x in particles if (x.genPartIdxMother>=0 and abs(x.pdgId)<6 and x.genPartIdxMother == j._index and abs(x.eta)<2.4)]
        zbinfj=[]; qinfj=[]
        for fj in fjInak8:
          if fj.pt>200. and abs(fj.eta)<2.4:          
            zbinfj=[(x,x.pt) for x in Zfinal if (len(Zfinal)>0 and x.DeltaR(fj)<0.8)]
            zbinfj.sort(key = lambda x: x[1])
        
            if len(zbinfj)>0:
              Z0=zbinfj[-1][0]
           
            qinfj=[(x,x.pt) for x in QfromZ if (len(QfromZ)>=2 and x.DeltaR(fj)<0.8)]
            qinfj.sort(key = lambda x: x[1])
            
            if len(qinfj)>=2:
              q0=qinfj[-1][0]
              q1=qinfj[-2][0]
       
              if q0.DeltaR(fj)<0.8 and q1.DeltaR(fj)<0.8 and particles[q0.genPartIdxMother].DeltaR(fj)<0.8:
                h_Z_msd.Fill(fj.msoftdrop)

      elif ip==2:
        for fj in fjInak8:
          h_QCD_msd.Fill(fj.msoftdrop)

color = [46,42,30,36,38]
lgd = [ROOT.kFullSquare, ROOT.kFullCircle, ROOT.kFullTriangleUp, ROOT.kFullTriangleDown, ROOT.kOpenCircle, ROOT.kOpenSquare ]

#####################################
pdfname="WZ_QCD_msd1"
legname=["QCD multijet", "W boson", "Z boson"]

## SETUP LEGENDARY ##
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

leg_g =  0.04 * len(legname) # num of legend entries
leg = ROOT.TLegend( xLeg+0.05, yLeg - leg_g, xLeg+0.15, yLeg )
leg.SetNColumns(1)
leg.SetFillStyle(0)
leg.SetTextFont(43)
leg.SetTextSize(14)
leg.SetBorderSize(0)

## CANVAS ##
i=0
c = ROOT.TCanvas("","",877, 620)
for a in [h_QCD_msd, h_W_msd, h_Z_msd]:

  a.SetStats(0)
  # a.SetStatisticOption(0)
  a.SetLineWidth(2)
  a.SetLineColor(color[i])
  a.SetLineColor(color[i])
  a.SetMarkerColor(color[i])
  a.SetMarkerStyle(lgd[i])
  a.SetMaximum(a.GetMaximum()+a.GetMaximum()/4)

  if i==0:
    a.DrawNormalized()
    leg.AddEntry(a,legname[i],"l")
  else:
    a.DrawNormalized("SAME")
    leg.AddEntry(a, legname[i], "l")
  i+=1

leg.Draw()
c.SetTicks(1,1)
c.Print("%s%s.pdf" %(outDir, pdfname))

#####################################
timer.Stop()
timer.Print()