import os, ROOT
from collections import OrderedDict 
import array as array
  
multiPtbin  = 1
multiTagger = 0

# color = [46, 42, 41, 30, 36, 38]
color = [ROOT.kRed+1, ROOT.kGreen+1, ROOT.kOrange+1, ROOT.kBlue+1, 38]
# lines = [1, 3, 5, 7, 9, 11]
lines = [1, 1, 1, 1, 1, 1]
EOSUSER = 'root://eosuser.cern.ch/'
inDir  = '/eos/user/s/ssyedoma/AnaJetTagging/MergedHistos/'
outDir = "/eos/user/s/ssyedoma/AnaJetTagging/Analysis/ROC/"
if not os.path.exists(outDir): os.makedirs(outDir)

outName = [("W_ROC_DeepAK8","W_ROC_tau21"), ("T_ROC_DeepAK8","T_ROC_tau32"), ("Z_ROC_DeepAK8","Z_ROC_tau21")]
signal = "WprimeWZ"

def main():
  
  inFileSig = ROOT.TFile.Open(inDir+'MergedHisto_%s_tag_pt.root' %signal)
  inFileBkg = ROOT.TFile.Open(inDir+'MergedHisto_QCDPt15To7000_tag_pt.root')
  # inFileSig = ROOT.TFile.Open(inDir+'MergedHisto_%s_tag_pt_2.root' %signal)
  # inFileBkg = ROOT.TFile.Open(inDir+'MergedHisto_QCDPt15To7000_tag_pt_2.root')

  part = ["W", "T", "Z"]

  tagList = {
    'WprimeWZ': {
      'deepak8md': 'ROC Curve for W-tagging (DeepAK8-MD)',
      'deepak8'  : 'ROC Curve for W-tagging (DeepAK8)',
      'sdtau21'  : 'ROC Curve for W-tagging (#tau_{21})',
      }
  }

  legList = [
  "300 < p_{T}^{truth} < 500 GeV", 
  "500 < p_{T}^{truth} < 1000 GeV",
  "1000 < p_{T}^{truth} < 1500 GeV",
  "1500 < p_{T}^{truth} < 2000 GeV",
  "2000 < p_{T}^{truth} < 2500 GeV",
  ]
  
  projCut = [(4,5), (6,10), (11,15), (16,20), (21,25)]


  yaxisname = "Background efficiency"
  xaxisname = "Signal efficiency"
  
  h_sig = [None] * len(projCut)
  h_bkg = [None] * len(projCut)

  if multiPtbin:

    for j, tag in enumerate(tagList[signal]):
      
      gr = [None] * len(projCut)
      
      #
      # setup TCanvas
      #
      c = setCanv('','', 800, 800)
      leg = setLeg(len(legList))

      #
      # get 2D histograms
      #
      h2d_sig = inFileSig.Get('h_pt_'+tag).Clone()
      h2d_bkg = inFileBkg.Get('h_pt_'+tag).Clone()
    
      # 1D projections
      for i, cut in enumerate(projCut):
        binLo, binHi = cut
        h_sig[i] = h2d_sig.ProjectionY('py_sig_%dTo%dBins_%s'%(binLo, binHi, tag), binLo, binHi)
        h_bkg[i] = h2d_bkg.ProjectionY('py_bkg_%dTo%dBins_%s'%(binLo, binHi, tag), binLo, binHi)
        
        bins = 4
        h_sig[i].Rebin(bins)
        h_bkg[i].Rebin(bins)

        fbin = h_sig[i].FindFirstBinAbove()
        nbin = h_sig[i].FindLastBinAbove()
      
        x = array.array('d')  
        y = array.array('d')

        for ibin in xrange(fbin, nbin+1):

          '''  
          efficiency = (cut region) / (total region)
          have to always include the signal in the cut region , hence different way of 'scanning' the distribution for different taggers
          '''
          if tag=='deepak8md' or tag=='deepak8':
            
            # signal efficiency
            totSig = h_sig[i].Integral(fbin, nbin+1)
            cutSig = h_sig[i].Integral(ibin, nbin+1)
            effSig = cutSig / totSig
            x.append(effSig)
          
            # background efficiency
            totBkg = h_bkg[i].Integral(fbin, nbin+1)
            cutBkg = h_bkg[i].Integral(ibin, nbin+1)
            effBkg = cutBkg / totBkg
            y.append(effBkg)

          elif tag=='sdtau21':
           
            # signal efficiency
            totSig = h_sig[i].Integral(fbin, nbin+1)
            cutSig = h_sig[i].Integral(fbin, ibin)
            effSig = cutSig / totSig
            x.append(effSig)
          
            # background efficiency
            totBkg = h_bkg[i].Integral(fbin, nbin+1)
            cutBkg = h_bkg[i].Integral(fbin, ibin)
            effBkg = cutBkg / totBkg
            y.append(effBkg)

        #
        # plot
        #
        n = nbin+1 - fbin
        gr[i] = ROOT.TGraph(n,x,y)
        gr[i].SetTitle('%s; %s; %s' %(tagList[signal][tag], xaxisname, yaxisname))
        gr[i].GetXaxis().SetRangeUser(0,1.1)
        gr[i].GetYaxis().SetRangeUser(10e-5,5)
        gr[i].SetLineStyle(lines[i])
        gr[i].SetLineWidth(2)
        gr[i].SetLineColor(color[i])
        gr[i].SetMarkerColor(color[i])
        
        gr[i].Draw('AC' if i==0 else 'C SAME')
        leg.AddEntry(gr[i], legList[i])

      leg.Draw()
      c.SetTicks(1,1)
      c.Print("%sROC_%s_%s.png" %(outDir, signal, tag))
      # del gr

  elif multiTagger:

    ptRange = legList
    legListTag=[]
    histoName = ["Pt300To500", "Pt500To1000", "Pt1000To1500", "Pt1500To2000", "Pt2000to2500"]


    for i, cut in enumerate(projCut):

      binLo, binHi = cut
      gr = [None] * len(projCut)

      c = setCanv()
      leg = setLeg(len(legList))

      for j, tag in enumerate(tagList[signal]):
        legListTag+=[tag]
        #
        # get 2D histograms
        #
        if tag=='deepak8md' or tag=='deepak8':
          h2d_sig = inFileSig.Get('h_pt_'+tag).Clone()
          h2d_bkg = inFileBkg.Get('h_pt_'+tag).Clone()

          h2d1 = h2d_sig.Clone()

        elif tag=='sdtau21':
          h2d_sig = inFileSig.Get('h_pt_'+tag).Clone()
          h2d_bkg = inFileBkg.Get('h_pt_'+tag).Clone()
          
          h2d2 = h2d_sig.Clone()

        #
        # 1D projections
        #
        h_sig = h2d_sig.ProjectionY('py_sig_%dTo%dBins_%s'%(binLo, binHi,tag), binLo, binHi)
        h_bkg = h2d_bkg.ProjectionY('py_bkg_%dTo%dBins_%s'%(binLo, binHi,tag), binLo, binHi)
        
        bins = 1
        h_sig.Rebin(bins)
        h_bkg.Rebin(bins)

        fbin = h_sig.FindFirstBinAbove()
        nbin = h_sig.FindLastBinAbove()

        x = array.array('d')  
        y = array.array('d')

        for ibin in xrange(fbin, nbin+1):
          if tag=='deepak8md' or tag=='deepak8':
            
            # signal efficiency
            totSig = h_sig.Integral(fbin, nbin+1)
            cutSig   = h_sig.Integral(ibin, nbin+1)
            eff = (cutSig/totSig)
            x.append(eff)
          
            # background efficiency
            totBkg = h_bkg.Integral(fbin, nbin+1)
            cutBkg = h_bkg.Integral(ibin, nbin+1)
            effBkg = (cutBkg/totBkg)
            y.append(effBkg)

          elif tag=='sdtau21':

            # signal efficiency
            totSig = h_sig.Integral(fbin, nbin+1)
            cutSig = h_sig.Integral(fbin, ibin)
            eff = (cutSig/totSig)
            x.append(eff)
          
            # background efficiency
            totBkg = h_bkg.Integral(fbin, nbin+1)
            cutBkg = h_bkg.Integral(fbin, ibin)
            effBkg = (cutBkg/totBkg)
            y.append(effBkg)
        
        n = nbin+1 - fbin
        
        gr[j] = ROOT.TGraph(n,x,y)
        gr[j].SetTitle('W-tagging for %s; %s; %s' %(ptRange[i], xaxisname, yaxisname))
        gr[j].GetXaxis().SetLimits(0,1.1)
        gr[j].GetYaxis().SetRangeUser(10e-6,5)
        gr[j].SetLineStyle(lines[j])
        gr[j].SetLineWidth(2)
        gr[j].SetLineColor(color[j])
        gr[j].SetMarkerColor(color[j])

        gr[j].Draw("AC" if j==0 else "C SAME")
        leg.AddEntry(gr[j], legListTag[j], "l")

        outName="ROC_%s_%s" %(signal, histoName[i])

      leg.Draw()
      c.SetTicks()
      c.Print("%s%s.png" %(outDir, outName))
      del gr

    #   c.Write(histoName[i])

    # filename = "ROC_%s_multiTag" %(signal)
    # outFile = ROOT.TFile("%s%s.root" %(outDir, filename),"RECREATE")
    # h2d1.RebinY(20)
    # h2d2.RebinY(20)
    # h2d1.Write("pt_%s" %(tagList[signal][0]))
    # h2d2.Write("pt_%s" %(tagList[signal][1]))
    # outFile.Close()

def setCanv(name='',title='',width=800,height=800):
  c = ROOT.TCanvas(name, title, width, height)
  c.SetFillStyle(4000)
  c.SetLeftMargin(0.15)
  c.SetRightMargin(0.08)
  c.SetTopMargin(0.1)
  c.SetBottomMargin(0.15)
  c.SetLogy()
  return c

def setLeg(ll):
  xLeg = 0.65
  yLeg = 0.4
  leg_g =  0.04 * ll
  leg = ROOT.TLegend( xLeg+0.05, yLeg - leg_g, xLeg+0.15, yLeg )
  
  leg.SetShadowColor(0)
  leg.SetFillColor(0)
  leg.SetLineColor(0)
  leg.SetBorderSize(0)
  leg.SetTextFont(43)
  leg.SetTextSize(14)
  return leg

if __name__ == "__main__":
  main()