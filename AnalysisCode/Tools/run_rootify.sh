#!/bin/bash
# sample script to run MJORCAROOT via submit_rootfiy.sh
# submit by doing this:   qsub -t 1-10 run_rootify.sh
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

source /home/ronquest/Work/Majorana/Software/mgsw/Majorana_env.sh

# cd into working directory
cd ${scratch}
#export label=${input_file#$raw_data_dir}
export zipped_file=${input_file#$raw_data_dir}
export label=${zipped_file%.bz2}
# copy the input file over to scratch disk first 
nice cp ${input_file} .
# unzip the input file
nice bunzip2 ${zipped_file}

#nice majorcaroot --sis --validatexml --eventwindow 5us  --label ${label}_5us ${input_file}
echo 'Processing ' ${label} 
#nice majorcaroot --sis --validatexml --eventwindow 5us  --label ${label}_5us ${label} | gzip >& ${label}_5us.log.gz
nice majorcaroot --sis --validatexml --eventwindow 50us  --label ${label}_50us ${label} | gzip >& ${label}_50us.log.gz

# now delete the input file 
rm ${label}
#nice mv ${label}_5us*  ${final_dir}
nice mv ${label}_50us*  ${final_dir}
	
#mv ${scratch}${job_name}${SGE_TASK_ID}.root ${final_dir}/${job_name}_${SGE_TASK_ID}.root

