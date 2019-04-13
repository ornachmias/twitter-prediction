from predictionModel import PredictionModel
from multiprocessing.pool import ThreadPool


prediction_model = PredictionModel()

# Number of iteration we want to run the algorithm on
# We average the results over the number of iteration in order to get more stable results
# Default is set as 1 to simply run it faster
# Note that all of the iteration are ran simultaneously even if the number of CPUs isn't that high,
# this is mostly for convenience, so the percentage of the iteration will be simultaneously.
number_of_iterations = 1
async_results = []
pool = ThreadPool(processes=number_of_iterations)
for i in range(number_of_iterations):
    async_results.append(pool.apply_async(prediction_model.run))

total_results = {}
for i in async_results:
    result = i.get()
    for p in result:
        if p not in total_results:
            total_results[p] = 0
        total_results[p] += result[p]

for p in total_results:
    print('Party {} got {:.4f}% votes'.format(p.name, (total_results[p] * 100)/number_of_iterations))
