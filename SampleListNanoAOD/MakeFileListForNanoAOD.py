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