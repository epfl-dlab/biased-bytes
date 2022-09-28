# biased-bytes
Code and data for:

Kristina Gligorić, Irena Ðorđević, and Robert West. 2022. Biased Bytes: On the Validity of Estimating Food
Consumption from Digital Traces. Proc. ACM Hum.-Comput. Interact. 6, CSCW2, Article 497 (November 2022),
27 pages. https://doi.org/10.1145/3555660.


### Code
The code is placed in the "code" folder. Code is organized into steps_1 to 6, which allow reproducing results. Twitter image data collection can be reproduced by running twitter_scraping_script.py.


### Data
Data is placed in the "data" folder. It has the following structure:

* **crowdsourced_annotation_input**: For each food type, contains input for Amazon Mechanical Turk experiments, including the IDs of compared images.
      
* **crowdsourced_annotation_output**: For each food type, contains results from Amazon Mechanical Turk experiments, including outcomes of pairwise comparisons and provided justifications.
      
* **aggregated_dataframes**: Contains two aggregated dataframes that allow reproducing the analysis and visualization code: df_results_images.pickle and df_results.pickle

* **twitter_dataset**: It contains the queries necessary to reproduce the data collection, raw dataset of tweets, and IDs of Twitter food images after manual and automated annotation.
    
       twitter_queries.csv: Category names necessary to reproduce the data collection
      
       dataset.csv: The raw dataset of collected tweets, including the tweet and user ID, which can be used to download the Twitter images themselves
      
       manual_and_automated_annotation.csv: Dataset of collected tweets after manual and automated annotation
            
MyFoodRepo images can be downloaded directly from the challenge website (https://www.aicrowd.com/challenges/food-recognition-challenge). It is necessary to log in, accept the Terms and conditions, and download the train-v0.4.tar.gz (1.16G) file: https://www.aicrowd.com/challenges/food-recognition-challenge/dataset_files.
