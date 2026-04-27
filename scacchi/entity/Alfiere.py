from scacchi.entity.Pezzo import Pezzo


class Alfiere(Pezzo) :
    """<<Entity>>.

    Classe che estende il generico pezzo e rappresenta l'Alfiere.
    - Ha le stesse caratteristiche del pezzo generico.
    """
    
    def __init__(self, colore):
        #input:
        # - colore: colore del pezzo
        # #
        if colore == "Bianco" :
            icona = "♝"
        else:
            if colore == "Nero":
                icona = "♗"

        super().__init__("Alfiere", colore, icona)

    
    
    def mossa_lecita(self, i_partenza_reale, j_partenza_reale,\
        i_arrivo_reale, j_arrivo_reale):
        flag = 0
        if abs(j_arrivo_reale-j_partenza_reale)== abs(i_arrivo_reale-i_partenza_reale):
            flag = 1
        else :
            flag = 0
        return flag
    
    
    def cattura_lecita(self, i_partenza_reale, j_partenza_reale,\
        i_arrivo_reale, j_arrivo_reale):
        return self.mossa_lecita( i_partenza_reale, j_partenza_reale,\
        i_arrivo_reale, j_arrivo_reale)

    