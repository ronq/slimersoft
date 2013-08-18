#!/bin/bash
# 
# This submits a number of batch jobs in order to rootify files



export job_name=""
#export raw_data_dir=/proj/Slimer/Slimer_mk2/8_01_2013/am241_8_01_2013_200msec/
#export raw_data_dir=/proj/Slimer/Slimer_mk2/8_01_2013/no_source_8_01_2013_200msec/
export raw_data_dir=/proj/Slimer/Slimer_mk2/8_01_2013/c14_8_01_2013_200msec/
export scratch=/local_scratch/ronquest/temp/
export final_dir=/proj/Slimer/Slimer_mk2/8_01_2013_mikes_ana/results/
export background_path=/proj/Slimer/Slimer_mk2/8_01_2013_mikes_ana/results/no_source_8_01_2013_200msec_average_array.npz

FILES=${raw_data_dir}${job_name}*
for f in $FILES
do
    export input_file=$f
    echo Processing $input_file
    #the qsub script will inherit the enviroment variables 
    #sleep 30
    #sleep 2 # this is about as fast as analysis jobs can be submitted and run.
    qsub run_image_analysis.sh
done        


