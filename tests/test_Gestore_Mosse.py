import pytest

from scacchi.control.Gestore_Mosse import Gestore_Mosse


@pytest.fixture
def gestore():
    """Restituisce un'istanza del Gestore_Mosse per i test."""
    return Gestore_Mosse()

## Test per Usa_Pedone ##
def test_Usa_Pedone(gestore):
    """Verifica che il pedone si muova correttamente o meno durante partita."""
    # Pedone si muove in avanti di 2 (prima mossa)
    assert gestore.Usa_Pedone("e4", "Bianco") == 1
    
    # Pedone si muove in avanti di 1
    gestore.scacchiera.set(3, 4, gestore.scacchiera.get_pedone("Nero"))
    assert gestore.Usa_Pedone("e6", "Nero") == 1
    
    # Cattura valida
    gestore.scacchiera.set(4, 3, gestore.scacchiera.get_pedone("Nero"))
    gestore.scacchiera.set(5, 2, gestore.scacchiera.get_pedone("Bianco"))
    assert gestore.Usa_Pedone("cxd4", "Bianco") == 1

    gestore.scacchiera.set(4, 3, gestore.scacchiera.get_pedone("Nero"))
    gestore.scacchiera.set(5, 2, gestore.scacchiera.get_pedone("Bianco"))
    gestore.scacchiera.set_vuoto(5,0)
    gestore.scacchiera.set_vuoto(5,1)
    gestore.scacchiera.set_vuoto(5,3)
    gestore.scacchiera.set_vuoto(5,4)
    gestore.scacchiera.set_vuoto(5,5)
    gestore.scacchiera.set_vuoto(5,6)
    gestore.scacchiera.set_vuoto(5,7)
    assert gestore.Usa_Pedone("xd4", "Bianco") == 1

    #solo uno di due pedoni può catturare
    gestore.scacchiera.set(4, 3, gestore.scacchiera.get_pedone("Nero"))
    gestore.scacchiera.set(5, 2, gestore.scacchiera.get_pedone("Bianco"))
    gestore.scacchiera.set(5, 4, gestore.scacchiera.get_pedone("Bianco"))
    assert gestore.Usa_Pedone("cxd4", "Bianco") == 1
    
    # Promozione
    gestore.scacchiera.set(1, 0, gestore.scacchiera.get_pedone("Bianco"))
    gestore.scacchiera.set_vuoto(0,0)
    assert gestore.Usa_Pedone("a8=D", "Bianco") == 1

    gestore.scacchiera.set(1, 0, gestore.scacchiera.get_pedone("Bianco"))
    assert gestore.Usa_Pedone("axb8=D", "Bianco") == 1

    #il pedone può fare l'en passant
    gestore.possibile_en_passant = 1
    gestore.colore_en_passant = "Nero"
    gestore.colonna_en_passant = 2
    gestore.riga_en_passant = 3
    gestore.scacchiera.set(3,1,gestore.scacchiera.get_pedone("Bianco"))
    gestore.scacchiera.set(3,2,gestore.scacchiera.get_pedone("Nero"))
    assert gestore.Usa_Pedone("bxc6","Bianco") == 1

    #Solo uno di due pedoni può catturare
    gestore.scacchiera.set(4, 3, gestore.scacchiera.get_pedone("Nero"))
    gestore.scacchiera.set(5, 2, gestore.scacchiera.get_pedone("Bianco"))
    gestore.scacchiera.set(5, 4, gestore.scacchiera.get_pedone("Bianco"))
    assert gestore.Usa_Pedone("xd4", "Bianco") == 2


    


