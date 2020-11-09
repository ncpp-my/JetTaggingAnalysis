#!/bin/bash
#
# CHECK: Specify your path
#
export X509_USER_PROXY=/afs/cern.ch/user/n/nbinnorj/myProxy
#
# CHECK: Specify your path
#
cd /afs/cern.ch/work/n/nbinnorj/AnaJetTagging/CMSSW_10_2_22/src/
#
#
#
eval `scramv1 runtime -sh`

cd JetTaggingAnalysis/NanoAODAnalyzer/pyroot/

echo "Running WZ_mass.py"
python ./WZ_mass.py

echo "Process_Read::DONE"
