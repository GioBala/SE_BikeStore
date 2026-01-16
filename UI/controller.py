from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO
        c=self._view.dd_category.value
        y1=self._view.dp1.value
        y2=self._view.dp2.value
        #print(y1,y2)
        s=self._model.crea_grafo(c,y1,y2)
        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(ft.Text(s))
        self._view.update()

    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        # TODO
        s=self._model.get_max()
        self._view.txt_risultato.controls.append(ft.Text(s))
        self._view.dd_prodotto_iniziale.options = [ft.dropdown.Option(key=i.id, text=i.product_name) for i in
                                                   self._model.riempi_dd()]
        self._view.dd_prodotto_finale.options = [ft.dropdown.Option(key=i.id, text=i.product_name) for i in
                                                   self._model.riempi_dd()]
        self._view.update()

    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
        try:
            s1=self._view.dd_prodotto_iniziale.value
            s2=self._view.dd_prodotto_finale.value
            s3=int(self._view.txt_lunghezza_cammino.value)
            s=self._model.get_cammino(s1,s2,s3)
            self._view.txt_risultato.controls.clear()
            self._view.txt_risultato.controls.append(ft.Text(s))
            self._view.update()
        except Exception:
            self._view.show_alert("inserisci valori correttamente")

    def riempi(self):
        return self._model.get_categories()