#def test_Usa_pedone(gestore):

    # Mossa nello stesso punto
    assert gestore.Usa_Pedone("e2", "Bianco") == 0

    #Mossa all'indietro
    assert gestore.Usa_Pedone("e1", "Bianco") == 0
    
    # Mossa laterale senza cattura
    gestore.scacchiera.set_vuoto(6,0)
    gestore.scacchiera.set_vuoto(6,1)
    gestore.scacchiera.set_vuoto(6,3)
    gestore.scacchiera.set_vuoto(6,4)
    gestore.scacchiera.set_vuoto(6,5)
    gestore.scacchiera.set_vuoto(6,6)
    gestore.scacchiera.set_vuoto(6,7)
    gestore.scacchiera.set_vuoto(6,2)
    gestore.scacchiera.set(6, 2, gestore.scacchiera.get_pedone("Bianco"))
    assert gestore.Usa_Pedone("d4", "Bianco") == 0
    
    #Non può catturare sulla stessa riga o colonna dove si trova
    gestore.scacchiera.set_vuoto(6,0)
    gestore.scacchiera.set_vuoto(6,1)
    gestore.scacchiera.set_vuoto(6,3)
    gestore.scacchiera.set_vuoto(6,4)
    gestore.scacchiera.set_vuoto(6,5)
    gestore.scacchiera.set_vuoto(6,6)
    gestore.scacchiera.set_vuoto(6,7)
    gestore.scacchiera.set_vuoto(6,2)
    gestore.scacchiera.set(6, 2, gestore.scacchiera.get_pedone("Bianco"))
    gestore.scacchiera.set(5, 2, gestore.scacchiera.get_pedone("Bianco"))
    assert gestore.Usa_Pedone("xc3", "Bianco") == 0

    gestore.scacchiera.set_vuoto(6,0)
    gestore.scacchiera.set_vuoto(6,1)
    gestore.scacchiera.set_vuoto(6,3)
    gestore.scacchiera.set_vuoto(6,4)
    gestore.scacchiera.set_vuoto(6,5)
    gestore.scacchiera.set_vuoto(6,6)
    gestore.scacchiera.set_vuoto(6,7)
    gestore.scacchiera.set_vuoto(6,2)
    gestore.scacchiera.set(6, 2, gestore.scacchiera.get_pedone("Bianco"))
    gestore.scacchiera.set(6, 3, gestore.scacchiera.get_pedone("Bianco"))
    assert gestore.Usa_Pedone("xc3", "Bianco") == 0

    # Cattura su casella vuota
    assert gestore.Usa_Pedone("cxd3", "Bianco") == 0

    #Non sempre si può fare l'en passant
    gestore.possibile_en_passant = 0
    gestore.colore_en_passant = "Nero"
    gestore.colonna_en_passant = 2
    gestore.riga_en_passant = 3
    gestore.scacchiera.set(3,1,gestore.scacchiera.get_pedone("Bianco"))
    gestore.scacchiera.set(3,2,gestore.scacchiera.get_pedone("Nero"))
    assert gestore.Usa_Pedone("bxc6","Bianco") == 0
    
    # Promozione non su ultima riga
    assert gestore.Usa_Pedone("c3=D", "Bianco") == 0

## Test per Usa_Torre ##
def test_usa_torre(gestore):
    """Test casi validi per le mosse della torre."""
    gestore.scacchiera.set(0, 0, gestore.scacchiera.get_torre("Bianco"))
    
    # Movimento verticale
    gestore.scacchiera.set_vuoto(6,0)
    assert gestore.Usa_Torre("Ta4", "Bianco") == 1
    
    # Movimento orizzontale

    gestore.scacchiera.set(4, 4, gestore.scacchiera.get_torre("Bianco"))
    assert gestore.Usa_Torre("Te6", "Bianco") == 1
    
    # Cattura valida
    gestore.scacchiera.set(4, 4, gestore.scacchiera.get_torre("Bianco"))
    gestore.scacchiera.set(4, 7, gestore.scacchiera.get_pedone("Nero"))
    assert gestore.Usa_Torre("Txh4", "Bianco") == 1

#def test_Usa_torre_casi_negativi(gestore):
    """Test casi non validi per le mosse della torre."""
    # Mossa diagonale
    assert gestore.Usa_Torre("Tb2", "Bianco") == 0
    
    # Salto sopra pezzi
    gestore.scacchiera.set(0, 0, gestore.scacchiera.get_torre("Bianco"))
    gestore.scacchiera.set(0, 1, gestore.scacchiera.get_pedone("Bianco"))
    assert gestore.Usa_Torre("Ta4", "Bianco") == 0
    
    # Cattura pezzo dello stesso colore
    gestore.scacchiera.set(4, 7, gestore.scacchiera.get_pedone("Bianco"))
    assert gestore.Usa_Torre("Txh5", "Bianco") == 0

