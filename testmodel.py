from model.model import Model

model = Model()
model.buildGraph()
print("Numero Nodi: ", model.get_numNodi())
print("Numero Archi: ", model.get_numArchi())