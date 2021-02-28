## Getting ROC curves:

1. Run **ReadNtuple.py** with **BatchRun_Read.sh.sub** to get 2D (tag score - pT) histograms
2. Merge the histograms according to sample with **mergeHistos.py**
3. Run **ROCMaker.py**


## To Do:

1. Check NtupleMaker implementation.
2. Check ReadNtuple implementation ie. selections.
3. Script to compute scale factors from the ROC curves or efficiency
4. Clean up any redundancies.
