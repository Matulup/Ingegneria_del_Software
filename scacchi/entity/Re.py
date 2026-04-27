from scacchi.entity.Pezzo import Pezzo


class Re(Pezzo):
    """<<Entity>>.

    Classe che estende il generico pezzo e rappresenta il Re.
    - Ha le stesse caratteristiche del pezzo generico.
    """

    def __init__(self, colore):
        #input:
        # - colore: colore del pezzo
        # #
        self.gia_mosso=0
        if colore == "Bianco" :
            icona = "♚"
        else:
            if colore == "Nero":
                icona = "♔"

        super().__init__("Re", colore, icona)

    def mossa_lecita(self, i_partenza_reale, j_partenza_reale,\
        i_arrivo_reale, j_arrivo_reale):
        flag=0
        if ( abs(i_partenza_reale-i_arrivo_reale)<=1 and \
               abs(j_partenza_reale-j_arrivo_reale)<=1 ) :

            flag=1
            self.gia_mosso=1
        return flag
            

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

    # per la futura cattura
    # def cattura_lecita(self, i_partenza_reale, j_partenza_reale, 
    #              i_arrivo_reale, j_arrivo_reale)

    def cattura_lecita(self, i_partenza_reale, j_partenza_reale,\
        i_arrivo_reale, j_arrivo_reale):
        flag=0
        if ( abs(i_partenza_reale-i_arrivo_reale)<=1 and \
               abs(j_partenza_reale-j_arrivo_reale)<=1 ) :
            

            flag=1
            self.gia_mosso=1
        return flag
    
    def get_mosso(self):
        return self.gia_mosso
    
