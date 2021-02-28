#!/bin/bash

#
# CHECK: Specify your path
#
export X509_USER_PROXY=/afs/cern.ch/user/s/ssyedoma/myProxy

#
# CHECK: Specify your path
#
cd /afs/cern.ch/work/s/ssyedoma/AnaJetTagging/CMSSW_10_2_22/src/

#
#
#
eval `scramv1 runtime -sh`

cd JetTaggingAnalysis/NanoAODAnalyzer/pyroot/NtupleMaker/
echo "Running ReadNanoAOD.py"

INPUTPATH="../../../SampleListNanoAOD/${1}.txt"

python ./MakeNtupleFromNanoAOD.py --input ${INPUTPATH}

echo "ProcessNanoAOD_AnaJetTagging::DONE"
