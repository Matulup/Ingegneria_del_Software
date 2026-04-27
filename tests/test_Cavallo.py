from scacchi.entity.Cavallo import Cavallo

cavallo = Cavallo("Bianco")
cavallon = Cavallo("Nero") 

def test_mossa_lecita():
    """Verifica che il cavallo si muova correttamente o meno."""
    #Il cavallo può effettuare solo movimenti ad L comprendendo 3 caselle \
    # (2 orizzonatali e una verticale) 
    assert cavallon.mossa_lecita(2,2,1,0) == 1
    assert cavallon.mossa_lecita(2,2,3,4) == 1
    assert cavallon.mossa_lecita(2,2,3,0) == 1
    assert cavallon.mossa_lecita(2,2,1,4) == 1
    assert cavallo.mossa_lecita(3,3,2,1) == 1
    assert cavallo.mossa_lecita(3,3,4,5) == 1
    assert cavallo.mossa_lecita(3,3,4,1) == 1
    assert cavallo.mossa_lecita(3,3,2,5) == 1

    #Il cavallo non si può spostare sulla stessa riga/colonna per più di due celle 
    assert cavallon.mossa_lecita(2,3,2,6) == 0
    assert cavallon.mossa_lecita(3,3,3,6) == 0
    assert cavallo.mossa_lecita(5,1,1,1) == 0
    assert cavallo.mossa_lecita(5,1,5,4) == 0
    
    #Il cavallo non può muoversi in diagonale 

    assert cavallon.mossa_lecita(2,2,1,3) == 0
    assert cavallon.mossa_lecita(2,2,0,0) == 0
    assert cavallon.mossa_lecita(2,2,3,1) == 0
    assert cavallon.mossa_lecita(2,2,3,3) == 0
    assert cavallo.mossa_lecita(3,3,2,4) == 0
    assert cavallo.mossa_lecita(3,3,1,1) == 0
    assert cavallo.mossa_lecita(3,3,4,4) == 0
    assert cavallo.mossa_lecita(3,3,4,0) == 0

def test_cattura_lecita():
    """Verifica che il cavallo si catturi correttamente o meno."""
    #Il cavallo può catturare solo muovendosi ad L comprendendo 3 caselle \
    # (2 orizzonatali e una verticale) 
    assert cavallon.cattura_lecita(2,2,1,0) == 1
    assert cavallon.cattura_lecita(2,2,3,4) == 1
    assert cavallon.cattura_lecita(2,2,3,0) == 1
    assert cavallon.cattura_lecita(2,2,1,4) == 1
    assert cavallo.cattura_lecita(3,3,2,1) == 1
    assert cavallo.cattura_lecita(3,3,4,5) == 1
    assert cavallo.cattura_lecita(3,3,4,1) == 1
    assert cavallo.cattura_lecita(3,3,2,5) == 1

    #Il cavallo non può catturare sulla stessa riga/colonna per più di due celle 
    assert cavallon.cattura_lecita(2,3,2,6) == 0
    assert cavallon.cattura_lecita(3,3,3,6) == 0
    assert cavallo.cattura_lecita(5,1,1,1) == 0
    assert cavallo.cattura_lecita(5,1,5,4) == 0
    
    #Il cavallo non può catturare in diagonale 

    assert cavallon.cattura_lecita(2,2,1,3) == 0
    assert cavallon.cattura_lecita(2,2,0,0) == 0
    assert cavallon.cattura_lecita(2,2,3,1) == 0
    assert cavallon.cattura_lecita(2,2,3,3) == 0
    assert cavallo.cattura_lecita(3,3,2,4) == 0
    assert cavallo.cattura_lecita(3,3,1,1) == 0
    assert cavallo.cattura_lecita(3,3,4,4) == 0
    assert cavallo.cattura_lecita(3,3,4,0) == 0

