This repository describes how to run the full pipeline. Step 3 is the most time-consuming. You need to run it only once to generate the data of interest.

Clone the repository
git clone https://github.com/sawal386/cs224c_project

cd into the directory
cd cs224c_project

To reproduce the main results, you can skip to step 5. Steps 3 and 4 are for preprocessing the raw data from the OJS systems.

The first step is to get the data of interest from the source JSON file. Open scripts/settings.sh and check if the directories are correct. Basically, you need to specify the directory containing JSON data and the output location. Also go over generate_data.sh. Then run,
bash scripts/generate_data.sh

The source data for this is the raw JSON file containing the information about all the articles. I am assuming the file is named as "{year}.json". If possible, follow this convention. Otherwise, you will have to make modifications in main_generate.py. The outputs are automatically saved in the path "inference_data/{subject}/{subject}{year}{month}". The saved file is a .pkl file containing a TimeCollection object. It includes all articles published in the given year and month.

Note that this takes some time to complete. The most expensive phase of this is at the beginning. Uploading 10 GB of JSON file into memory takes time. Also, make sure sufficient memory is available. Otherwise, the program crashes.

Now that we have created the inference data, we will run the actual inference. Check the script run_inference.sh in the folder scripts. Make sure the paths are correct. Next run,
bash scripts/run_inference.sh

This script will run main_analysis.py. The inputs to this are the parquet files containing the distribution. In the current version, the file can be accessed via "cs224c_project/data/distribution/distribution.parquet". The other input file is the location to the folder containing inference data obtained from step 3. The program will automatically loop through the files in the folder and use the relevant parquet files to estimate alpha. The final output is saved to output/{subject_name}_{year}.csv

The aforementioned approach is more general, as it applies to articles from any field. For the report, we focused on articles related to education research. To reproduce some of the results, you can run the following Jupyter notebooks:
  a. prepare_data.ipynb
  b. reproduce_results.ipynb
  c. validation.ipynb