## Test per Usa_Alfiere ##
def test_Usa_alfiere(gestore):
    """Test casi validi per le mosse dell'alfiere."""
    gestore.scacchiera.set(2, 2, gestore.scacchiera.get_alfiere("Bianco"))

    # Cattura valida
    gestore.scacchiera.set(5, 5, gestore.scacchiera.get_pedone("Nero"))
    assert gestore.Usa_Alfiere("Axd7", "Bianco") == 1

    # Movimento diagonale
    gestore.scacchiera.set(2, 2, gestore.scacchiera.get_alfiere("Bianco"))
    gestore.scacchiera.set_vuoto(3,1)
    assert gestore.Usa_Alfiere("Ad5", "Bianco") == 1

def test_usa_alfiere_casi_negativi(gestore):
    """Test casi non validi per le mosse dell'alfiere."""
    # Mossa dritta
    gestore.scacchiera.set_vuoto(2,2)
    gestore.scacchiera.set_vuoto(5,5)
    gestore.scacchiera.set(3, 1, gestore.scacchiera.get_pedone("Nero"))
    assert gestore.Usa_Alfiere("Ac6", "Bianco") == 0
    
    # Salto sopra pezzi
    gestore.scacchiera.set(3, 3, gestore.scacchiera.get_pedone("Bianco"))
    assert gestore.Usa_Alfiere("Af4", "Bianco") == 0
    
    # Cattura pezzo dello stesso colore
    gestore.scacchiera.set(5, 5, gestore.scacchiera.get_pedone("Bianco"))
    assert gestore.Usa_Alfiere("Axf6", "Bianco") == 0

## Test per Usa_Cavallo ##
def test_usa_cavallo(gestore):
    """Test casi validi per le mosse del cavallo."""
    #gestore.scacchiera.set(1, 1, gestore.scacchiera.get_cavallo("Bianco"))
    
    # Movimento a L
    assert gestore.Usa_Cavallo("Cc3", "Bianco") == 1
    
    # Cattura valida
    gestore.scacchiera.set(5, 2, gestore.scacchiera.get_pedone("Nero"))
    assert gestore.Usa_Cavallo("Cxc3", "Bianco") == 1

    #Due cavalli dello stesso tipo possono catturare insieme purchè sia specificata la \
    # colonna di partenza
    gestore.scacchiera.set(7,3,gestore.scacchiera.get_cavallo("Bianco"))
    assert gestore.Usa_Cavallo("Cdxc3", "Bianco") == 1

    #Due cavalli dello stesso tipo possono catturare insieme purchè sia specificata la \
    # riga di partenza
    gestore.scacchiera.set(6,2,gestore.scacchiera.get_cavallo("Bianco"))
    gestore.scacchiera.set(5,3,gestore.scacchiera.get_cavallo("Bianco"))
    gestore.scacchiera.set(4,4,gestore.scacchiera.get_pedone("Nero"))
    assert gestore.Usa_Cavallo("C2xc3", "Bianco") == 1


#def test_usa_cavallo_casi_negativi(gestore):
    """Test casi non validi per le mosse del cavallo."""
    # Mossa non a L
    assert gestore.Usa_Cavallo("Cb3", "Bianco") == 0
    
    # Cattura pezzo dello stesso colore
    gestore.scacchiera.set(5, 2, gestore.scacchiera.get_pedone("Bianco"))
    assert gestore.Usa_Cavallo("Cxc3", "Bianco") == 0

    #Due cavalli non possono catturare se non è specificata la colonna di partenza
    gestore.scacchiera.set(6,3,gestore.scacchiera.get_cavallo("Bianco"))
    gestore.scacchiera.set(6,5,gestore.scacchiera.get_cavallo("Bianco"))
    gestore.scacchiera.set(4,4,gestore.scacchiera.get_pedone("Nero"))
    assert gestore.Usa_Cavallo("Cxe4", "Bianco") == 2

    #Due cavalli dello stesso tipo non  possono catturare insieme se non è specificata \
    # la riga di partenza
    gestore.scacchiera.set(6,2,gestore.scacchiera.get_cavallo("Bianco"))
    gestore.scacchiera.set(5,1,gestore.scacchiera.get_cavallo("Bianco"))
    gestore.scacchiera.set(4,4,gestore.scacchiera.get_pedone("Nero"))
    assert gestore.Usa_Cavallo("Cxe4", "Bianco") == 2

