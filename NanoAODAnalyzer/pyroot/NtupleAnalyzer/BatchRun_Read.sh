#!/bin/bash
#
# CHECK: Specify your path
#
export X509_USER_PROXY=/afs/cern.ch/user/s/ssyedoma/myProxy
cd /afs/cern.ch/work/s/ssyedoma/AnaJetTagging/CMSSW_10_2_22/src/
#
#
eval `scramv1 runtime -sh`

cd JetTaggingAnalysis/NanoAODAnalyzer/pyroot/NtupleAnalyzer/

SAMPLE=${1}

echo "Running ReadNtuple.py"
python ./ReadNtuple.py --batch --sample ${SAMPLE}
# python ./ReadNtuple2.py --batch --sample ${SAMPLE}