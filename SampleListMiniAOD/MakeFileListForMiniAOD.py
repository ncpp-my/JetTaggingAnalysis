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
samples["VBFGZZM600"]    = "/VBF_BulkGravToZZinclusive_narrow_M-600_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM"
# samples["GZZM400"]       = "/BulkGravToZZToZlepZhad_narrow_M-400_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["GZZM450"]       = "/BulkGravToZZToZlepZhad_narrow_M-450_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["GZZM500"]       = "/BulkGravToZZToZlepZhad_narrow_M-500_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["GZZM550"]       = "/BulkGravToZZToZlepZhad_narrow_M-550_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["GZZM600"]       = "/BulkGravToZZToZlepZhad_narrow_M-600_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["GZZM650"]       = "/BulkGravToZZToZlepZhad_narrow_M-650_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["GZZM800"]       = "/BulkGravToZZToZlepZhad_narrow_M-800_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["GZZM900"]       = "/BulkGravToZZToZlepZhad_narrow_M-900_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["GZZM1000"]      = "/BulkGravToZZToZlepZhad_narrow_M-1000_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["GZZM1200"]      = "/BulkGravToZZToZlepZhad_narrow_M-1200_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["GZZM1400"]      = "/BulkGravToZZToZlepZhad_narrow_M-1400_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["GZZM1600"]      = "/BulkGravToZZToZlepZhad_narrow_M-1600_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["GZZM1800"]      = "/BulkGravToZZToZlepZhad_narrow_M-1800_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["GZZM2000"]      = "/BulkGravToZZToZlepZhad_narrow_M-2000_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["GZZM2500"]      = "/BulkGravToZZToZlepZhad_narrow_M-2500_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["GZZM3000"]      = "/BulkGravToZZToZlepZhad_narrow_M-3000_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["GZZM3500"]      = "/BulkGravToZZToZlepZhad_narrow_M-3500_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["GZZM4000"]      = "/BulkGravToZZToZlepZhad_narrow_M-4000_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["GZZM4500"]      = "/BulkGravToZZToZlepZhad_narrow_M-4500_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["ZprimeWWM600"]  = "/ZprimeToWW_narrow_M-600_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["ZprimeWWM800"]  = "/ZprimeToWW_narrow_M-800_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["ZprimeWWM1000"] = "/ZprimeToWW_narrow_M-1000_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["ZprimeWWM1200"] = "/ZprimeToWW_narrow_M-1200_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["ZprimeWWM1400"] = "/ZprimeToWW_narrow_M-1400_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["ZprimeWWM1600"] = "/ZprimeToWW_narrow_M-1600_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["ZprimeWWM1800"] = "/ZprimeToWW_narrow_M-1800_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["ZprimeWWM2000"] = "/ZprimeToWW_narrow_M-2000_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["ZprimeWWM2500"] = "/ZprimeToWW_narrow_M-2500_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["ZprimeWWM3000"] = "/ZprimeToWW_narrow_M-3000_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["ZprimeWWM3500"] = "/ZprimeToWW_narrow_M-3500_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["ZprimeWWM4000"] = "/ZprimeToWW_narrow_M-4000_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["ZprimeWWM4500"] = "/ZprimeToWW_narrow_M-4500_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
# samples["QCDPt15To7000"] = "/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"

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