## Test per Usa_Donna ##
def test_usa_donna_casi_positivi(gestore):
    """"Test mosse valide per la regina."""
     #Due donne si muovono sulla stessa riga
    gestore.scacchiera.set(3, 3, gestore.scacchiera.get_Donna("Bianco"))
    gestore.scacchiera.set(3, 4, gestore.scacchiera.get_Donna("Bianco"))
    assert gestore.Usa_Donna("Ddc4","Bianco") == 1
    gestore.scacchiera.set_vuoto(4,2)
    gestore.scacchiera.set(3, 3, gestore.scacchiera.get_Donna("Bianco"))
    #Cattura con due donne sulla stessa riga
    gestore.scacchiera.set(4, 3, gestore.scacchiera.get_pedone("Nero"))
    assert gestore.Usa_Donna("Ddxd4","Bianco") == 1
    
    gestore.scacchiera.set_vuoto(4,3)
    gestore.scacchiera.set_vuoto(4,2)
    gestore.scacchiera.set_vuoto(3,4)
    gestore.scacchiera.set(3, 3, gestore.scacchiera.get_Donna("Bianco"))
    
    # Movimento diagonale
    assert gestore.Usa_Donna("De6", "Bianco") == 1
    
    # Movimento dritto
    gestore.scacchiera.set_vuoto(1,3)
    assert gestore.Usa_Donna("Dd7", "Bianco") == 1

    #Movimento sulla colonna
    gestore.scacchiera.set_vuoto(3,2)
    assert gestore.Usa_Donna("Dd4", "Bianco") == 1

    # Cattura valida sulla stessa colonna
    gestore.scacchiera.set(5, 3, gestore.scacchiera.get_pedone("Nero"))
    assert gestore.Usa_Donna("Dxd3", "Bianco") == 1

    #cattura sulla stessa diagonale
    gestore.scacchiera.set(4, 4, gestore.scacchiera.get_pedone("Nero"))
    assert gestore.Usa_Donna("Dxe4", "Bianco") == 1

    #Due donne si muovono sulla stessa colonna
    
    gestore.scacchiera.set_vuoto(4,4)
    gestore.scacchiera.set_vuoto(5,3)
    gestore.scacchiera.set(4, 3, gestore.scacchiera.get_Donna("Bianco"))
    assert gestore.Usa_Donna("D4e4","Bianco") == 1

    #due donne catturano sulla stessa colonna
    gestore.scacchiera.set_vuoto(4,4)
    gestore.scacchiera.set(3, 3, gestore.scacchiera.get_Donna("Bianco"))
    gestore.scacchiera.set(4, 3, gestore.scacchiera.get_Donna("Bianco"))
    gestore.scacchiera.set(4, 4, gestore.scacchiera.get_pedone("Nero"))
    assert gestore.Usa_Donna("D4xe4","Bianco") == 1
    
    
    


def test_usa_donna_casi_negativi(gestore):
    """"Test mosse non valide per la regina."""
    #Due donne si muovono sulla stessa riga  ma va specificata la riga di partenza
    gestore.scacchiera.set(3, 3, gestore.scacchiera.get_Donna("Bianco"))
    gestore.scacchiera.set(3, 4, gestore.scacchiera.get_Donna("Bianco"))
    assert gestore.Usa_Donna("Dd4","Bianco") == 2
    gestore.scacchiera.set_vuoto(4,2)
    gestore.scacchiera.set(3, 3, gestore.scacchiera.get_Donna("Bianco"))

    #Cattura con due donne sulla stessa riga purchè specificata la riga di partenza
    gestore.scacchiera.set(4, 3, gestore.scacchiera.get_pedone("Nero"))
    assert gestore.Usa_Donna("Dxd4","Bianco") == 2
    
    gestore.scacchiera.set_vuoto(4,3)
    gestore.scacchiera.set_vuoto(4,2)
    gestore.scacchiera.set_vuoto(3,4)
    gestore.scacchiera.set(3, 3, gestore.scacchiera.get_Donna("Bianco"))
    
    # Movimento fuori traiettoria
    assert gestore.Usa_Donna("Df6", "Bianco") == 0
    gestore.scacchiera.set_vuoto(1,3)

    # Salto sopra pezzi
    gestore.scacchiera.set(4, 3, gestore.scacchiera.get_pedone("Bianco"))
    assert gestore.Usa_Donna("Da7", "Bianco") == 0
    
    # Cattura pezzo dello stesso colore
    gestore.scacchiera.set(6, 3, gestore.scacchiera.get_pedone("Bianco"))
    assert gestore.Usa_Donna("Dxd7", "Bianco") == 0

    gestore.scacchiera.set_vuoto(3,2)
    

    # Cattura fuori traiettoria
    gestore.scacchiera.set(5, 4, gestore.scacchiera.get_pedone("Nero"))
    assert gestore.Usa_Donna("Dxf4", "Bianco") == 0

    #Due donne si muovono sulla stessa riga se è specificata la riga di partenza
    
    gestore.scacchiera.set_vuoto(4,4)
    gestore.scacchiera.set_vuoto(5,3)
    gestore.scacchiera.set(4, 3, gestore.scacchiera.get_Donna("Bianco"))
    assert gestore.Usa_Donna("De4","Bianco") == 2

    #due donne catturano sulla stessa colonna se è speficata la colonna di partenza
    gestore.scacchiera.set_vuoto(4,4)
    gestore.scacchiera.set(3, 3, gestore.scacchiera.get_Donna("Bianco"))
    gestore.scacchiera.set(4, 3, gestore.scacchiera.get_Donna("Bianco"))
    gestore.scacchiera.set(4, 4, gestore.scacchiera.get_pedone("Nero"))
    assert gestore.Usa_Donna("Dxe4","Bianco") == 2
    

