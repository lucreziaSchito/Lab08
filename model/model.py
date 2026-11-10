from database.distributore_DAO import DistributoreDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789)
        """
        # TODO
        self.lista_dist_avg = []
        for distributore in self._distributori:
            prezzi_per_mese = [] # svuoto la lista ogni volta che passo ad un nuovo distributore
            distributore.get_prezzi()
            for prezzo in distributore.lista_prezzi :
                if prezzo.data.month == mese: # controllo sul mese, data è un oggetto di tipo datetime.date con attributo month
                    prezzi_per_mese.append(float(prezzo.prezzo_litro))         #che restituisce un intero in base al mese corrispondente
            prezzo_medio = sum(prezzi_per_mese) / len(prezzi_per_mese)
            self.lista_dist_avg.append((distributore.nome, prezzo_medio))
        return self.lista_dist_avg

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """
        # TODO
        '''if giorno == 7 :
            return sequenza_parziale
        else :
            comparazione = []
            for distributore in self._distributori:
                prez_litro = prezzi_settimana[distributore.id][giorno-1]
                if ultimo_distributore == distributore.id or ultimo_distributore is None:
                    costo = float(prez_litro)*100
                else :
                    costo = 5 + float(prez_litro)*100
                comparazione.append((distributore.id, costo))
            prezzo_migliore = min(comparazione, key=lambda x: x[1])
            ultimo_distributore = prezzo_migliore[0]
            sequenza_parziale.append(ultimo_distributore)
            giorno += 1
            costo_corrente += prezzo_migliore[1]
            return self.__ricorsione(sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana)'''
        # prima idea di ricorsione con backtracking : ancora da spiegare !


    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        # TODO
        self.dict_prima_settimana = {}
        for distributore in self._distributori:
            prezzi_prima_settimna = []
            distributore.get_prezzi()
            for prezzo in distributore.lista_prezzi:
                if prezzo.data.month == mese and prezzo.data.day in (1, 2, 3, 4, 5, 6, 7):
                    prezzi_prima_settimna.append((float(prezzo.prezzo_litro)))
            self.dict_prima_settimana[distributore.id] = prezzi_prima_settimna
        return self.dict_prima_settimana
