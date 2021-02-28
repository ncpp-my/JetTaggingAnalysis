import sys
import os
import glob
import ROOT
from collections import OrderedDict 

ROOT.gROOT.SetBatch()

color1=[ROOT.kRed,ROOT.kBlue,ROOT.kGreen]
color2 = [46,42,30,36,38,27]
lgd = [ROOT.kFullSquare, ROOT.kFullCircle, ROOT.kFullTriangleUp, ROOT.kFullTriangleDown, ROOT.kOpenCircle, ROOT.kOpenSquare ]

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

def PlotTH1F(outDir, filename, histoList):

  outFile = ROOT.TFile("%s%s%s.root" %(outDir, filename),"RECREATE")

  i=0
  for a in histoList:
    a.SetLineColor(ROOT.kRed)
    a.SetLineWidth(2)
    a.SetMarkerColor(ROOT.kRed)
    a.SetStats(0)
    a.Write()
    i+=1
  outFile.Close()

def PlotTH2F(outDir, filename, histoList):

  outFile = ROOT.TFile("%s%s.root" %(outDir, filename), "RECREATE")

  for a in histoList:
    a.SetStats(0)
    a.SetOption("COLZ")
    a.Write()
  
  outFile.Close()

def PlotMulPDFTH2F(outDir, pdfname, histoList):
  
  c=ROOT.TCanvas("","",877,620)
  for i, a in enumerate(histoList):
    a.SetStats(0)
    a.SetOption("COLZ")
    a.Draw()
    c.SetTicks(1,1)
    c.Print("%s%s.pdf" %(outDir, pdfname[i]))

def plotPDF(pdfname, legname, outDir, histoList):
  color = [46,42,30,36,38]
  lgd = [ROOT.kFullSquare, ROOT.kFullCircle, ROOT.kFullTriangleUp, ROOT.kFullTriangleDown, ROOT.kOpenCircle, ROOT.kOpenSquare ]
  leg=BeginLeg(len(legname))
  i=0
  c = ROOT.TCanvas("","",877, 620)
  for a in histoList:
    a.SetStats(0)
    a.SetLineWidth(1)
    a.SetLineColor(color[i])
    a.SetMarkerColor(color[i])
    a.SetMarkerStyle(lgd[i])
    a.SetMaximum(a.GetMaximum()+a.GetMaximum())

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

def plotROOT(filename, legname, outDir, histoList):
  color = [46,42,30,36,38]
  lgd = [ROOT.kFullSquare, ROOT.kFullCircle, ROOT.kFullTriangleUp, ROOT.kFullTriangleDown, ROOT.kOpenCircle, ROOT.kOpenSquare ]

  ################################
  ### ROOT FILE ###
  ################################
  # outFile = ROOT.TFile("%s%s.root" %(outDir, filename), "RECREATE")

  # for a in histoList:
  #   a.SetStats(0)
  #   a.SetOption("COLZ")
  #   a.Write()

  # outFile.Close()

def plotEff(pdfname, legname, outDir, effList):
  leg=BeginLeg(len(legname))
  i=0
  c = ROOT.TCanvas("","",877, 620)
  for a in effList:
    a.SetStatisticOption(0)
    a.SetLineWidth(2)
    a.SetLineColor(color2[i])
    a.SetLineColor(color2[i])
    a.SetMarkerColor(color2[i])
    a.SetMarkerStyle(lgd[i])
    # a.SetFillColor(color2[i])

    if i==0:
      a.Draw()
    else:
      a.Draw("SAME")
    
    leg.AddEntry(a, legname[i], "p")
    i+=1

    c.Update() 
    graph = a.GetPaintedGraph()
    graph.GetXaxis().SetLimits(0, 600.0)
    graph.SetMinimum(0)
    graph.SetMaximum(1.6) 
    xmax = graph.GetXaxis().GetXmax()
    c.Update()
   

  line = ROOT.TLine(0,1,xmax,1)
  line.SetLineStyle(7)
  line.Draw()
  leg.Draw()
  c.SetTicks(1,1)
  c.Print("%s%s.pdf" %(outDir, pdfname))
