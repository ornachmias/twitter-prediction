from dataLoader import DataLoader

data_loader = DataLoader()
tweets = data_loader.get_categorized_tweets()
print('Number of categorized tweets:{}'.format(len(tweets)))
tweets = data_loader.get_uncategorized_tweets()
print('Number of uncategorized tweets:{}'.format(len(tweets)))



