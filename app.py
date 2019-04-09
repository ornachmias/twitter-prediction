from model.parties import Parties
from predictionModel import PredictionModel
from multiprocessing.pool import ThreadPool


prediction_model = PredictionModel()

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


# for i in range(8):
#     results = prediction_model.run()
#     for p in results:
#         if p not in total_results:
#             total_results[p] = 0
#         total_results[p] += results[p]
#
# for p in total_results:
#     print('Party {} got {:.4f}% votes'.format(p.name, (total_results[p] * 100)/8))

# voting_results = {
#     Parties.BlueAndWhite: 1260,
#     Parties.Kulanu: 237,
#     Parties.Meretz: 482,
#     Parties.Labor: 754,
#     Parties.UnionOfRightWing: 225,
#     Parties.NewRight: 246,
#     Parties.Likud: 169,
#     Parties.Zehut: 5,
#     Parties.Shas: 1,
#     Parties.HadashTaal: 7
# }
#
# popularity_results = {
#     Parties.HadashTaal: 0.02389762405590604,
#     Parties.Meretz: 0.00788987759894752,
#     Parties.UnionOfRightWing: 0.011184043959826539,
#     Parties.Zehut: 0.015602355420385442,
#     Parties.Kulanu: 0.009481101727676671,
#     Parties.UnitedTorah: 0.0002075071769475874,
#     Parties.Likud: 0.37030756784786906,
#     Parties.NewRight: 0.02913513778842919,
#     Parties.Shas: 0.01648328749057575,
#     Parties.Labor: 0.48356591701462665,
#     Parties.BlueAndWhite: 0.03224557991880961
# }
#
# results = prediction_model._aggregate_results(voting_results, popularity_results)
