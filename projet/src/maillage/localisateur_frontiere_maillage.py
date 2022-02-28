class LocalisateurFrontiereMaillage:

    def __init__(self, maillage):
        self.maillage = maillage

    def ajouter_edge(self, noeud1, noeud2):

        edges_index = len(self.edges)

        self.edges.append([noeud1, noeud2])
        self.next.append(-1)

        previous = self.first[noeud1]
        self.first[noeud1] = edges_index
        self.next[edges_index] = previous

    def trouver_aretes(self):

        self.edges = []
        self.first = [-1] * len(self.maillage.noeuds)
        self.next = []

        for element in self.maillage.elements:
            element = sorted(element)
            self.ajouter_edge(element[0], element[1])
            self.ajouter_edge(element[0], element[2])
            self.ajouter_edge(element[1], element[2])

        return self.edges

    def ajouter_edge_sans_doublon(self, noeud1, noeud2):

        edges_index = len(self.edges)

        self.edges.append([noeud1, noeud2, False])
        self.next.append(-1)

        previous = self.first[noeud1]
        self.first[noeud1] = edges_index
        self.next[edges_index] = previous

        following = edges_index

        while previous != -1 and noeud2 <= self.edges[previous][1]:

            if noeud2 == self.edges[previous][1]:
                self.edges[previous][2] = True
                self.edges[following][2] = True

            last_edge = self.edges[previous]
            self.edges[previous] = self.edges[following]
            self.edges[following] = last_edge

            following = previous
            previous = self.next[previous]

    def trouver_aretes_avec_type(self):

        self.edges = []
        self.first = [-1] * len(self.maillage.noeuds)
        self.next = []

        for element in self.maillage.elements:

            element = sorted(element)

            self.ajouter_edge_sans_doublon(element[0], element[1])
            self.ajouter_edge_sans_doublon(element[0], element[2])
            self.ajouter_edge_sans_doublon(element[1], element[2])

        return self.edges

    def trouver_aretes_du_bord(self):
        aretes = self.trouver_aretes_avec_type()
        aretes_du_bord = filter(lambda arete: arete[2] == False, aretes)
        return list(map(lambda arete: [arete[0], arete[1]], aretes_du_bord))
