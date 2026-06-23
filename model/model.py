import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.DiGraph()
        self._store=[]
        self._idMapS={}



    def fillDDStores(self):
        return DAO.getAllStores()


    def buildGraph(self,storeId,k):
        self._graph.clear()
        self._store=DAO.getAllNodes(storeId)
        for i in self._store:
            self._idMapS[i.order_id]=i
        self._graph.add_nodes_from(self._store)

        allEdges=DAO.getAllEdges(storeId,k,self._idMapS)
        for e in allEdges:
            self._graph.add_edge(e.ordine1,e.ordine2,weight=e.peso)


    def dettagliGrafo(self):
        return len(self._graph.nodes),len(self._graph.edges)


    def getTopFive(self):
        listaArchi = list(self._graph.edges(data=True))
        listaArchi.sort(key=lambda x: x[2]["weight"], reverse=True)
        return listaArchi[:5]