import flet as ft
from UI.view import View
from model.model import Model

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: Model):
        self._model = model
        self._view = view

        # Variabili per memorizzare le selezioni correnti
        self.biblioteca_selezionata = None
        self.genere_selezionato = None

    # POPOLA DROPDOWN
    def popola_dropdown(self):
        biblioteche = self._model.get_biblioteche()
        #per ogni biblioteca, aggiungo il suo NOME nel menu a tendina
        for b in biblioteche:
            self._view.dd_biblioteca.options.append(ft.dropdown.Option(b.nome))

        generi=self._model.get_generi()
        for g in generi:
            self._view.dd_genere.options.append(ft.dropdown.Option(g))

        self._view.update()


    # CALLBACKS DROPDOWN
    def handle_selezione_biblioteca(self, e):
        scelta = self._view.dd_biblioteca.value
        if scelta == "Nessun filtro":
            self.biblioteca_selezionata = None
        else:
            self.biblioteca_selezionata = scelta

    def handle_selezione_genere(self, e):
        scelta=self._view.dd_genere.value
        if scelta == "Nessun filtro":
            self.genere_selezionato = None
        else:
            self.genere_selezionato = scelta

    # AZIONE: MOSTRA LIBRI
    def handle_mostra_libri(self, e):
        #chiamo i libri filtrati dal modello
        libri=self._model.get_libri_filtrati(self.biblioteca_selezionata, self.genere_selezionato)

        #pulisce la listview grafica dai risultati della ricerca precedente:
        self._view.lista_libri.controls.clear()

        if not libri:
            self._view.show_alert("Nessun libro soddisfa i criteri di filtraggio indicati.")
        else:
            #riempie la lista convertendo ogni DTO Libro in stringa
            for libro in libri:
                self._view.lista_libri.controls.append(ft.Text(str(libro)))

        self._view.update()
