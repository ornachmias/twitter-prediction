class Configurations(object):
    # This class is made so it'll be easier to change the settings inside the algorithms
    # Especially useful when checking the best hyperparameters for the specific data

    api_key = ''
    api_secret_key = ''
    access_token = ''
    access_token_secret = ''
    data_root = './data'
    historical_days_extraction = 90

    # Those are the search queries to be used as the unclassified data
    search_keywords = ['בחירות ישראל', '#בחירות2019', 'בחירות 2019',
                       'israel elections', '#IsraelElections2019', '#israelelections', '#israel_elections']

    # Limit the search on the unclassified data to a specific country
    # I've decided to give up on the country search, the number of results are too small
    search_country = ''

    # Number of tweets that will be merged and compressed together
    batch_size = 100

    # There are 3 algorithms that take a part in the final results, this is the weight of each one
    popularity_algo_weight = 0.4
    hashtags_algo_weight = 0  # After running this option I found out that it's just the same as the popularity

    # Number of comparisons that should be made in the KNN
    n_value = 20
