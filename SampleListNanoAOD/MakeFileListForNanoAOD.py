#! /usr/bin/env python
import os
import subprocess
import collections
# REMEMBER TO SOURCE CRAB3 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# DO: source /cvmfs/cms.cern.ch/crab3/crab.sh
# https://twiki.cern.ch/twiki/bin/view/CMS/DBS3APIInstructions
# https://github.com/dmwm/DBS/blob/master/Client/src/python/dbs/apis/dbsClient.py
# 
from dbs.apis.dbsClient import DbsApi 
dbs = DbsApi('https://cmsweb.cern.ch/dbs/prod/global/DBSReader')

samples = collections.OrderedDict()

samples["WprimeWZM600"]  = "/WprimeToWZToWhadZhad_narrow_M-600_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["WprimeWZM800"]  = "/WprimeToWZToWhadZhad_narrow_M-800_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["WprimeWZM1000"] = "/WprimeToWZToWhadZhad_narrow_M-1000_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["WprimeWZM1200"] = "/WprimeToWZToWhadZhad_narrow_M-1200_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["WprimeWZM1400"] = "/WprimeToWZToWhadZhad_narrow_M-1400_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["WprimeWZM1600"] = "/WprimeToWZToWhadZhad_narrow_M-1600_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["WprimeWZM2000"] = "/WprimeToWZToWhadZhad_narrow_M-2000_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["WprimeWZM2500"] = "/WprimeToWZToWhadZhad_narrow_M-2500_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["WprimeWZM3000"] = "/WprimeToWZToWhadZhad_narrow_M-3000_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["WprimeWZM3500"] = "/WprimeToWZToWhadZhad_narrow_M-3500_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["WprimeWZM4000"] = "/WprimeToWZToWhadZhad_narrow_M-4000_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["WprimeWZM4500"] = "/WprimeToWZToWhadZhad_narrow_M-4500_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["WprimeWZM5000"] = "/WprimeToWZToWhadZhad_narrow_M-5000_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["WprimeWZM5500"] = "/WprimeToWZToWhadZhad_narrow_M-5500_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["WprimeWZM6000"] = "/WprimeToWZToWhadZhad_narrow_M-6000_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["WprimeWZM6500"] = "/WprimeToWZToWhadZhad_narrow_M-6500_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["WprimeWZM7000"] = "/WprimeToWZToWhadZhad_narrow_M-7000_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["WprimeWZM7500"] = "/WprimeToWZToWhadZhad_narrow_M-7500_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["WprimeWZM8000"] = "/WprimeToWZToWhadZhad_narrow_M-8000_TuneCP5_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"

samples["GToZZM800"]     = "/BulkGravToZZToZhadZhad_narrow_M-800_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["GToZZM1000"]    = "/BulkGravToZZToZhadZhad_narrow_M-1000_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["GToZZM1200"]    = "/BulkGravToZZToZhadZhad_narrow_M-1200_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["GToZZM1400"]    = "/BulkGravToZZToZhadZhad_narrow_M-1400_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["GToZZM1600"]    = "/BulkGravToZZToZhadZhad_narrow_M-1600_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["GToZZM1800"]    = "/BulkGravToZZToZhadZhad_narrow_M-1800_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["GToZZM2000"]    = "/BulkGravToZZToZhadZhad_narrow_M-2000_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["GToZZM3000"]    = "/BulkGravToZZToZhadZhad_narrow_M-3000_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
samples["GToZZM4000"]    = "/BulkGravToZZToZhadZhad_narrow_M-4000_13TeV-madgraph/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"

# samples["ZprimeToTTM500"]  = "/ZprimeToTT_M500_W5_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
# samples["ZprimeToTTM50_ext1"]  = "/ZprimeToTT_M500_W5_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7_ext1-v1/NANOAODSIM"
# samples["ZprimeToTTM750"]  = "/ZprimeToTT_M750_W7p5_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
# samples["ZprimeToTTM750_ext1"]  = "/ZprimeToTT_M750_W7p5_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7_ext1-v1/NANOAODSIM"
# samples["ZprimeToTTM1000"] = "/ZprimeToTT_M1000_W10_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
# samples["ZprimeToTTM1000_ext1"] = "/ZprimeToTT_M1000_W10_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7_ext1-v1/NANOAODSIM"
# samples["ZprimeToTTM1250"] = "/ZprimeToTT_M1250_W12p5_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
# samples["ZprimeToTTM1250_ext1"] = "/ZprimeToTT_M1250_W12p5_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7_ext1-v1/NANOAODSIM"
# samples["ZprimeToTTM1500"] = "/ZprimeToTT_M1500_W15_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
# samples["ZprimeToTTM1500_ext1"] = "/ZprimeToTT_M1500_W15_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7_ext1-v1/NANOAODSIM"
# samples["ZprimeToTTM2000"] = "/ZprimeToTT_M2000_W20_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
# samples["ZprimeToTTM2000_ext1"] = "/ZprimeToTT_M2000_W20_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7_ext1-v1/NANOAODSIM"
# samples["ZprimeToTTM2500"] = "/ZprimeToTT_M2500_W25_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
# samples["ZprimeToTTM2500_ext1"] = "/ZprimeToTT_M2500_W25_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7_ext1-v1/NANOAODSIM"
# samples["ZprimeToTTM3000"] = "/ZprimeToTT_M3000_W30_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
# samples["ZprimeToTTM3000_ext1"] = "/ZprimeToTT_M3000_W30_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7_ext1-v1/NANOAODSIM"
# samples["ZprimeToTTM3500"] = "/ZprimeToTT_M3500_W35_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
# samples["ZprimeToTTM3500_ext1"] = "/ZprimeToTT_M3500_W35_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7_ext1-v1/NANOAODSIM"
# samples["ZprimeToTTM4000"] = "/ZprimeToTT_M4000_W40_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
# samples["ZprimeToTTM4000_ext1"] = "/ZprimeToTT_M4000_W40_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7_ext1-v1/NANOAODSIM"
# samples["ZprimeToTTM5000"] = "/ZprimeToTT_M5000_W50_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
# samples["ZprimeToTTM5000_ext1"] = "/ZprimeToTT_M5000_W50_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7_ext1-v1/NANOAODSIM"
# samples["ZprimeToTTM6000"] = "/ZprimeToTT_M6000_W60_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
# samples["ZprimeToTTM6000_ext1"] = "/ZprimeToTT_M6000_W60_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7_ext1-v1/NANOAODSIM"
# samples["ZprimeToTTM7000"] = "/ZprimeToTT_M7000_W70_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
# samples["ZprimeToTTM7000_ext1"] = "/ZprimeToTT_M7000_W70_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7_ext1-v1/NANOAODSIM"
# samples["ZprimeToTTM8000"] = "/ZprimeToTT_M8000_W80_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"
# samples["ZprimeToTTM8000_ext1"] = "/ZprimeToTT_M8000_W80_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7_ext1-v1/NANOAODSIM"

samples["QCDPt15To7000"] = "/QCD_Pt-15to7000_TuneCP5_Flat2017_13TeV_pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"

for sample in samples:
  shortName = sample
  dataset   = samples[sample]
  fout      = "%s.txt" %(shortName)
  print "Saving path to files in %s for sample = %s" %(fout, dataset)
  #
  # This spits out a list of dictionary. Each element of the list
  # is a single file of the dataset
  #
  fileDictList = dbs.listFiles(dataset=dataset, detail=0)

  fo = open(fout, "w")
  for fileDict in fileDictList:
    fileNameFull = fileDict["logical_file_name"]
    fo.write(fileNameFull+'\n')
  fo.close()