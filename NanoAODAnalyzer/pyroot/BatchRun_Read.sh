#!/bin/bash
export X509_USER_PROXY=/afs/cern.ch/user/s/ssyedoma/myProxy
cd /afs/cern.ch/work/s/ssyedoma/AnaJetTagging/CMSSW_10_2_15/src/
eval `scramv1 runtime -sh`

cd JetTaggingAnalysis/NanoAODAnalyzer/pyroot/

echo "Running WZ_mass.py"
python ./WZ_mass.py

echo "Process_Read::DONE"
