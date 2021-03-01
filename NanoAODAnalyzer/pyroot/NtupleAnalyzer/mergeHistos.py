import glob, ROOT, os

version = 'ULv2'
inDir = '/eos/user/s/ssyedoma/AnaJetTagging/Histos/%s/'%version
outDir = '/eos/user/s/ssyedoma/AnaJetTagging/MergedHistos/%s/'%version
if not os.path.exists(outDir): os.makedirs(outDir)

# sample = 'QCDPt15To7000'
sample = 'BulkGravWW'

fileList = glob.glob(inDir+'Histo_%s*_tag_pt.root'%sample)
# fileList = glob.glob(inDir+'Histo_%s*_tag_pt_2.root'%sample)

totHisto = {}
histoName = ['h_pt_deepak8', 'h_pt_deepak8md', 'h_pt_sdtau21']
files = map(ROOT.TFile.Open, fileList)
names = map(lambda f: f.split('/')[-1].split('_tag_pt')[0].replace('Histo_',''), fileList)

for hN in histoName:
	histos = map(lambda f,n,:f.Get(hN).Clone(hN+n), files, names)
	for i,h in enumerate(histos):
		if i==0: totHisto[hN] = h
		else 	 : totHisto[hN].Add(h)

outFile = ROOT.TFile(outDir+'MergedHisto_%s_tag_pt.root'%sample, 'RECREATE')
# outFile = ROOT.TFile(outDir+'MergedHisto_%s_tag_pt_2.root'%sample, 'RECREATE')
for histo in totHisto: totHisto[histo].Write(histo.replace('W',''))
outFile.Close()