## Test per Usa_Re ##
def test_usa_re_casi_positivi(gestore):
    """Test casi validi per le mosse del re."""
    gestore.scacchiera.set(4, 4, gestore.scacchiera.get_re("Bianco"))
    
    # Movimento di una casella
    gestore.scacchiera.set_vuoto(6,4)
    assert gestore.Usa_Re("Re2", "Bianco") == 1
    
    # Cattura valida
    gestore.scacchiera.set(5,4, gestore.scacchiera.get_pedone("Nero"))
    assert gestore.Usa_Re("Rxe3", "Bianco") == 1

def test_usa_re_casi_negativi(gestore):
    """Test casi non validi per le mosse del re."""
    # Mossa troppo lunga
    assert gestore.Usa_Re("Re3", "Bianco") == 0

    #Salta su un pezzo
    assert gestore.Usa_Re("Re2", "Bianco") == 0

    #Cattura lo stesso colore
    assert gestore.Usa_Re("Rxe2","Bianco") == 0

    
    # Mossa in scacco
    gestore.scacchiera.set_vuoto(6,4)
    gestore.scacchiera.set(6, 3, gestore.scacchiera.get_torre("Nero"))
    assert gestore.Usa_Re("Re2", "Bianco") == 3
    

## Test per arrocco ##
def test_arrocco_casi_positivi(gestore):
    """Test casi validi per l'arrocco."""
    #Arrocco corto
    gestore.scacchiera.set_vuoto(7,5)
    gestore.scacchiera.set_vuoto(7,6)
    assert gestore.arrocco("0-0", "Bianco") == 1

    #Arrocco lungo
    gestore.scacchiera.set_vuoto(7,1)
    gestore.scacchiera.set_vuoto(7,2)
    gestore.scacchiera.set_vuoto(7,3)
    gestore.scacchiera.set_vuoto(7,6)
    gestore.scacchiera.set(7,4,gestore.scacchiera.get_re("Bianco"))
    assert gestore.arrocco("0-0-0", "Bianco") == 1





def test_arrocco_casi_negativi(gestore):
    """Test casi non validi per l'arrocco."""
    # Arrocco corto con pezzi in mezzo
    assert gestore.arrocco("0-0", "Bianco") == 0
    # Arrocco lungo con pezzi in mezzo
    assert gestore.arrocco("0-0-0", "Nero") == 0
    # Re già mosso
    gestore.scacchiera.set_vuoto(7,5)
    gestore.scacchiera.set_vuoto(7,6)
    gestore.scacchiera.get_pezzo(7,4).gia_mosso = 1
    assert gestore.arrocco("0-0", "Bianco") == 0
    
    # Torre già mossa
    gestore.scacchiera.set_vuoto(7,6)
    gestore.scacchiera.set(7,4,gestore.scacchiera.get_re("Bianco"))
    gestore.scacchiera.set_vuoto(7,5)
    gestore.scacchiera.set(7,7,gestore.scacchiera.get_torre("Bianco"))
    gestore.scacchiera.get_pezzo(0, 0).set_Prima_Mossa()
    assert gestore.arrocco("0-0-0", "Nero") == 0
    
    # Re sotto scacco
    gestore.scacchiera.set_vuoto(7,6)
    gestore.scacchiera.set(7,4,gestore.scacchiera.get_re("Bianco"))
    gestore.scacchiera.set_vuoto(7,5)
    gestore.scacchiera.set(7,7,gestore.scacchiera.get_torre("Bianco"))
    gestore.scacchiera.set(6,5,gestore.scacchiera.get_Donna("Nero"))
    assert gestore.arrocco("0-0", "Bianco") == 0

    #Casella Minacciata
    gestore.scacchiera.set_vuoto(6,5)
    gestore.scacchiera.set(6,6,gestore.scacchiera.get_Donna("Nero"))
    assert gestore.arrocco("0-0", "Bianco") == 0

