This repository describes on how to run the full pipeline. Step 3 is the most time consuming. You need to run it only once to generate the data of interest. 

1. Clone the repository 

   git clone https://github.com/sawal386/project

2. cd into the directory 
    
    cd project 

3. The first step is to get the data of interest from the source json file. Open scripts/settings.sh and check if the directories are correct. Basically, you need to specify the directory containing json data and the output location.  Also go over generate_data.sh. The run, 
    
    bash scripts/generate_data.sh 

The source data for this is the raw json file containing the information about all the articles. I am assuming the file is name as "{year}.json". If possible, follow this convention. Otherwise, you will have to make modifications in main_generate.py. The outputs are automatically saved in the path "inference_data/{subject}/{subject}_{year}_{month}". The saved file is a .pkl file containing TimeCollection object. It includes all articles published in the given year and month. 

Note that this takes sometime to complete. The most expensive phase of this is at the beginning. Uploading 10 Gigs of json file into the memory takes time. Also, make sure sufficient memory is available. Otherwise the program crashes. 

4. Now that we have created the inference data, we will run the actual inference. Before this check the script run_inference.sh in the folder scripts. Make sure the paths are correct. Next run,

    bash scripts/run_inference.sh 

This script will run the main_analysis.py. The inputs to this are the parquet files containing the distribution. In the current version, the file can be accessed via "project/data/distribution/distribution.parquet". The other input file is location to the folder containing inference data distribution obtained from step 3. The program will automatically loop through the files in the folder and use the relevant parquet files to estimate alpha. The final output is saved to output/{subject_name}_{year}.csv

5. For reproducing (some of) the results in the report, run:
   a. prepare_data.ipynb 
   b. reproduce_results.ipynb 
   c. validation.ipynb 
 

