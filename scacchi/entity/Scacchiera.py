from .Alfiere import Alfiere
from .Cavallo import Cavallo
from .Donna import Donna
from .Pedone import Pedone
from .Pezzo_Vuoto import Pezzo_Vuoto
from .Re import Re
from .Torre import Torre


class Scacchiera:
    """<<Entity>>.

    Classe che rappresenta la scacchiera.
    - Contiene tutti i pezzi del gioco e consente il semplice spostamento (inteso come 
        spostamento senza controlli di validità) degli stessi sulla scacchiera.
    - Consente di selezionare un pezzo sulla scacchiera.
    - Consente la conversione di coordinate algebriche in coordinate reali
        (ad esempio a-1 diventa 7-0).
    - Consente la conversione di coordinate reali in coordinate algebriche 
        (ad esempio 7-0 diventa a-1).
    - Consente la creazione di nuovi pezzi accessibili all'esterno.
    """
    
    def __init__(self):
        vuoto = Pezzo_Vuoto()
        self.scacchiera = [[Torre("Nero"), Cavallo("Nero"), Alfiere("Nero"), \
                                    Donna("Nero"), Re("Nero"), Alfiere("Nero"),\
                                    Cavallo("Nero"), Torre("Nero")],
                                [Pedone("Nero"), Pedone("Nero"), Pedone("Nero"), \
                                    Pedone("Nero"), Pedone("Nero"), Pedone("Nero"), \
                                    Pedone("Nero"), Pedone("Nero")],
                                [vuoto,vuoto,vuoto,vuoto,vuoto,vuoto,vuoto,vuoto],
                                [vuoto,vuoto,vuoto,vuoto,vuoto,vuoto,vuoto,vuoto],
                                [vuoto,vuoto,vuoto,vuoto,vuoto,vuoto,vuoto,vuoto],
                                [vuoto,vuoto,vuoto,vuoto,vuoto,vuoto,vuoto,vuoto],
                                [Pedone("Bianco"),Pedone("Bianco"),Pedone("Bianco"), \
                                    Pedone("Bianco"),Pedone("Bianco"),Pedone("Bianco"),\
                                    Pedone("Bianco"),Pedone("Bianco")],
                                [Torre("Bianco"),Cavallo("Bianco"),Alfiere("Bianco"), \
                                    Donna("Bianco"),Re("Bianco"),Alfiere("Bianco"), \
                                    Cavallo("Bianco"),Torre("Bianco")]
                                ]


    def sposta_pezzo(self, i_partenza, j_partenza, i_arrivo, j_arrivo):
        # Sposta il pezzo che si trova nelle coordinate specificate 
        # nelle coordinate di destinazione
        # input:
        # - i_partenza: ordinata reale(cioè il numero di riga) in cui si trova il pezzo 
        # - j_partenza: ascissa reale(cioè il numero di colonna) in cui si 
        #     trova il pezzo
        # - i_arrivo: ordinata reale(cioè il numero di riga) in cui il si vuole
        #     portare il pezzo 
        # - j_arrivo: ascissa reale(cioè il numero di colonna) in cui il si vuole 
        #     portare il pezzo 
        # #
        if not(j_partenza == j_arrivo and i_partenza == i_arrivo) and \
            j_partenza>=0 and j_partenza<8 and i_partenza>=0 and i_partenza<8\
                    and j_arrivo>=0 and j_arrivo<8 and i_arrivo>=0 and i_arrivo<8:
                self.scacchiera[i_arrivo][j_arrivo] =\
                     self.scacchiera[i_partenza][j_partenza]
                self.scacchiera[i_partenza][j_partenza] = Pezzo_Vuoto() 
    
    def get_pezzo(self, ordinata_reale, ascissa_reale):
        # Restituisce il pezzo che si trova nell coordinate passate
        # input:
        # - ordinata_reale: ordinata reale(cioè il numero di riga) in 
        #   cui si trova il pezzo 
        # - ascissa_reale: ascissa reale(cioè il numero di colonna) in 
        #   cui si trova il pezzo
        # #
        return self.scacchiera[ordinata_reale][ascissa_reale]
    
    def converti_ordinata_reale(self, i):
        # Restituisce la ordinata reale (cioè il numero di colonna) associato alla 
        # colonna passata espressa nel formato algebrico (esempio: i = 8, return: 0)
        # input:
        # - i: ordinata espressa nel formato algebrico (valori di input in [1,8] )
        # output: ordinata reale 
        # #
        if i>=1 and i<=8:
            return 8 - i
        
    def converti_ascissa_reale(self,j):
        # Restituisce l'ascissa reale (cioè il numero di riga) associato alla riga 
        # passata espressa nel formato algebrico(esempio: j = 'a', return: 0)
        # input:
        # - j: ascissa espressa nel formato algebrico (valori di input in ['a','h'] )
        # output: ascissa reale 
        # #
        if j>='a' and j<='h':
            return ord(j) - ord('a')
        

    def converti_ordinata_algebrica(self, i):
        # Restituisce la ordinata algebrica (cioè il numero di colonna) associato alla 
        # colonna passata (esempio: i = 1, return: 7)
        # #
        if i >=0 and i <= 7:
            return 8 - i
        
    def converti_ascissa_algebrica(self, j):
        # Restituisce l'ascissa algebrica (cioè il numero di riga) associato alla riga 
        # passata espressa nel formato reale (esempio: j = 0, return: 'a')
        # #
        if j >= 0 and j <= 7:
            return chr(ord('a') + j)
    
    
    def set(self, i,j,pezzo):
        self.scacchiera[i][j]=pezzo
    
    def set_vuoto(self,i,j):
        self.scacchiera[i][j]=Pezzo_Vuoto()

    def get_torre(self, colore):
        return Torre(colore)

    def get_alfiere(self, colore):
        return Alfiere(colore)

    def get_cavallo(self, colore):
        return Cavallo(colore)

    def get_Donna(self, colore):
        return Donna(colore)

    def get_re(self, colore):
        return Re(colore)

    def get_pedone(self, colore):
        return Pedone(colore)