import sys
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

#
# Set version number
#
version="v0"

config.General.requestName     = 'JetTagPostNanoMC16_'+version
#
# Change this PATH where the crab directories are stored
# Example: config.General.workArea = '/afs/cern.ch/work/n/nbinnorj/private/crab_projects/'
#
config.General.workArea        = '/afs/cern.ch/work/n/nbinnorj/private/crab_projects/'
config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName   = 'PSet.py'
config.JobType.scriptExe  = 'crab_script.sh'
config.JobType.maxJobRuntimeMin = 300
config.JobType.scriptArgs = [
'isMC=1',
'isSig=0',
'era=2016',
]
config.JobType.inputFiles = [
'../../scripts/keep_and_drop_branches.txt',
'../ProcessSampleCrab.py',
'../../../../PhysicsTools/NanoAODTools/scripts/haddnano.py' #hadd nano will not be needed once nano tools are in cmssw
]
config.JobType.sendPythonFolder  = True
config.JobType.outputFiles = ['tree.root','histo.root']

config.Data.inputDataset     = '/WprimeToWZToWhadZlep_width0p1_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM' #Dummy
config.Data.outputDatasetTag = 'JetTagPostNanoMC16_Test_v0' # Dummy

config.Data.splitting    = 'FileBased'
config.Data.unitsPerJob  = 1
config.Data.publication  = False
config.Data.allowNonValidInputDataset = True
config.JobType.allowUndistributedCMSSW = True

config.Data.outLFNDirBase  = '/store/user/nbinnorj/CRABOUTPUT_JetTag_'+version+'/'
config.Site.storageSite    = 'T2_CH_CERNBOX'

config.Data.ignoreLocality   = True
whitelist_sites=[
'T2_CH_CERN',
'T2_US_*',
'T2_UK_*',
'T2_DE_*',
'T2_FR_*',
]
config.Site.whitelist = whitelist_sites

# config.Data.ignoreLocality   = False
# whitelist_sites=['T2_CH_CERN']
# config.Site.whitelist = whitelist_sites

if __name__ == '__main__':
  #
  # Read in txt file with list of samples
  #
  f = open(sys.argv[1]) 
  samplelist = f.readlines()
  samplelist = [x.strip() for x in samplelist] 

  from CRABAPI.RawCommand import crabCommand
  for dataset in samplelist:
    print "\n\n"
    print "======================================================================================"
    if dataset.startswith( '#' ): 
      print "Skipping : ", dataset
      continue
    print "Send CRAB job for ", dataset
    config.Data.inputDataset = dataset
    #
    # Have to make unique requestName. pain in the ass really
    # Sample naming convention is a bit dumb and makes this more difficult.
    #
    primaryName   = dataset.split('/')[1].split("_")[0:3]
    primaryName   = "_".join(primaryName)
    secondaryName = dataset.split('/')[2]
    secondaryName = secondaryName.replace("RunIISummer16NanoAODv5","MC16NanoAODv5")
    secondaryName = secondaryName.replace("Nano1June2019_","")
    #
    requestName = primaryName + "_" + secondaryName.replace("PUMoriond17_102X_mcRun2_asymptotic_v7","")
    requestName = "XZV_" + requestName + "_" + version
    config.General.requestName   = requestName
    #  
    outputDatasetTag = "XZV_" + secondaryName + "_" + version
    config.Data.outputDatasetTag = outputDatasetTag 
    #
    print requestName , " | ", outputDatasetTag
    crabCommand('submit', config = config)
