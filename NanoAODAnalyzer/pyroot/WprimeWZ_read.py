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

# a = input("Choose 0.QCD 1.Wtag 2.Ztag 3.Toptag : ")
a=1

nQCD  = range(0,75)
# massW = ["800"]
massW = ["600","800","1000","1200","1400","1600","2000","2500","3000","3500","4000","4500","5000","5500","6000","6500","7000","7500","8000"]
# massZ = ["2000"]
massZ = ["800","1000","1200","1400","1600","1800","2000","3000","4000"]
massT = ["500","750","1000","1250","1500","2000","2500","3000","3500","4000","5000","6000","7000","8000"]
sample = [(nQCD,"QCD","QCDPt15To7000_"),(massW,"WprimeWZ","WprimeWZM"),(massZ,"GToZZ","GToZZM"),(massT,"ZprimeToTT","ZprimeToTTM")]
p = sample[a]

QQfromZ=[]
QQfromZ_AK8=[]
QQfromW=[]
QQfromW_AK8=[]

### DEFINE HISTOGRAMS ###
bins = 10000
h_WToQQ_pt   = ROOT.TH1F("h_WToQQ_pt", "W to QQ (pt);pt;No.of events", bins, 0., 1000.)
h_WToQQ_dr   = ROOT.TH1F("h_WToQQ_dr", "W to QQ (dR);dR;No.of events", bins, 0., .8)
h_ZToQQ_pt   = ROOT.TH1F("h_ZToQQ_pt", "Z to QQ (pt);pt;No.of events", bins, 0., 1000.)
h_ZToQQ_dr   = ROOT.TH1F("h_ZToQQ_dr", "Z to QQ (dR);dR;No.of events", bins, 0., .8)
h_deepAK8 	 = ROOT.TH1F("h_deepAK8", "W'->WZ DeepAK8; DeepAK8; No.of events", bins, 0., 1.)
h_tau21 		 = ROOT.TH1F("h_tau21","W'->WZ #tau21; #tau21; No. of events", bins, 0., 1.)
h_tau31 		 = ROOT.TH1F("h_tau31","W'->WZ #tau31; #tau31; No. of events", bins, 0., 1.)
h_tau32 		 = ROOT.TH1F("h_tau32","W'->WZ #tau32; #tau32; No. of events", bins, 0., 1.)

histoList = [
	# h_WToQQ_pt,
	# h_WToQQ_dr,
	# h_ZToQQ_pt,
	# h_ZToQQ_dr,
	h_deepAK8,
	h_tau21,
	h_tau31,
	h_tau32, 		
]

