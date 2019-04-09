class Configurations(object):
    api_key = ''
    api_secret_key = ''
    access_token = ''
    access_token_secret = ''
    data_root = './data'
    historical_days_extraction = 90
    search_keywords = ['בחירות ישראל', '#בחירות2019', 'בחירות 2019',
                       'israel elections', '#IsraelElections2019', '#israelelections', '#israel_elections']
    search_country = ''  # I've decided to give up on the country search, the number of results are too small
    batch_size = 100
    popularity_algo_weight = 0.4
    hashtags_algo_weight = 0  # After running this option I found out that it's just the same as the popularity
    n_value = 20
