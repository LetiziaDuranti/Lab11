import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self._current_rifugio = None

    def handle_calcola(self, e):
        """Callback per il bottone 'Calcola sentieri'."""

        year = self._view.txt_anno.value
        try:
            year_n = int(year)
        except (ValueError, TypeError):
            self._view.show_alert("Inserisci un valore numerico nel campo anno.")
            return

        if year_n < 1950 or year_n > 2024:
            self._view.show_alert("Inserisci un valore compreso tra 1950 e 2024.")
            return

        # Costruisce il grafo con il model
        self._model.build_graph(year_n)

        # Aggiorna l'area risultati
        self._view.lista_visualizzazione.controls.clear()

        # Uso il metodo corretto per il numero di componenti
        num_cc = self._model.get_num_connected_components()
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Il grafo ha {num_cc} componenti connesse.", weight=ft.FontWeight.BOLD))  # Aggiunto BOLD
        self._view.lista_visualizzazione.controls.append(ft.Text("Di seguito il dettaglio sui nodi:"))

        # 1. Recupera la lista di oggetti Rifugio DTO e ordina per nome
        rifugi_nel_grafo = self._model.get_nodes()
        rifugi_ordinati = sorted(rifugi_nel_grafo, key=lambda r: r.nome)

        # 2. Ciclo con ENUMERATE per ottenere la numerazione [i] e formattazione esatta
        for i, rifugio_dto in enumerate(rifugi_ordinati, 1):
            # n (che ho rinominato in rifugio_dto) è un oggetto rifugio.
            # get_num_neighbors è stato corretto per accettare il DTO.
            grado = self._model.get_num_neighbors(rifugio_dto)

            # La stringa "Rifugio Nome (Localita)" è gestita da rifugio_dto.__str__ o costruita qui
            # Assumendo che il DTO sia stato modificato per stampare solo Nome (Località):
            nome_completo_stringa = str(rifugio_dto)

            # Formato Esatto: [i] Rifugio Nome (Località) -- X vicini.
            output_string = (
                f"[{i}] {nome_completo_stringa} -- {grado} vicini."
            )

            self._view.lista_visualizzazione.controls.append(ft.Text(output_string))

        # Abilita dropdown e bottone raggiungibili
        self._view.dd_rifugio.disabled = False
        self._view.pulsante_raggiungibili.disabled = False

        # Riempe il dropdown con i rifugi attuali
        self._fill_dropdown()
        self._view.update()

    def handle_raggiungibili(self, e):
        """Callback per il bottone 'Rifugi raggiungibili'."""

        if self._current_rifugio is None:
            self._view.show_alert("Seleziona prima un rifugio dal menu a tendina.")
            return

            # Passa l'ID al Model (corretto)
        raggiungibili = self._model.get_reachable(self._current_rifugio.id)

        self._view.lista_visualizzazione.controls.clear()

        # Intestazione (Formato Esatto)
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Da '{self._current_rifugio.nome}' è possibile raggiungere a piedi {len(raggiungibili)} rifugi:",
                    weight=ft.FontWeight.BOLD))

        # Elenco dei rifugi raggiungibili: L'output corretto è [ID] Nome (Località)
        for r in raggiungibili:
            # r è un oggetto Rifugio DTO

            # 1. Recupera l'ID del rifugio (che è il numero grande richiesto)
            rifugio_id = r.id

            # 2. Formattazione: Nome (Località)
            nome_completo = f"{r.nome} ({r.localita})"

            # Output Finale: [ID] Nome (Località) (Il Controller precedente aveva problemi con il numero 1)
            # L'ID (r.id) è già presente nella stringa DTO se non hai modificato __str__, ma qui lo formattiamo esplicitamente per controllo.

            self._view.lista_visualizzazione.controls.append(ft.Text(f"[{rifugio_id}] {nome_completo}"))

        self._view.update()
    def _fill_dropdown(self):
        """Popola il dropdown con i rifugi presenti nel grafo."""
        self._view.dd_rifugio.options.clear()
        all_rifugi = self._model.get_nodes()

        for r in all_rifugi:
            # Solo text e data: value non serve
            option = ft.dropdown.Option(text=r.nome, data=r)
            self._view.dd_rifugio.options.append(option)

        # aggiorna il dropdown
        self._view.dd_rifugio.update()

        # Associa callback on_change sul Dropdown (non sulle singole Option)
        self._view.dd_rifugio.on_change = self.read_dd_rifugio

    def read_dd_rifugio(self, e):
        """Callback chiamato quando si seleziona un'opzione nel dropdown."""

        selected_option = e.control.value
        if selected_option is None:
            self._current_rifugio = None
            return

        # selected_option è una stringa? in Flet moderno spesso è text, quindi cerchiamo l'oggetto data corrispondente
        found = None
        for opt in e.control.options:
            if opt.text == selected_option:
                found = opt.data
                break

        self._current_rifugio = found
        print("Rifugio selezionato:", self._current_rifugio)
