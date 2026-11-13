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
        if len(sequenza_parziale) == 7:
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                # eseguo una copia della lista, altrimenti le modifiche successive,tramite pop(),
                # sovrascriveranno anche la sequenza ottima salvata
                self.__sequenza_ottima = list(sequenza_parziale)
            return

        # interrompo l'esplorazione del ramo se il costo parziale ha già superato il costo ottimo attuale
        if self.__costo_ottimo != -1 and costo_corrente >= self.__costo_ottimo:
            return


        for distributore in self._distributori:
            prezzo_litro = prezzi_settimana[distributore.id][giorno - 1]

            costo_giornaliero = float(prezzo_litro) * 100

            if ultimo_distributore is not None and ultimo_distributore != distributore.id:
                costo_giornaliero += 5
            sequenza_parziale.append(distributore.id)

            self.__ricorsione(sequenza_parziale,
                              giorno + 1,
                              distributore.id,
                              costo_corrente + costo_giornaliero,
                              prezzi_settimana)

            # BACKTRACKING
            # finito di esplorare un ramo, rimuovo l'ultimo elemento e passo all'altro ramo possibile: l'altro distributore
            # per poi scegliere quello più conveniente nella prima parte della funzione __ricorsione
            sequenza_parziale.pop()


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