timer = ROOT.TStopwatch()
### LOOP OVER MASS ###
for y in p[0]:
	print ""
	print "****************************************"
	print ""
	print "START Processing sample:"
	print "%s%s"%(p[2],y)
	print ""
	print"****************************************"
	INDIR		=	 "/eos/user/s/ssyedoma/AnaJetTagging/Ntuples/Ntuple_"
	INDIR		+= p[2]
	INDIR		+= y

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
	
	### LOOP OVER EVENTS ###
	print "Total events: ",nEvents
	for i in xrange(0,nEvents):

		if i%10000==0:
			print "Running %d out of %d" %(i,nEvents)
		
		evt 			= Event(inTree,i)
		particles	=	Collection(evt, "GenPart")
		fatjet 		= Collection(evt, "FatJet")
		jetak8		=	Collection(evt,	"GenJetAK8")
		# print "Event: ", i

		QfromW=[]
		QfromZ=[]

		for part in particles:
			mother=particles[part.genPartIdxMother]
			if part.genPartIdxMother>=0:
				if abs(part.pdgId)<6 and abs(mother.pdgId) == 24:
					QfromW.append(part)
			
				if abs(part.pdgId)<6 and abs(mother.pdgId) == 23:
					QfromZ.append(part)
			
		if len(QfromW) == 2:
			# print "There's two quarks from W!"
			q0 = QfromW[0]
			q1 = QfromW[1]
			QQfromW.append((q0,q1))
			mother=particles[(q0.genPartIdxMother)]

			for fj in fatjet:
				if fj.pt>200 and fj.eta<2.4:
					if q0.DeltaR(fj)<0.8 and q1.DeltaR(fj)<0.8 and mother.DeltaR(fj)<0.8:
						QQfromW_AK8.append(QQfromW)
						h_deepAK8.Fill(fj.deepTag_WvsQCD)
						h_tau21.Fill(fj.tau21)
						h_tau31.Fill(fj.tau31)
						h_tau32.Fill(fj.tau32)
 	
 						# h_WToQQ_pt.Fill(mother.pt)
						# h_WToQQ_dr.Fill(q0.DeltaR(fj))
						# h_WToQQ_dr.Fill(q1.DeltaR(fj))
						# h_WToQQ_dr.Fill(mother.DeltaR(fj))


		# if len(QfromZ) == 2:
		# 	# print "There's two quarks from Z!"
		# 	q0 = QfromZ[0]
		# 	q1 = QfromZ[1]
		# 	QQfromZ.append((q0,q1))
		# 	mother=particles[(q0.genPartIdxMother)]

		# 	for fj in fatjet:
		# 		if fj.pt>200 and fj.eta<2.4:
		# 			if q0.DeltaR(fj)<0.8 and q1.DeltaR(fj)<0.8 and mother.DeltaR(fj)<0.8:
		# 				QQfromZ_AK8.append(QQfromZ)
		# 				h_ZToQQ_pt.Fill(mother.pt)
		# 				h_ZToQQ_dr.Fill(q0.DeltaR(fj))
		# 				h_ZToQQ_dr.Fill(q1.DeltaR(fj))
		# 				h_ZToQQ_dr.Fill(mother.DeltaR(fj))
		
	# print "qq from %s: %d | qq from Z: %d" %(p[1], len(QQfromW), len(QQfromZ))
	# print "qq from %s AK8: %d | qq from Z AK8: %d" %(p[1], len(QQfromW_AK8), len(QQfromZ_AK8))
	# print "0 fatjets: %d | 1 fatjets: %d | 2 fatjets: %d | 3 fatjets: %d | 4 fatjets: %d | fatjets: %d" %(len(FJ0), len(FJ1), len(FJ2) , len(FJ3), len(FJ4), len(FJ5))

### ROOT FILE ###
filename="_all_tagged"
pdfname="deepAK8"
color=[ROOT.kRed,ROOT.kBlue,ROOT.kGreen]
lgd = [ROOT.kFullSquare, ROOT.kFullCircle, ROOT.kFullTriangleUp, ROOT.kFullTriangleDown, ROOT.kOpenCircle, ROOT.kOpenSquare ]
outFile = ROOT.TFile("%s%s.root" %(p[2], filename),"RECREATE")

i=0
for a in histoList:
	a.SetLineColor(ROOT.kRed)
	a.SetLineWidth(2)
	a.SetMarkerColor(ROOT.kRed)
	a.Write()
	i+=1

# c = ROOT.TCanvas("","",877, 620)
# for a in [h_deepAK8,h_deepAK8QCD]:
# 	a.SetLineColor(color[i])
# 	a.Set(2)
# 	a.SetMarkerColor(color[i])
# 	if i==0:
# 		a.Draw("l")
# 	else:
# 		a.Draw("l SAME")
# 	i+=1
# c.Print(pdfname+".pdf")

outFile.Close()

# os.system("mv "+pdfname+".pdf /eos/user/s/ssyedoma/AnaJetTagging/ANALYSIS/")
os.system('mv %s%s.root /eos/user/s/ssyedoma/AnaJetTagging/ANALYSIS/' %(p[2], filename))

timer.Stop()
timer.Print()