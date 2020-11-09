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
cmsrel CMSSW_10_2_22
cd CMSSW_10_2_22/src
cmsenv
```

### 1. Checkout framework

```bash
git clone git@github.com:ncpp-my/JetTaggingAnalysis.git JetTaggingAnalysis
```

### 2. Checkout NanoAOD-Tools

Get NanoAODTools framework

```bash
git clone git@github.com:cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools

```

Instruction from https://github.com/cms-nanoAOD/nanoAOD-tools#checkout-instructions-cmssw

### 3. Compile

```bash
scram b -j 4
cmsenv
```