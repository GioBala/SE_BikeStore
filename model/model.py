import copy

import networkx as nx

from database.dao import DAO

class Model:
    def __init__(self):
        self.G=nx.DiGraph()
        self.nodi=[]
        self.map={}
        self.cammino_best=[]
        self.peso_max=0

    def get_date_range(self):
        return DAO.get_date_range()

    def get_categories(self):
        return DAO.get_categorie()

    def crea_grafo(self,categoria,y1,y2):
        self.G=nx.DiGraph()
        self.map={}
        self.nodi=DAO.get_prodotti(categoria)
        self.G.add_nodes_from(self.nodi)
        #print(self.nodi)
        for nodi in self.nodi:
            self.map[nodi.id]=nodi
        ar=DAO.get_nodi(y1,y2,categoria)
        #print(ar)
        #print(self.map)
        for i in range(len(ar)-1):
            for j in range(i+1,len(ar)):
                #print(ar[i][0],ar[j][1])
                if ar[i][1]>ar[j][1]:
                    #print((ar[i][1]+ar[j][1]))
                    self.G.add_edge(self.map[ar[i][0]],self.map[ar[j][0]],weight=(ar[i][1]+ar[j][1]))
                elif ar[i][1]<ar[j][1]:
                    self.G.add_edge(self.map[ar[j][0]], self.map[ar[i][0]], weight=(ar[i][1] + ar[j][1]))
                elif ar[i][1]==ar[j][1]:
                    self.G.add_edge(self.map[ar[j][0]], self.map[ar[i][0]], weight=(ar[i][1] + ar[j][1]))
                    self.G.add_edge(self.map[ar[i][0]], self.map[ar[j][0]], weight=(ar[i][1] + ar[j][1]))
        #print(self.G)
        s=(f"Date selezionate:\n"
           f"Start: {y1}\nEnd: {y2}\n")
        s=s+(f"Grafo creato:\n"
           f"Numero di nodi: {len(self.G.nodes)}\n"
           f"Numero di archi: {len(self.G.edges)}\n")
        return s

    def get_max(self):
        massimi=[]
        for nodi in self.nodi:
            n1=list(self.G.successors(nodi))
            n2=list(self.G.predecessors(nodi))
            #print(n1,n2)
            s1=0
            s2=0
            s3=0
            for i in n1:
                p=self.G.get_edge_data(nodi,i,"weight")
                #print(p)
                s1=s1+p["weight"]

                #s1=s1+p
            for i in n2:
                p=self.G.get_edge_data(i,nodi,"weight")
                #print(p)
                s2=s2+p["weight"]
            s3=s1-s2
            massimi.append([nodi.product_name,s3])

        s="I cinque prodotti più venduti\n"
        c=0
        for i in sorted(massimi,key=lambda x:x[1],reverse=True):
            s=s+f"{i[0]} -> {i[1]}\n"
            c+=1
            if c==5:
                break
        return s

    def get_cammino(self,start,end,lunghezza):
        self.cammino_best = []
        self.peso_max = 0
        s=self.map[int(start)]
        e=self.map[int(end)]
        #print(s)
        self.ricorsione(s,e,int(lunghezza),[],0)
        #print(self.peso_max)
        s="Cammino migliore\n"
        for i in self.cammino_best:
            #p=self.G.get_edge_data(self.cammino_best[i],self.cammino_best[i+1],"weight")
            #pe=p["weight"]
            s=s+f"{i}\n"
        s=s+f"Peso: {self.peso_max}"
        return s



    def ricorsione(self,nodo,end,lunghezza,percorso,peso):
        percorso.append(nodo)
        #print(nodo)
        n=list(self.G.successors(nodo))

        #print(percorso[-2],nodo)
        #print(percorso)
        #p=self.G.get_edge_data(percorso[-2],nodo,"weight")
        #pe=peso+p["weight"]
        if len(percorso)==lunghezza and nodo==end and peso>self.peso_max:
            self.peso_max=peso
            self.cammino_best=copy.deepcopy(percorso)
            return
        if len(percorso)>=lunghezza:
            return
        for i in n:
            if i not in percorso:
                p=self.G.get_edge_data(nodo,i,"weight")
                pe=p["weight"]
                self.ricorsione(i,end,lunghezza,percorso,peso+pe)
                percorso.pop()

    def riempi_dd(self):
        return self.nodi

