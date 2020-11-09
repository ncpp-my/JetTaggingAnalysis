#!/bin/bash
export X509_USER_PROXY=/afs/cern.ch/user/n/nbinnorj/myProxy
cd /afs/cern.ch/work/n/nbinnorj/AnaJetTagging/CMSSW_10_2_15/src/
eval `scramv1 runtime -sh`

cd JetTaggingAnalysis/NanoAODAnalyzer/pyroot/
echo "Running ReadNanoAOD.py"

FULLPATH="/afs/cern.ch/work/n/nbinnorj/AnaJetTagging/CMSSW_10_2_15/src/JetTaggingAnalysis/SampleListNanoAOD/${1}.txt"

python ./ReadNanoAOD.py --input ${FULLPATH} --outputDir "root://eosuser.cern.ch//eos/user/n/nbinnorj/AnaJetTagging/Ntuples/"

echo "ProcessNanoAOD_AnaJetTagging::DONE"
