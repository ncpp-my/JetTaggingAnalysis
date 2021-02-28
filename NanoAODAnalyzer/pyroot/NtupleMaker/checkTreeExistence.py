import glob, ROOT

files = glob.glob('/eos/user/s/ssyedoma/AnaJetTagging/Ntuples/Ntuple_WprimeWZ*.root')
nlist = []
for f in files:
	if any('M%s.'%n in f for n in nlist): continue
	file = ROOT.TFile.Open(f)
	w = file.Get('TreeFatJet')

	print w.GetEntries(), f.split('/')[-1]