from tqdm import tqdm

from compressionHandler import CompressionHandler
from dataLoader import DataLoader
from popularityHandler import PopularityHandler
from preProcess import PreProcess

data_loader = DataLoader()
pre_process = PreProcess()

categorized_tweets = data_loader.get_categorized_tweets()
uncategorized_tweets = data_loader.get_uncategorized_tweets()

categorized_tweets = pre_process.pre_process(categorized_tweets)
categorized_tweets = pre_process.split_by_language(categorized_tweets)

hebrew_training_set = categorized_tweets['iw']
english_training_set = categorized_tweets['en']
print('Training Set: English={}, Hebrew={}'.format(len(english_training_set), len(hebrew_training_set)))

uncategorized_tweets = pre_process.pre_process(uncategorized_tweets)
uncategorized_tweets = pre_process.split_by_language(uncategorized_tweets)

hebrew_test_set = uncategorized_tweets['iw']
english_test_set = uncategorized_tweets['en']
print('Test Set: English={}, Hebrew={}'.format(len(english_test_set), len(hebrew_test_set)))

# Training Set: English=155, Hebrew=5848
# Test Set: English=22663, Hebrew=3386
# At this point I think I'll skip the English tweets, not enough data to train on

splitted_training_set = pre_process.split_by_party(hebrew_training_set)
# batched_training_set = []
# for p in splitted_training_set:
#     batches = pre_process.split_to_batches(splitted_training_set[p], 100)
#     for b in batches:
#         batched_training_set.append((p, b))
#
# training_merged = []
# for p, b in batched_training_set:
#     training_merged.append((p, pre_process.merge_tweets_text(b)))

for p in splitted_training_set:
    merged_text = pre_process.merge_tweets_text(splitted_training_set[p])
    print('Party {} has {} tweets with total length of {}'.format(p, len(splitted_training_set[p]), len(merged_text)))
    splitted_training_set[p] = merged_text

popularityHandler = PopularityHandler()
popularityResult = popularityHandler.get_popularity_score(hebrew_training_set)

compression_handler = CompressionHandler()
compression_handler.initialize(splitted_training_set)


results = {}
for t in tqdm(hebrew_test_set):
    selected_party = compression_handler.find_best_match(t.text)
    if selected_party not in results:
        results[selected_party] = 0
    results[selected_party] += 1

total_votes = sum(results.values())

for r in results:
    print('Party={} got {}%'.format(r, (results[r]/total_votes)*100))
