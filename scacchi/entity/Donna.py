from scacchi.entity.Pezzo import Pezzo


class Donna(Pezzo):
    """<<Entity>>.

    Classe che estende il generico pezzo e rappresenta la Donna.
    - Ha le stesse caratteristiche del pezzo generico.
    """

    def __init__(self, colore):
         #input:
        # - colore: colore del pezzo
        # #
        if colore == "Bianco" :
            icona = "♛"
        else:
            if colore == "Nero":
                icona = "♕"

        super().__init__("Donna", colore, icona)

    def mossa_lecita(self, i_partenza_reale, j_partenza_reale, \
                     i_arrivo_reale, j_arrivo_reale):
        flag = 0

        #se le coordinate sono valide
        if (j_arrivo_reale>=0 and j_arrivo_reale<8) and (j_partenza_reale>=0 \
            and j_partenza_reale<8) and (i_arrivo_reale>=0 and i_arrivo_reale<8) \
            and (i_partenza_reale>=0 and i_partenza_reale<8):

            if not((i_partenza_reale == i_arrivo_reale) and \
                   (j_partenza_reale == j_arrivo_reale)):

                #se si muove sulla stessa riga
                if (i_partenza_reale == i_arrivo_reale) and \
                    (j_arrivo_reale != j_partenza_reale) :
                    flag = 1
                    #print("riga")
                else:
                    #se si muove sulla stessa colonna
                    if(j_partenza_reale == j_arrivo_reale) \
                        and (i_arrivo_reale != i_partenza_reale):
                        flag = 1
                        #print("colonna")
                    else:#se si muove in diagonale
                        copia_riga = i_partenza_reale
                        copia_colonna = j_partenza_reale

                        #se si muove in avanti(riferito al bianco)
                        if i_partenza_reale>i_arrivo_reale: 
                            #se si muove in avanti a destra
                            if j_partenza_reale < j_arrivo_reale: 
                                
                                while (copia_colonna != j_arrivo_reale) and (flag == 0):
                                    
                                    copia_riga = copia_riga - 1
                                    copia_colonna = copia_colonna + 1
                                    if (copia_colonna == j_arrivo_reale) and\
                                          (copia_riga == i_arrivo_reale):
                                        flag = 1

                            else:#se si muove in avanti a sinistra
                                while (copia_colonna != j_arrivo_reale) and (flag == 0):
                                   copia_riga = copia_riga - 1
                                   copia_colonna = copia_colonna - 1
                                   if (copia_colonna == j_arrivo_reale) and\
                                      (copia_riga == i_arrivo_reale):
                                       flag = 1

                        else:#se si muove indietro(riferito al bianco)
                            #se si muove indietro a destra
                            if j_partenza_reale < j_arrivo_reale: 
                               while (copia_colonna != j_arrivo_reale) and (flag == 0):
                                   copia_riga = copia_riga + 1
                                   copia_colonna = copia_colonna + 1
                                   if (copia_colonna == j_arrivo_reale) and\
                                      (copia_riga == i_arrivo_reale):
                                       flag = 1
                               
                            else:#se si muove inidietro a sinistra
                                while (copia_colonna != j_arrivo_reale) and (flag == 0):
                                   copia_riga = copia_riga + 1
                                   copia_colonna = copia_colonna - 1
                                   if (copia_colonna == j_arrivo_reale) and\
                                      (copia_riga == i_arrivo_reale):
                                       flag = 1
                        
            else:
                flag = 0
        else:
            flag = 0

        return flag
    
    def cattura_lecita(self, i_partenza_reale, j_partenza_reale,\
                        i_arrivo_reale, j_arrivo_reale):
        return self.mossa_lecita(i_partenza_reale, j_partenza_reale,\
                                  i_arrivo_reale, j_arrivo_reale)