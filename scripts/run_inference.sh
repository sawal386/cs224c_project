#!/bin/bash

source scripts/settings.sh


for sub in "medicine"
do
    for year in 2024
    do
        INFERENCE_OUTPUT_LOC="${OUTPUT_DATA_DIR}/${sub}"
        python main_analysis.py \
            --data_loc ${INFERENCE_OUTPUT_LOC} \
            --subject $sub \
            --year $year \
            --output_loc ${OUTPUT_ANALYSIS_DIR} \
            --dist_path ${DIST_DIR_FULL}
    done
done

    
    
