

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        self._idMapFermate = {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f

    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgesPesati()

    def addEdgesPesati(self):
        self._grafo.clear_edges()
        #riutilizzare il principio di funzionamento del metodo addEdges3,
        #ma contando quante volte provo ad aggiungere l'arco
        alledges = DAO.getAllEdges()
        for conn in alledges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]
            #se l'arco esiste aggiungo 1
            if self._grafo.has_edge(u,v):
                self._grafo[u][v]['weight'] += 1
            #se non esiste lo aggiungo e lo inizializzo a 1
            else:
                self._grafo.add_edge(u, v,weight=1)

    def addEdgesPesati2(self):
        #delega il calcolo del peso alla query sql
        self._grafo.clear_edges()
        alledgesWpeso = DAO.getAllEdgesPesati()
        #(id.staz_P,id.staz_A,peso)
        for e in alledgesWpeso:
            u = self._idMapFermate[e[0]]
            v = self._idMapFermate[e[1]]
            peso = e[2]
            self._grafo.add_edge(u,v,weight = peso)

    def getArchiPesoMaggiore(self):
        edges = self._grafo.edges(data=True)        #se metto data = True mi salva anche il peso associato

        edgesMaggiore = []
        for e in edges:
            if self._grafo.get_edge_data(e[0],e[1])["weight"]>1:
                #self._grafo[e[0]][e[1]]['weight']
                edgesMaggiore.append(e)
        return edgesMaggiore


    def buildGraph(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)

        self.addedges3()

    def addedges(self):
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasconn(u,v):
                    self._grafo.add_edge(u,v)

    def addedges2(self):
        for u in self._fermate:
            for conn in DAO.getvicini(u):
                v = self._idMapFermate[conn.id_stazA]
                self._grafo.add_edge(u,v)

    def addedges3(self):
        self._grafo.clear_edges()
        alledges = DAO.getAllEdges()
        for conn in alledges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]
            self._grafo.add_edge(u,v)


    def getBFSNodesFromEdges(self,source):
        archi = nx.bfs_edges(self._grafo,source)
        nodiBFS = []
        for u,v in archi:
            nodiBFS.append(v)
        return nodiBFS

    def getDFSNodesFromEdges(self,source):
        archi = nx.dfs_edges(self._grafo,source)
        nodiDFS = []
        for u,v in archi:
            nodiDFS.append(v)
        return nodiDFS

    def getBFSNodesFromTree(self,source):
        tree = nx.bfs_tree(self._grafo,source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi

    def getDFSNodesFromTree(self,source):
        tree = nx.dfs_tree(self._grafo,source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi





    def get_numNodi(self):
        return len(self._grafo.nodes)

    def get_numArchi(self):
        return len(self._grafo.edges)



    @property
    def fermate(self):
        return self._fermate