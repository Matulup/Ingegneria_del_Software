from scacchi.entity.Pezzo import Pezzo


class Cavallo(Pezzo):
    """<<Entity>>.

    Classe che estende il generico pezzo e rappresenta il Cavallo.
    - Ha le stesse caratteristiche del pezzo generico.
    """

    def __init__(self, colore):
        #input:
        # - colore: colore del pezzo
        # #
        if colore == "Bianco" :
            icona = "♞"
        else:
            if colore == "Nero":
                icona = "♘"

        super().__init__("Cavallo", colore, icona)

    def mossa_lecita(self, i_partenza_reale, j_partenza_reale,\
        i_arrivo_reale, j_arrivo_reale):
        flag =0
        if (j_arrivo_reale>=0) and (j_arrivo_reale<=7) \
            and (i_arrivo_reale>=0) and (i_arrivo_reale<=7):
            if abs(j_arrivo_reale-j_partenza_reale)==2 \
            and abs(i_arrivo_reale-i_partenza_reale)==1:
                flag = 1
            if abs(j_arrivo_reale-j_partenza_reale)==1 \
                and abs(i_arrivo_reale-i_partenza_reale)==2:
                flag = 1
        else:
            flag=0
        return flag

    def cattura_lecita(self, i_partenza_reale, j_partenza_reale,\
        i_arrivo_reale, j_arrivo_reale):
        return self.mossa_lecita( i_partenza_reale, j_partenza_reale,\
        i_arrivo_reale, j_arrivo_reale)