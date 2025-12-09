import networkx as nx
from database.dao import DAO
from collections import deque


class Model:
    def __init__(self):
        self.G = nx.Graph()

        # Strutture dati di supporto necessarie
        self._rifugi_list = DAO.get_all_rifugi()
        # Mappa ID -> Rifugio DTO per accedere ai nomi e ai dettagli
        self._rifugi_map = {r.id: r for r in self._rifugi_list}
    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        # TODO
        self.G.clear()
        connessioni = DAO.get_connessioni_fino_a(year)

        if not connessioni:
            # Se non ci sono connessioni, non aggiungere nodi (il grafo rimane vuoto)
            return

        # 1. Aggiungi gli archi. NetworkX aggiunge automaticamente i nodi coinvolti.
        archi_validi = [(conn['id_rifugio1'], conn['id_rifugio2']) for conn in connessioni]
        self.G.add_edges_from(archi_validi)

    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        # TODO
        return [self._rifugi_map[node_id] for node_id in self.G.nodes]
    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        # TODO
        node_id = node.id

        if node_id not in self.G:
            return 0

        # NetworkX restituisce il grado per l'ID del nodo
        return self.G.degree[node_id]

        # 3. Utilizza l'ID per interrogare NetworkX e ottenere il grado
        # NetworkX restituisce il grado per il nodo specificato (il suo ID)
        return self.G.degree[node_id]
        return self.G.degree[node_id]
    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        # TODO
        if self.G.number_of_nodes() == 0:
            return 0
        return nx.number_connected_components(self.G)
    def _get_reachable_bfs_iterative(self, start: int) -> set:
        """ Algoritmo iterativo (BFS) per trovare tutti i nodi raggiungibili. """

        visited = {start}
        queue = deque([start])

        while queue:
            u = queue.popleft()

            # Itera sui vicini (neighbor) di u
            for v in self.G.neighbors(u):
                if v not in visited:
                    visited.add(v)
                    queue.append(v)

        return visited

    def _get_reachable_dfs_nx(self, start: int) -> set:
        """ Metodo NetworkX (DFS) per trovare i nodi raggiungibili. """
        # dfs_tree restituisce l'albero di visita. I nodi nell'albero sono i raggiungibili.
        albero_dfs = nx.dfs_tree(self.G, source=start)
        return set(albero_dfs.nodes)



    def get_reachable(self, start):
        """
        Deve eseguire almeno 2 delle 3 tecniche indicate nella traccia:
        * Metodi NetworkX: `dfs_tree()`, `bfs_tree()`
        * Algoritmo ricorsivo DFS
        * Algoritmo iterativo
        per ottenere l'elenco di rifugi raggiungibili da `start` e deve restituire uno degli elenchi calcolati.
        :param start: nodo di partenza, da non considerare nell'elenco da restituire.

        ESEMPIO
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_iterative(start)
        b = self.get_reachable_recursive(start)

        return a
        """

        # TODO
        # Estraiamo l'ID del nodo di partenza, che è ciò che NetworkX si aspetta.
        # Il parametro 'start' è l'ID intero del rifugio (inviato dal Controller corretto).
        start_node_id = start

        if start_node_id not in self.G:
            return []

        # Esecuzione delle tecniche richieste (passando l'ID intero)

        # 1. Tecnica NetworkX (DFS)
        nodi_raggiungibili_dfs = self._get_reachable_dfs_nx(start_node_id)

        # 2. Tecnica Algoritmo Iterativo (BFS)
        nodi_raggiungibili_iter = self._get_reachable_bfs_iterative(start_node_id)

        # Scelta del risultato
        risultato_ids = nodi_raggiungibili_dfs

        # Conversione in oggetti Rifugio DTO (escludendo il nodo di partenza per coerenza)
        # Nota: La ricerca DFS/BFS include il nodo di partenza, quindi lo escludiamo qui
        risultato_oggetti = [
            self._rifugi_map[node_id]
            for node_id in risultato_ids
            if node_id != start_node_id  # Esclude il nodo di partenza
        ]

        # Ordinamento per nome
        return sorted(risultato_oggetti, key=lambda r: r.nome)