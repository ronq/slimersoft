#!/bin/bash
# 
# This submits a number of batch jobs in order to rootify files






#export job_name=2012-3-5-LongRun_Deg135_133Ba_1uCi
#export raw_data_dir=/proj3/GLAD/Raw/LongRun/
#export job_name=2012-3-9-LongRun_Deg135_133Ba_10uCi
#export job_name=2012-4-19-GLAD_v2_Na22_test
#export job_name=2012-4-19-GLAD_v2_133Ba_Deg0
#export job_name=2012-5-4-GLAD_v6_133Ba_Splinter
export job_name=2012
#export raw_data_dir=/bigscratch1/ronquest/GLAD/
#export raw_data_dir=/bigscratch1/ronquest/GLAD/2012-4-18/
#export raw_data_dir=/bigscratch4/ronquest/GLAD/2012-4-30/
#export raw_data_dir=/proj/GLAD/Raw/GLAD_v6/
#export raw_data_dir=/bigscratch4/ronquest/GLAD/GLAD_v10/Raw/
#export raw_data_dir=/bigscratch4/ronquest/GLAD/GLAD_v11/Raw/
export raw_data_dir=/bigscratch4/ronquest/GLAD/Testing/Raw/
export scratch=/local_scratch/ronquest/temp/
#export final_dir=/proj3/GLAD/NominalData_rootified/
#export final_dir=/bigscratch1/ronquest/GLAD/2012-4-18/ORCAROOT/
#export final_dir=/bigscratch4/ronquest/GLAD/GLAD_v10/Rootified/
export final_dir=/bigscratch4/ronquest/GLAD/Testing/Rootified/
FILES=${raw_data_dir}${job_name}*
for f in $FILES
do
    export input_file=$f
    echo Processing $input_file
    #the qsub script will inherit the enviroment variables 
    #sleep 30
    sleep 20
    qsub run_rootify.sh
done        


