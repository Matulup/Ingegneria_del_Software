from scacchi.entity.Pezzo import Pezzo


class Pedone(Pezzo) :
    """<<Entity>>.

    Classe che estende il generico pezzo e rappresenta il Pedone.
    - Ha le stesse caratteristiche del pezzo generico.
    - Si può muovere solo in avanti di una casella (eccetto la prima mossa 
        dove ha la possibilità di muoversi di due caselle).
    - Permette di aggiornare il suo stato interno per indicare che ha già effettuato
        la propria prima mossa.
    """

    def __init__(self, colore):
        #input:
        # - colore: colore del pezzo
        # #
        self.prima_mossa = 1

        if colore == "Bianco" :
            icona = "♟"
        else:
            if colore == "Nero":
                icona = "♙"

        super().__init__("Pedone", colore, icona)
    
    def mossa_lecita(self, i_partenza_reale, j_partenza_reale, \
                     i_arrivo_reale, j_arrivo_reale):
        flag = 0

         # Il pedone si muove solo sulla stessa colonna
        if j_partenza_reale == j_arrivo_reale:
            if self.colore == "Bianco" and (i_partenza_reale == (i_arrivo_reale + 1))or\
                    (i_partenza_reale == (i_arrivo_reale + 2) and\
                      self.prima_mossa == 1):
                    flag = 1
                    #self.prima_mossa = 0
                
            else:
                if self.colore == "Nero" and(i_partenza_reale == (i_arrivo_reale - 1))\
                        or(i_partenza_reale == (i_arrivo_reale - 2)\
                            and self.prima_mossa == 1):
                        flag = 1
                        #self.prima_mossa = 0
        return flag
    def cattura_lecita(self, i_partenza_reale, j_partenza_reale, i_arrivo_reale,\
                        j_arrivo_reale):
        flag = 0
        #self.prima_mossa = 0
        if (j_partenza_reale == (j_arrivo_reale-1) or (j_partenza_reale \
                                                       == (j_arrivo_reale+1)) ):
            
            if self.colore == "Bianco":  
                
                flag = 1 if  i_arrivo_reale == (i_partenza_reale-1)  else 0
                    
                    
            else: 
                if self.colore == "Nero":
                    
                     flag=1 if i_arrivo_reale == (i_partenza_reale+1)  else 0
                      
        
                
 
        return flag
    def set_prima_mossa(self):
        self.prima_mossa = 0
