from scacchi.entity.Pezzo import Pezzo


class Torre(Pezzo) :
    """<<Entity>>.

    Classe che estende il generico pezzo e rappresenta la Torre.
    - Ha le stesse caratteristiche del pezzo generico.
    """
    
    def __init__(self, colore):
        #input:
        # - colore: colore del pezzo
        # #
        self.Prima_mossa=0
        if colore == "Bianco" :
            icona = "♜"
        else:
            if colore == "Nero":
                icona = "♖"
        super().__init__("Torre", colore, icona)
    def mossa_lecita(self, i_partenza_reale, j_partenza_reale, \
                     i_arrivo_reale, j_arrivo_reale):
        flag=0
        #si muove sulla stessa riga
        if((i_partenza_reale==i_arrivo_reale) and ( j_partenza_reale!=\
            j_arrivo_reale)) or ((j_partenza_reale==j_arrivo_reale) \
            and ( i_partenza_reale!=i_arrivo_reale)):
            flag=1
        return flag
     
    def cattura_lecita(self, i_partenza_reale, j_partenza_reale,\
        i_arrivo_reale, j_arrivo_reale):
        return self.mossa_lecita(i_partenza_reale, j_partenza_reale,\
                i_arrivo_reale, j_arrivo_reale)
            
    
    def get_Prima_Mossa(self):
        return self.Prima_mossa
    def set_Prima_Mossa(self):
        self.Prima_mossa=1
    
       
    
       
        