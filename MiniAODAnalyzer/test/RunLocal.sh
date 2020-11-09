#!/bin/sh


SAMPLES=(
"VBFGZZM600"
# "ZprimeWWM600"
# "ZprimeWWM800"
# "ZprimeWWM1000"
# "ZprimeWWM1200"
# "ZprimeWWM1400"
# "ZprimeWWM1600"
# "ZprimeWWM1800"
# "ZprimeWWM2000"
# "ZprimeWWM2500"
# "ZprimeWWM3000"
# "ZprimeWWM3500"
# "ZprimeWWM4000"
# "ZprimeWWM4500"
# "GZZM400"
# "GZZM450"
# "GZZM500"
# "GZZM550"
# "GZZM600"
# "GZZM650"
# "GZZM800"
# "GZZM900"
# "GZZM1000"
# "GZZM1200"
# "GZZM1400"
# "GZZM1600"
# "GZZM1800"
# "GZZM2000"
# "GZZM2500"
# "GZZM3000"
# "GZZM3500"
# "GZZM4000"
# "GZZM4500"
)

for s in "${SAMPLES[@]}"
do
  FULLPATH="../../SampleListMiniAOD/${s}.txt"
  python ReadMiniAOD.py --input ${FULLPATH}
done

