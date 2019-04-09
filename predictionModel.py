from batchCompressionHandler import BatchCompressionHandler
from configurations import Configurations
from dataLoader import DataLoader
from popularityHandler import PopularityHandler
from preProcess import PreProcess
from tqdm import tqdm


class PredictionModel(object):
    def __init__(self):
        self._data_loader = DataLoader()
        self._pre_process = PreProcess()

    def _get_data(self):
        categorized_tweets = self._data_loader.get_categorized_tweets()
        uncategorized_tweets = self._data_loader.get_uncategorized_tweets()
        return categorized_tweets, uncategorized_tweets

    def _pre_process_data(self, train_data, test_data):
        categorized_tweets = self._pre_process.pre_process(train_data)
        categorized_tweets = self._pre_process.split_by_language(categorized_tweets)

        hebrew_training_set = categorized_tweets['iw']
        english_training_set = categorized_tweets['en']
        print('Training Set: English={}, Hebrew={}'.format(len(english_training_set), len(hebrew_training_set)))

        uncategorized_tweets = self._pre_process.pre_process(test_data)
        uncategorized_tweets = self._pre_process.split_by_language(uncategorized_tweets)

        hebrew_test_set = uncategorized_tweets['iw']
        english_test_set = uncategorized_tweets['en']
        print('Test Set: English={}, Hebrew={}'.format(len(english_test_set), len(hebrew_test_set)))

        # Training Set: English=155, Hebrew=5848
        # Test Set: English=22663, Hebrew=3386
        # At this point I think I'll skip the English tweets, not enough data to train on
        batched_training_set = self._batch_data(hebrew_training_set)

        training_merged = []
        for p, b in batched_training_set:
            training_merged.append((p, self._pre_process.merge_tweets_text(b)))

        return training_merged, hebrew_test_set

    def _batch_data(self, training_set):
        splitted_training_set = self._pre_process.split_by_party(training_set)
        batched_training_set = []
        for p in splitted_training_set:
            batches = self._pre_process.split_to_batches(splitted_training_set[p], Configurations.batch_size)
            for b in batches:
                batched_training_set.append((p, b))

        return batched_training_set

    def _classify_tweets(self, train_set, test_set):
        compression_handler = BatchCompressionHandler()
        compression_handler.initialize(train_set)
        results = {}
        for t in tqdm(test_set):
            selected_party = compression_handler.find_match(t.text, Configurations.n_value)
            if selected_party not in results:
                results[selected_party] = 0
            results[selected_party] += 1

        return results

    def _aggregate_results(self, tweets_classification, popularity_result, hashtags_results):
        results = {}
        popularity_weight = Configurations.popularity_algo_weight
        hashtags_weight = Configurations.hashtags_algo_weight
        total_votes = sum(tweets_classification.values())
        total_prob = 0
        for r in tweets_classification:
            prob1 = tweets_classification[r] / total_votes
            prob2 = popularity_result[r]
            prob3 = hashtags_results[r]
            joint_prob = ((1 - popularity_weight - hashtags_weight) * prob1) + (popularity_weight * prob2) + (hashtags_weight * prob3)
            total_prob += joint_prob

        for r in tweets_classification:
            prob1 = tweets_classification[r] / total_votes
            prob2 = popularity_result[r]
            prob3 = hashtags_results[r]
            joint_prob = ((1 - popularity_weight - hashtags_weight) * prob1) + (popularity_weight * prob2) + (hashtags_weight * prob3)
            total = joint_prob / total_prob
            results[r] = total

        return results

    def run(self):
        train_data, test_data = self._get_data()
        processed_train_data, processed_test_data = self._pre_process_data(train_data, test_data)

        popularity_handler = PopularityHandler()
        popularity_result = popularity_handler.get_popularity_score(train_data)
        hashtags_dist = popularity_handler.count_hashtags(train_data)

        tweets_classification = self._classify_tweets(processed_train_data, processed_test_data)
        results = self._aggregate_results(tweets_classification, popularity_result, hashtags_dist)
        return results




