import snappy
import lz4.frame
import zlib
import numpy as np


class BatchCompressionHandler(object):
    def __init__(self):
        # We can use multiple compression algorithms as a feature vector
        self._compression_algorithms = [lz4.frame.compress, snappy.compress, zlib.compress]
        self._original_data = []

    def initialize(self, party_text_touples):
        """
        Initialize the class with the training data to be used later to compare to the test data
        :param party_text_touples: Array of tuples (p, t) where p is the party and t is several tweets' text combined
        """

        # Create an in memory array made of (p, t, c) where p is the party, t is the original text made of several
        # tweets and c is the compressed text
        for p, t in party_text_touples:
            self._original_data.append((p, t, self._compress_text(t)))

    def find_match(self, text, n):
        """
        Given a tweet text, this method compress the additional text with each in text in the training set, and
        calculate what are the best n compressions that were made. The party that has the most appearances in this n
        matches is selected and returned.
        This is a variation of the KNN algorithm.
        :param text: A tweet text
        :param n: Number of best n comparisons to take into account
        :return: The party with the most votes within the N comparisons.
        """
        results = []

        # Calculate the difference between the original compression and current compression
        for p, t, d in self._original_data:
            results.append((p, self.calculate_distance(t, text, d)))

        # Sort the result by the difference and take the first n results
        results = sorted(results, key=lambda x: x[1])[:n]

        # Count the parties in the first n results
        count_results = {}
        for r in results:
            if r[0] not in count_results:
                count_results[r[0]] = 0
            count_results[r[0]] += 1

        # Return the party that has the most votes
        return max(count_results, key=count_results.get)

    def _compress_text(self, text):
        """
        Compress a text using the given compression algorithms
        :param text: Text to compress
        :return: An array containing the length of the text after compression using the different compression algorithms
        """
        results = []
        for c in self._compression_algorithms:
            results.append(len(c(text.encode())))

        return results

    def calculate_distance(self, train_text, text, original_compression_length):
        """
        Calculate the euclidean distance between the length of the original compressed text and the current compressed
        text
        :param train_text: The original merged tweets
        :param text: The current tweet's text we want to classify
        :param original_compression_length: The length of the original compression
        :return: The euclidean distance between the size of the original text and the size of the
        original text combined with current text
        """
        results = []
        for c in self._compression_algorithms:
            results.append(len(c((train_text + text).encode())))

        # Find euclidean distance between the features vector
        return np.linalg.norm(np.array(results) - original_compression_length)
