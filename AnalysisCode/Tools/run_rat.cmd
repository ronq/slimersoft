#!/bin/bash
# sample script to run RAT via SGE arrays.
# submit by doing this:   qsub -t 1-10 sge_rat.sh
# -- here's the SGE crap ------

# set the shell to use
#$ -S /bin/bash
# import all environment variables
#$ -V
# set the current directory as the working directory
#$ -cwd
# join the stdout and stderr into a single log file
#$ -j yes
echo Running on `hostname`

source ~/Work/MiniCLEAN/RAT/setup_rat.cmd
#export job_name=na22_
export job_name=Pm147_nov2012_run6
export scratch=/local_scratch/ronquest/temp/
export final_dir=/bigscratch3/ronquest/MiniCLEAN/Pm147

export macro_name=Pm147.mac
nice rat -o ${scratch}${job_name}_${SGE_TASK_ID}.root ${macro_name} >& ${job_name}_${SGE_TASK_ID}.joblog
	
mv ${scratch}${job_name}_${SGE_TASK_ID}.root ${final_dir}/${job_name}_${SGE_TASK_ID}.root

