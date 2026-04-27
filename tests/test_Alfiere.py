from scacchi.entity.Alfiere import Alfiere

alfiere = Alfiere("Bianco")
alfieren = Alfiere("Nero") 
def test_mossa_lecita():
    """Testa se l'alfiere può muoversi correttamente o no."""
    #L'alfiere si può muovere solo in diagonale senza limitazioni 
    assert alfiere.mossa_lecita(3,1,1,3) == 1
    assert alfiere.mossa_lecita(2,2,0,0) == 1
    assert alfieren.mossa_lecita(1,1,3,3) == 1
    assert alfieren.mossa_lecita(1,4,3,2) == 1

    #L'alfiere non si può muovere sulle stessa riga o sulla stessa colonna
    assert alfiere.mossa_lecita(3,1,1,1) == 0
    assert alfiere.mossa_lecita(4,1,2,1) == 0
    assert alfiere.mossa_lecita(5,3,5,6) == 0
    assert alfieren.mossa_lecita(1,2,3,2) == 0
    assert alfieren.mossa_lecita(5,2,3,2) == 0
    assert alfieren.mossa_lecita(1,1,1,3) == 0

def test_cattura_lecita():
    """Testa se l'alfiere può catturare o no."""
    #L'alfiere  può catturare solo in diagonale senza limitazioni 
    assert alfiere.cattura_lecita(3,1,1,3) == 1
    assert alfiere.cattura_lecita(2,2,0,0) == 1
    assert alfieren.cattura_lecita(1,1,3,3) == 1
    assert alfieren.cattura_lecita(1,4,3,2) == 1

    #L'alfiere non  può catturare  sulle stessa riga o sulla stessa colonna
    assert alfiere.cattura_lecita(3,1,1,1) == 0
    assert alfiere.cattura_lecita(4,1,2,1) == 0
    assert alfiere.cattura_lecita(5,3,5,6) == 0
    assert alfieren.cattura_lecita(1,2,3,2) == 0
    assert alfieren.cattura_lecita(5,2,3,2) == 0
    assert alfieren.cattura_lecita(1,1,1,3) == 0
