import os, glob, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d' , '--delComplete', action='store_true')
args = parser.parse_args()
delComplete = args.delComplete

allOutFile =  glob.glob('./Histo.*.out')
allOutFile.sort() # sort by name

jobsDone=[]
jobsNotDone=[]

for fileName in allOutFile:
  file = open(fileName,"r")


  lines = file.read()
  if "Process_Read::DONE" in lines:
    jobsDone.append(fileName)
  else:
    jobsNotDone.append(fileName)

print "============================================"
print "                Jobs Done                   "
print "============================================"

for jobs in jobsDone:
  print jobs

print "============================================"
print "                Jobs Still Not Done         "
print "============================================"

for jobs in jobsNotDone:
  print jobs


print "========================================================"
print "                Checking last line of jobs  not done"
print "========================================================"

for jobs in jobsNotDone:
  print jobs 
  os.system('tail -n 1 ' + jobs)
  print "\n"

if delComplete:
	if len(jobsDone)==0: print "no completed job to be deleted"
	else:
		for job in jobsDone:
			print "deleting " + job +" . . ."
			os.system("rm {job}.err {job}.out".format(job=job.replace(".out","")))