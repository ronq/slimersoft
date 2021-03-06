#!/bin/bash
# sample script to run image_analysis.py via submit_image_analsyis.sh
# submit by doing this:   qsub  run_image_analysis.sh
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

source /proj/Software/Notes/SetupScripts/setup_anaconda_root.sh
export executable_path=/home/ronquest/Work/SLIMER/AnalysisCode/ImageAnalysis/image_analysis.py

# cd into working directory
cd ${scratch}

export input_label=${input_file#$raw_data_dir}
export output_label=${input_label%.tif}

# copy the input file over to scratch disk first 
nice cp ${input_file} .


echo 'Processing ' ${input_label} 
limit -m 3146000
nice ${executable_path} ${input_label} ${background_path} ${output_label}


# now delete the input file 
rm ${input_label}
# mv the rest to the final destination
nice mv ${output_label}*  ${final_dir}

