import ROOT


ROOT.gROOT.SetBatch()

fData =   ROOT.TFile("pileup_2016_data.root")
fMC   =   ROOT.TFile("pileup_2016_mc.root")



hData = fData.Get("pileup")
hMC   = fMC.Get("pileup")



c  = ROOT.TCanvas("","",)
hData.Scale(1.0/hData.Integral(0,1000))
hMC.Scale(1.0/hMC.Integral(0,1000))

hData.SetLineColor(1)
hMC.SetLineColor(2)

# hData.Draw("HIST")
# hMC.Draw("HISTSAME")

hRatio = hMC.Clone("Ratio")
hRatio.Divide(hData)

for i in xrange(0, hRatio.GetNbinsX() + 1):
  print i, "|" ,hRatio.GetBinContent(i)
hRatio.Draw("HIST");


c.Print("RATIO.pdf")
