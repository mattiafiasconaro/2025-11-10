from model.model import Model

myModel=Model()

myModel.buildGraph(1,5)
nodi,archi=myModel.graphDetails()
print(nodi,archi)

