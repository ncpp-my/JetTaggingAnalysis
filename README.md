# JetTaggingAnalysis

## Setting up framework
### 0. Setup CMSSW for the first time

Make a working directory (any name would do):
```bash
mkdir AnaJetTagging
cd AnaJetTagging
```

Setup a CMSSW release.

```bash
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_15
cd CMSSW_10_2_15/src
cmsenv
```

### 1. Checkout framework

```bash
git clone git@github.com:ncpp-my/JetTaggingAnalysis.git JetTaggingAnalysis
```

### 2. Checkout framework which the parent NanoAODAnalysis framework

```bash
git clone git@github.com:nurfikri89/NanoAODAnalysis.git 
```

### 3. Checkout NanoAOD-Tools

Get NanoAODTools framework

```bash
git clone git@github.com:cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools

```

Instruction from to https://github.com/cms-nanoAOD/nanoAOD-tools#checkout-instructions-cmssw

### 4. Compile

```bash
scram b -j 4
cmsenv
```