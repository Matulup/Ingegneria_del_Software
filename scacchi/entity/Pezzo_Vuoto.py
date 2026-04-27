from scacchi.entity.Pezzo import Pezzo


class Pezzo_Vuoto(Pezzo):
    """<<Entity>>.

    Classe che estende il generico pezzo e rappresenta un pezzo vuoto 
    (usato per rappresentare la casella vuota all'interno della scacchiera).
    - Ha le stesse caratteristiche del pezzo generico.
    """

    def __init__(self):
        super().__init__("Vuoto", " ", " ")