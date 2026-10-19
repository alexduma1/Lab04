import csv


class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.stand_assegnato = None

    def __str__(self):
        if self.stand_assegnato is not None:
            return f"{self.codice}: {self.nome} {self.cognome} - Stand: {self.stand_assegnato.codice}"
        return f"{self.codice}: {self.nome} {self.cognome} - Nessuno stand"

    def __eq__(self, other):
        if isinstance(other, Espositore):
            return self.codice == other.codice
        return False


class Stand:
    def __init__(self, codice, mq, padiglione, prezzo_base):
        self.codice = codice
        self.mq = int(mq)
        self.padiglione = int(padiglione)
        self.prezzo_base = float(prezzo_base)
        self.espositore = None

    def calcola_prezzo(self):
        return self.prezzo_base

    def __str__(self):
        stato = "Disponibile" if self.espositore is None else "Occupato"
        return f"{self.codice}: Standard | {self.mq} mq - Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - {stato}"

    def __eq__(self, other):
        if isinstance(other, Stand):
            return self.codice == other.codice
        return False

    def __lt__(self, other):
        return self.calcola_prezzo() < other.calcola_prezzo()


class StandPrese(Stand):
    def __init__(self, codice, mq, padiglione, prezzo_base, prese):
        super().__init__(codice, mq, padiglione, prezzo_base)
        self.prese = int(prese)

    def calcola_prezzo(self):
        return self.prezzo_base * (1 + 0.07 * self.prese)

    def __str__(self):
        stato = "Disponibile" if self.espositore is None else "Occupato"
        return f"{self.codice}: Prese Extra | {self.mq} mq - Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - Prese aggiuntive: {self.prese} - {stato}"


class StandPremium(Stand):
    def __init__(self, codice, mq, padiglione, prezzo_base, posizione):
        super().__init__(codice, mq, padiglione, prezzo_base)
        self.posizione = posizione

    def calcola_prezzo(self):
        return self.prezzo_base * 1.30

    def __str__(self):
        stato = "Disponibile" if self.espositore is None else "Occupato"
        return f"{self.codice}: Premium | {self.mq} mq - Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - Posizione: {self.posizione} - {stato}"


class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self._nome = nome
        self.dizionario_stand = {}
        self.dizionario_espositori = {}

    """Aggiungere setter e getter se necessari"""

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nuovo_nome):
        self._nome = nuovo_nome

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lettore = csv.reader(f)
                for riga in lettore:
                    if len(riga) == 3:
                        nuovo_espositore = Espositore(riga[0], riga[1], riga[2])
                        self.dizionario_espositori[nuovo_espositore.codice] = nuovo_espositore

                    elif len(riga) == 4:
                        nuovo_stand = Stand(riga[0], riga[1], riga[2], riga[3])
                        self.dizionario_stand[nuovo_stand.codice] = nuovo_stand

                    elif len(riga) == 5:
                        try:
                            numero_prese = int(riga[4])
                            nuovo_stand = StandPrese(riga[0], riga[1], riga[2], riga[3], numero_prese)
                        except ValueError:
                            posizione = riga[4]
                            nuovo_stand = StandPremium(riga[0], riga[1], riga[2], riga[3], posizione)

                        self.dizionario_stand[nuovo_stand.codice] = nuovo_stand

        except FileNotFoundError:
            raise FileNotFoundError()

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        if codice_stand not in self.dizionario_stand:
            raise Exception("Stand non trovato nel sistema.")

        if codice_espositore not in self.dizionario_espositori:
            raise Exception("Espositore non trovato nel sistema.")

        stand_selezionato = self.dizionario_stand[codice_stand]
        espositore_selezionato = self.dizionario_espositori[codice_espositore]

        if stand_selezionato.espositore is not None:
            raise Exception("Lo stand è già stato assegnato a un altro espositore.")

        if espositore_selezionato.stand_assegnato is not None:
            raise Exception("Questo espositore ha già uno stand.")

        stand_selezionato.espositore = espositore_selezionato
        espositore_selezionato.stand_assegnato = stand_selezionato

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        for espositore in self.dizionario_espositori.values():
            print(espositore)

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        lista_di_tutti_gli_stand = list(self.dizionario_stand.values())
        lista_di_tutti_gli_stand.sort()
        return lista_di_tutti_gli_stand
