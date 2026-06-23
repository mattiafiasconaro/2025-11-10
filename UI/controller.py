import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self, e):
        self._view.txt_result.clean()
        idStore = self._view._ddStore.value
        giornoMax= self._view._txtIntK.value
        if idStore is None:
            self._view.txt_result.controls.append(ft.Text("inserire uno store",color="red"))
            self._view.update_page()
            return
        if giornoMax =="":
            self._view.txt_result.controls.append(ft.Text("Inserire un valore numerico", color="red"))
            self._view.update_page()
            return

        try:
            intero = int(giornoMax)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("inserire un valore numerico int", color="red"))
            self._view.update_page()
            return

        if intero <=0:
            self._view.txt_result.controls.append(ft.Text("inserire un valore che sia maggiore di 0 ", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(idStore, giornoMax)
        nodi,archi=self._model.dettagliGrafo()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente eseguito"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi : {nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi : {archi}"))

        for n1,n2,peso in self._model.getTopFive():
            self._view.txt_result.controls.append(ft.Text(f"Arco {n1} -> arco {n2} : {peso["weight"]}"))



        self._view.update_page()



    def handleCerca(self, e):
        pass

    def handleRicorsione(self, e):
        pass

    def fillDDStores(self):
        store= self._model.fillDDStores()
        for s in store:
            self._view._ddStore.options.append(ft.dropdown.Option(text=s[1],key=s[0] ))
        self._view.update_page()



