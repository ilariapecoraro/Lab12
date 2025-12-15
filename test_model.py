from model.model import Model

model = Model()
model.build_weighted_graph(2000)
peso_max = model.get_edges_weight_min_max()
print(peso_max)
num_soglia = model.count_edges_by_threshold(5)
print(num_soglia)
(cammino, peso) = model.search_cammino_minimo(1)