## Test per mossa_legale ##
def test_mossa_legale_casi_positivi(gestore):
    """Test casi validi per mossa_legale."""
    #Re sfugge allo scacco 
    gestore.scacchiera.set(6,5,gestore.scacchiera.get_Donna("Nero"))
    gestore.Usa_Re("Rxf2","Bianco")
    assert gestore.mossa_legale("Bianco") == 0
    
    # Re non sotto scacco
    gestore.Usa_Pedone("d4","Bianco")
    assert gestore.mossa_legale("Bianco") == 0

def test_mossa_legale_casi_negativi(gestore):
    """Test casi non validi per mossa_legale."""
    #Il re resta sotto cattura
    gestore.scacchiera.set_vuoto(6,5)
    gestore.scacchiera.set(5,6,gestore.scacchiera.get_Donna("Nero"))
    gestore.Usa_Re("Rf2","Bianco")
    assert gestore.mossa_legale("Bianco") == 3

    #Il pezzo si sposta mettendo in pericolo il Re
    gestore.scacchiera.set(6,5,gestore.scacchiera.get_pedone("Bianco"))
    assert gestore.Usa_Pedone("f4","Bianco") == 3



## Test per possibile_scacco_matto ##
def test_possibile_scacco_matto_casi_positivi(gestore):
    """Test casi validi per scacco matto."""
    # Scacco matto classico
    gestore.scacchiera.set(3, 4, gestore.scacchiera.get_Donna("Nero"))
    gestore.scacchiera.set(4, 4, gestore.scacchiera.get_Donna("Nero"))
    gestore.Usa_Donna("Dxe2","Nero")
    assert gestore.possibile_scacco_matto("Nero") == 1
    
    # Non scacco matto (re può muoversi)
    gestore.scacchiera.set(0, 4, gestore.scacchiera.get_re("Nero"))
    gestore.scacchiera.set(1, 3, gestore.scacchiera.get_Donna("Bianco"))
    assert gestore.possibile_scacco_matto("Nero") == 0

def test_possibile_scacco_matto_casi_negativi(gestore):
    """Verifica i casi in cui non si verifica uno scacco matto."""
    #Un pezzo può coprire il re
    gestore.scacchiera.set(3, 4, gestore.scacchiera.get_Donna("Nero"))
    gestore.scacchiera.set(4, 4, gestore.scacchiera.get_Donna("Nero"))
    gestore.scacchiera.set_vuoto(6,4)
    gestore.scacchiera.set(5, 5,gestore.scacchiera.get_Donna("Bianco"))
    #gestore.Usa_Donna("De3","Bianco")
    assert gestore.possibile_scacco_matto("Bianco") == 0

    #Il re può difendersi 
    gestore.scacchiera.set_vuoto(3,4)
    gestore.Usa_Donna("Dxe3","Nero")
    assert gestore.possibile_scacco_matto("Bianco") == 0

    #Il re può scappare
    gestore.scacchiera.set_vuoto(6,4)
    gestore.scacchiera.set_vuoto(7,3)
    gestore.scacchiera.set_vuoto(5,5)
    assert gestore.possibile_scacco_matto("Bianco") == 0




