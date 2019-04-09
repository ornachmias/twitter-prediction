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
        for p, t in party_text_touples:
            self._original_data.append((p, t, self._compress_text(t)))

    def find_match(self, text, n):
        results = []
        for p, t, d in self._original_data:
            results.append((p, self.calculate_distance(t, text, d)))

        results = sorted(results, key=lambda x: x[1])[:n]
        count_results = {}
        for r in results:
            if r[0] not in count_results:
                count_results[r[0]] = 0
            count_results[r[0]] += 1

        return max(count_results, key=count_results.get)

    def _compress_text(self, text):
        results = []
        for c in self._compression_algorithms:
            results.append(len(c(text.encode())))

        return results

    def calculate_distance(self, train_text, text, original_compression_length):
        results = []
        for c in self._compression_algorithms:
            results.append(len(c((train_text + text).encode())))

        # Find euclidean distance between the features vector
        return np.linalg.norm(np.array(results) - original_compression_length)
