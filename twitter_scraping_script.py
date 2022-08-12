from twarc import Twarc2, expansions
import datetime
import json
import config as cf
import pandas as pd
import os
import urllib
import argparse
import unidecode

# Replace your bearer token below
client = Twarc2(bearer_token=cf.credentials['bearer_token'])

DATA_FOLDER = '/anonymized'

def download(url, folder):
    file_name = os.path.join(folder, url.split('/')[-1])
    urllib.request.urlretrieve(url, file_name)

def scrape_category_images(category, query_words, start_time, end_time, data_path = 'data', country_code = 'CH', max_results = 100):

    category_dir = os.path.join(data_path, category)
    if not os.path.exists(category_dir):
        os.mkdir(category_dir)
    country_code_dir = os.path.join(category_dir, country_code)
    if not os.path.exists(country_code_dir):
        os.mkdir(country_code_dir)

    query = "({}) has:images place_country:{}".format(query_words, country_code)
    print(query)

    # The search_all method call the full-archive search endpoint to get Tweets based on the query, start and end times
    search_results = client.search_all(query=query, start_time=start_time, end_time=end_time, max_results=100)

    i = 0
    all_pages = []
    # Twarc returns all Tweets for the criteria set above, so we page through the results
    for page in search_results:

        result = expansions.flatten(page)
        all_pages = all_pages + result

        for tweet in result:

            if ('attachments' in tweet):
                for media in tweet['attachments']['media']:
                    if "url" in media:
                        download(media['url'], country_code_dir)
            i+=1

    with open(os.path.join(country_code_dir, 'data.json'), 'w') as f:
        json.dump(all_pages, f)

    with open(os.path.join(country_code_dir, 'query.txt'), 'w') as f:
        f.write(query)


def load_categories_from_csv(data_path):
    df = pd.read_csv(data_path)
    categories = df['query_name'].unique()
    return categories


def load_queries(data_path):

    df = pd.read_csv(data_path, encoding='cp1252')
    categories = list(df['english'])
    queries = ['{} OR {} OR {} OR {}'.format(row['english'], row['german'], row['french'], row['italian']) for i, row in df.iterrows()]
    return queries, categories

def load_queries_plural(data_path):

    df = pd.read_csv(data_path, encoding='cp1252')
    categories = list(df['english'])
    queries_singular = ['{} OR {} OR {} OR {}'.format(row['english'], row['german'], row['french'], row['italian']) for i, row in df.iterrows()]
    queries_plural = []
    plural_columns = ['english plural', 'french plural', 'italian plural', 'german plural']
    for i, row in df.iterrows():
        q = ""
        for column in plural_columns:
            if row[column] == row[column]:
                q = q + " OR " + unidecode.unidecode(row[column])
        queries_plural.append(q)
    queries = [singular + plural for singular, plural in zip(queries_singular, queries_plural)]
    return queries, categories


def main():

    # This is where we specify our query as discussed in module 5
    query = '((bread) has:images place_country:CH)',

    category = 'ice cream'

    query_words = 'crème glacée'

    scrape_category_images(category, query_words, start_time, end_time, data_path = 'new_data', country_code = 'CH', max_results = 100)
            

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Twitter data scraping.')

    parser.add_argument('--category', default="all", type=str,
                        help='food category scraping')

    args = parser.parse_args()

    # Specify the start time in UTC for the time period you want Tweets from
    start_time = datetime.datetime(2017, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)

    # Specify the end time in UTC for the time period you want Tweets from
    end_time = datetime.datetime(2020, 12, 31, 0, 0, 0, 0, datetime.timezone.utc)


    twitter_data_folder = os.path.join(DATA_FOLDER, "twitter_extended_plural")

    if (args.category == "all"):

        real_classes_path = os.path.join(DATA_FOLDER, "queries_extended_test.csv")
    
        queries, categories = load_queries_plural(real_classes_path)
        for query, category in zip(queries, categories):
            scrape_category_images(category, query, start_time, end_time, data_path=twitter_data_folder)

    elif (args.category == 'subset'):
        real_classes_path = os.path.join(DATA_FOLDER, "queries_extended_test.csv")
    
        queries, categories = load_queries_plural(real_classes_path)
        cat_list = os.listdir(twitter_data_folder)

        for query, category in zip(queries, categories):
            if category not in cat_list:
                scrape_category_images(category, query, start_time, end_time, data_path=twitter_data_folder)



    else:
        scrape_category_images(args.category, args.category, start_time, end_time, data_path=twitter_data_folder)


    #main()