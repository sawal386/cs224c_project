#!/bin/bash

source scripts/settings.sh

# you can add subjects and years. for example,
## for sub in "education" "medicine"
## do
##     for year in 2024
##     do
##           {Rest of the code }

for sub in "education"
do
    for year in 2024
    do
        python main_generate.py \
            --input_loc ${BASE_JSON_DIR} \
            --subject $sub \
            --year $year \
            --output_loc ${OUTPUT_DATA_DIR}
    done
done

    
    
