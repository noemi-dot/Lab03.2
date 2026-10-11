from operator import attrgetter

#creo una nuova classe per gli strumenti
class Strumento:
    def __init__(self, id_strumento, tipo, marca, anno_acquisto, valore):
        self.id_strumento = id_strumento
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = anno_acquisto
        self.valore = valore

    def __str__(self):
        return (f"{self.id_strumento}: {self.tipo} {self.marca} (acquistato nel {self.anno_acquisto}, valore {self.valore:.2f} €)")

    def __repr__(self):
        return (f"Strumento({self.id_strumento!r}, {self.tipo!r}, {self.marca!r}, {self.anno_acquisto!r}, {self.valore!r})")

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        # TODO
        self._nome = nome
        self._responsabile = responsabile
        self._strumenti = []  # lista di Strumento
        self._prestiti = {}  # dizionario dei prestiti attivi, con chiave id_prestito
        self._contatore_prestiti = 0  # per generare P1, P2, ...
        # --- getter / setter ---
        @property
        def nome(self):
            return self._nome

        @property
        def responsabile(self):
            return self._responsabile

        @responsabile.setter
        def responsabile(self, nuovo_responsabile):
            self._responsabile = nuovo_responsabile


    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        # TODO
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for riga in f:
                    riga = riga.strip()
                    if not riga:
                        continue
                    id_s, tipo, marca, anno, valore = riga.split(",")
                    self._strumenti.append(
                        Strumento(id_s, tipo, marca, int(anno), float(valore)))
        except FileNotFoundError:
            return None

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        # TODO
        ultimo = 0
        for s in self._strumenti:
            ultimo = max(ultimo, int(s.id_strumento[1:]))  #per capire che codice inserire. tolgo la S per vedere solo il numero
        nuovo = Strumento(f"S{ultimo + 1}", tipo, marca, anno_acquisto, valore)
        self._strumenti.append(nuovo)
        return nuovo

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        # TODO
        return sorted(self._strumenti, key=attrgetter("marca"))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        # TODO
        trovato = False
        for s in self._strumenti:
            if s.id_strumento == id_strumento:
                trovato = True
        if not trovato:
            raise Exception("lo strumento non esiste")
        for p in self._prestiti.values():
            if p["id_strumento"] == id_strumento:
                raise Exception ("lo strumento è già in prestito")
        #vuol dire che adesso posso effettuare il prestito, quindi aumento il contatore

        self._contatore_prestiti += 1
        id_prestito = f"P{self._contatore_prestiti}"
        prestito = {
            "id_prestito": id_prestito,
            "data": str(data),
            "id_strumento": id_strumento,
            "cognome_allievo": cognome_allievo,
        }
        self._prestiti[id_prestito] = prestito
        return prestito


    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        # TODO
        if id_prestito not in self._prestiti:
            raise Exception("Il prestito non esiste")
        else:
            self._prestiti[id_prestito]
