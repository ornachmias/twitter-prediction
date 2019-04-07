import snappy
import lz4.frame
import zlib
import numpy as np


class CompressionHandler(object):
    def __init__(self):
        # We can use multiple compression algorithms as a feature vector
        self._compression_algorithms = [lz4.frame.compress, snappy.compress, zlib.compress]
        self._compression_baseline = {}
        self._categorized_text = {}

    def initialize(self, categorized_text):
        self._categorized_text = categorized_text
        for k in categorized_text:
            self._compression_baseline[k] = self.get_compression_lengths(categorized_text[k])

    def get_compression_lengths(self, text):
        results = []
        for c in self._compression_algorithms:
            results.append(len(c(text.encode())))
        return np.array(results)

    def find_best_match(self, text):
        distance = {}
        for p in self._categorized_text:
            distance[p] = self.calculate_distance(p, text)

        return min(distance, key=distance.get)

    def calculate_distance(self, party, text):
        results = []
        for c in self._compression_algorithms:
            results.append(len(c((self._categorized_text[party] + text).encode())))

        # Find euclidean distance between the features vector
        return np.linalg.norm(np.array(results) - self._compression_baseline[party])
