import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self, e):
        store=self._view._ddStore.value
        if store is None:
            self._view.txt_result.controls.append(ft.Text("Inserire un negozio",color="red"))
            self._view.update_page()
            return
        self._view.txt_result.clean()

        k=self._view._txtIntK.value
        if k is None:
            self._view.txt_result.controls.append(ft.Text("Inserire un numero max di giorni", color="red"))
            self._view.update_page()
            return
        self._view.txt_result.clean()

        try :
            intK=int(k)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Inserire un valore numerico", color="red"))
            self._view.update_page()
            return
        self._view.txt_result.clean()
        if intK <= 0 :
            self._view.txt_result.controls.append(ft.Text("Inserire un valore numerico maggiore di 0", color="red"))
            self._view.update_page()
            return
        self._view.txt_result.clean()

        self._model.buildGraph(store, intK)
        nodi,archi=self._model.graphDetails()

        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"N nodi : {nodi} - n archi : {archi}"))


        topFive=self._model.getTopFive()
        self._view.txt_result.controls.append(ft.Text("5 archi di peso maggiore : "))
        for n1,n2,weight in topFive :
            self._view.txt_result.controls.append(ft.Text(f"Arco : {n1.order_id} -> {n2.order_id}  - Peso : {weight["weight"]} "))






        self._view.update_page()

    def handleCerca(self, e):
        pass



    def handleRicorsione(self, e):
        pass

    def fillDDStores(self):
        store = self._model.getStore()

        for s in store :
            self._view._ddStore.options.append(ft.dropdown.Option(key=s[0], text=s[1]))

        self._view.update_page()