## Test per possibile_stallo ##
def test_possibile_stallo_casi_positivi(gestore):
    """Test casi validi per stallo."""
    # Riga 0
    gestore.scacchiera.set_vuoto(0, 0)
    gestore.scacchiera.set_vuoto(0, 1)
    gestore.scacchiera.set_vuoto(0, 2)
    gestore.scacchiera.set_vuoto(0, 3)
    gestore.scacchiera.set_vuoto(0, 4)
    gestore.scacchiera.set_vuoto(0, 5)
    gestore.scacchiera.set_vuoto(0, 6)
    gestore.scacchiera.set_vuoto(0, 7)

    # Riga 1
    gestore.scacchiera.set_vuoto(1, 0)
    gestore.scacchiera.set_vuoto(1, 1)
    gestore.scacchiera.set_vuoto(1, 2)
    gestore.scacchiera.set_vuoto(1, 3)
    gestore.scacchiera.set_vuoto(1, 4)
    gestore.scacchiera.set_vuoto(1, 5)
    gestore.scacchiera.set_vuoto(1, 6)
    gestore.scacchiera.set_vuoto(1, 7)

    # Riga 2
    gestore.scacchiera.set_vuoto(2, 0)
    gestore.scacchiera.set_vuoto(2, 1)
    gestore.scacchiera.set_vuoto(2, 2)
    gestore.scacchiera.set_vuoto(2, 3)
    gestore.scacchiera.set_vuoto(2, 4)
    gestore.scacchiera.set_vuoto(2, 5)
    gestore.scacchiera.set_vuoto(2, 6)
    gestore.scacchiera.set_vuoto(2, 7)

    # Riga 3
    gestore.scacchiera.set_vuoto(3, 0)
    gestore.scacchiera.set_vuoto(3, 1)
    gestore.scacchiera.set_vuoto(3, 2)
    gestore.scacchiera.set_vuoto(3, 3)
    gestore.scacchiera.set_vuoto(3, 4)
    gestore.scacchiera.set_vuoto(3, 5)
    gestore.scacchiera.set_vuoto(3, 6)
    gestore.scacchiera.set_vuoto(3, 7)

    # Riga 4
    gestore.scacchiera.set_vuoto(4, 0)
    gestore.scacchiera.set_vuoto(4, 1)
    gestore.scacchiera.set_vuoto(4, 2)
    gestore.scacchiera.set_vuoto(4, 3)
    gestore.scacchiera.set_vuoto(4, 4)
    gestore.scacchiera.set_vuoto(4, 5)
    gestore.scacchiera.set_vuoto(4, 6)
    gestore.scacchiera.set_vuoto(4, 7)

    # Riga 5
    gestore.scacchiera.set_vuoto(5, 0)
    gestore.scacchiera.set_vuoto(5, 1)
    gestore.scacchiera.set_vuoto(5, 2)
    gestore.scacchiera.set_vuoto(5, 3)
    gestore.scacchiera.set_vuoto(5, 4)
    gestore.scacchiera.set_vuoto(5, 5)
    gestore.scacchiera.set_vuoto(5, 6)
    gestore.scacchiera.set_vuoto(5, 7)

    # Riga 6
    gestore.scacchiera.set_vuoto(6, 0)
    gestore.scacchiera.set_vuoto(6, 1)
    gestore.scacchiera.set_vuoto(6, 2)
    gestore.scacchiera.set_vuoto(6, 3)
    gestore.scacchiera.set_vuoto(6, 4)
    gestore.scacchiera.set_vuoto(6, 5)
    gestore.scacchiera.set_vuoto(6, 6)
    gestore.scacchiera.set_vuoto(6, 7)

    # Riga 7
    gestore.scacchiera.set_vuoto(7, 0)
    gestore.scacchiera.set_vuoto(7, 1)
    gestore.scacchiera.set_vuoto(7, 2)
    gestore.scacchiera.set_vuoto(7, 3)
    gestore.scacchiera.set_vuoto(7, 4)
    gestore.scacchiera.set_vuoto(7, 5)
    gestore.scacchiera.set_vuoto(7, 6)
    gestore.scacchiera.set_vuoto(7, 7)

    
    # Stallo classico
    gestore.scacchiera.set(0, 0, gestore.scacchiera.get_re("Nero"))
    gestore.scacchiera.set(1, 2, gestore.scacchiera.get_Donna("Bianco"))
    gestore.scacchiera.set(2, 0, gestore.scacchiera.get_re("Bianco"))
    assert gestore.possibile_stallo("Nero") == 1

    
    # Non stallo (re può muoversi)
    gestore.scacchiera.set_vuoto(1,2)
    assert gestore.possibile_stallo("Nero") == 0