from abc import abstractmethod


class Pezzo:
    """<<Entity>>.

    Classe che rappresenta un generico pezzo del gioco.
    - Contiene il nome specifico del pezzo e ne consente la lettura. 
    - Contiene il colore (Nero o Bianco) e ne consente la lettura.
    - Contiene l'icona che lo rappresenta e ne consente la lettura.
    - Può effetturare un insieme finito di mosse a seconda del tipo di pezzo.
    """

    def __init__(self, nome, colore, icona): 
        # input:
        # - nome: nome del pezzo
        # - colore: colore del pezzo
        # - icona: icona del pezzo
        # #
        self.nome = nome
        self.colore = colore
        self.icona = icona

    def get_colore(self):
        # output: colore del pezzo ("Bianco" o "Nero")
        # #
        return self.colore
    
    def get_nome(self):
        # output: nome del pezzo ("Pedone" o "Alfiere" o ...)
        # #
        return self.nome
    
    def get_icona(self):
        # output: icona del pezzo
        # #
        return self.icona
    
    @abstractmethod
    def mossa_lecita(self, i_partenza_reale, j_partenza_reale,\
        i_arrivo_reale, j_arrivo_reale):pass
        # Dice se la mossa (definita dalle coordinate reali di partenzae di arrivo)
        # è lecita per lo specifico pezzo
        # input:
        # - i_partenza_reale: ordinata reale(cioè il numero di riga) in cui 
        #     si trova il pezzo 
        # - j_partenza_reale: ascissa reale(cioè il numero di colonna) in cui 
        #     si trova il pezzo
        # - i_arrivo_reale: ordinata reale(cioè il numero di riga) in cui il 
        #     si vuole portare il pezzo 
        # - j_arrivo_reale: ascissa reale(cioè il numero di colonna) in cui il 
        #     si vuole portare il pezzo
        # output:
        #  1) 0 se la mossa non è lecita 
        #  2) 1 se la mossa è lecita
        # #

    @abstractmethod
    def cattura_lecita(self, i_partenza_reale, j_partenza_reale, \
                  i_arrivo_reale, j_arrivo_reale): pass