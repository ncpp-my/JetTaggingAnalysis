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

samples["BulkGravWWM600"] = "/BulkGravToWWToWhadWhad_narrow_M-600_TuneCP5_PSWeights_13TeV-madgraph-pythia/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"
samples["BulkGravWWM700"] = "/BulkGravToWWToWhadWhad_narrow_M-700_TuneCP5_PSWeights_13TeV-madgraph-pythia/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"
samples["BulkGravWWM800"] = "/BulkGravToWWToWhadWhad_narrow_M-800_TuneCP5_PSWeights_13TeV-madgraph-pythia/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"
samples["BulkGravWWM900"] = "/BulkGravToWWToWhadWhad_narrow_M-900_TuneCP5_PSWeights_13TeV-madgraph-pythia/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"
samples["BulkGravWWM1000"] = "/BulkGravToWWToWhadWhad_narrow_M-1000_TuneCP5_PSWeights_13TeV-madgraph-pythia/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"
samples["BulkGravWWM1200"] = "/BulkGravToWWToWhadWhad_narrow_M-1200_TuneCP5_PSWeights_13TeV-madgraph-pythia/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"
samples["BulkGravWWM1400"] = "/BulkGravToWWToWhadWhad_narrow_M-1400_TuneCP5_PSWeights_13TeV-madgraph-pythia/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"
samples["BulkGravWWM1600"] = "/BulkGravToWWToWhadWhad_narrow_M-1600_TuneCP5_PSWeights_13TeV-madgraph-pythia/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"
samples["BulkGravWWM1800"] = "/BulkGravToWWToWhadWhad_narrow_M-1800_TuneCP5_PSWeights_13TeV-madgraph-pythia/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"
samples["BulkGravWWM2000"] = "/BulkGravToWWToWhadWhad_narrow_M-2000_TuneCP5_PSWeights_13TeV-madgraph-pythia/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"
samples["BulkGravWWM2500"] = "/BulkGravToWWToWhadWhad_narrow_M-2500_TuneCP5_PSWeights_13TeV-madgraph-pythia/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"
samples["BulkGravWWM3000"] = "/BulkGravToWWToWhadWhad_narrow_M-3000_TuneCP5_PSWeights_13TeV-madgraph-pythia/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"
samples["BulkGravWWM3500"] = "/BulkGravToWWToWhadWhad_narrow_M-3500_TuneCP5_PSWeights_13TeV-madgraph-pythia/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"
samples["BulkGravWWM4000"] = "/BulkGravToWWToWhadWhad_narrow_M-4000_TuneCP5_PSWeights_13TeV-madgraph-pythia/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"
samples["BulkGravWWM4500"] = "/BulkGravToWWToWhadWhad_narrow_M-4500_TuneCP5_PSWeights_13TeV-madgraph-pythia/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"

samples["QCDPt15To7000"] = "/QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/RunIISummer19UL18NanoAODv2-FlatPU0to70_106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"

for sample in samples:
  shortName = sample
  dataset   = samples[sample]
  fout      = "%s.txt" %(shortName)

  #
  # This spits out a list of dictionary. Each element of the list
  # is a single file of the dataset
  #
  fileDictList = dbs.listFiles(dataset=dataset, detail=0)
  print "Saving path to files in %s for sample = %s, nfiles = %d" %(fout, dataset, len(fileDictList))
  fo = open(fout, "w")
  for fileDict in fileDictList:
    fileNameFull = fileDict["logical_file_name"]
    fo.write(fileNameFull+'\n')
  fo.close()
