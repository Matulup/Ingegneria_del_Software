from scacchi.entity.Torre import Torre

torre = Torre("Bianco")

def test_mossa_lecita():
    """Verifica che la Torre si muova solo in linea retta (orizzontale o verticale)."""
    #La torre ha libertà di movimento purchè si muova solo sulla stessa colonna o sulla\
    #stessa riga
    assert torre.mossa_lecita(7,0,3,0) == 1
    assert torre.mossa_lecita(0,0,1,0) == 1
    assert torre.mossa_lecita(2,1,2,6) == 1
    assert torre.mossa_lecita(1,4,1,1) == 1

    #La torre non può muoversi in diagonale
    assert torre.mossa_lecita(1,1,2,2) == 0
    assert torre.mossa_lecita(0,0,2,1) == 0
    assert torre.mossa_lecita(7,0,6,1) == 0
    assert torre.mossa_lecita(3,4,2,3) == 0

def test_cattura_lecita():
    """Verifica che la Torre possa catturare solo su riga o colonna."""
    #La Torre può catturare soltanto sulla colonna o sulla riga dove si trova 
    assert torre.cattura_lecita(7,0,3,0) == 1
    assert torre.cattura_lecita(0,0,1,0) == 1
    assert torre.cattura_lecita(2,1,2,6) == 1
    assert torre.cattura_lecita(1,4,1,1) == 1

    #La torre non può catturare in diagonale
    assert torre.cattura_lecita(1,1,2,2) == 0
    assert torre.cattura_lecita(0,0,2,1) == 0
    assert torre.cattura_lecita(7,0,6,1) == 0
    assert torre.cattura_lecita(3,4,2,3) == 0


def test_set_Prima_Mossa():
    """Verifica l'inizializzazione dello stato 'Prima mossa' per la Torre."""
    torreb = Torre("Bianco")
    torren = Torre("Nero") 
    torreb.set_Prima_Mossa()
    torren.set_Prima_Mossa()

    assert torreb.Prima_mossa == 1
    assert torren.Prima_mossa == 1

def test_get_Prima_Mossa():
    """Testa il recupero dello stato 'Prima mossa' della Torre."""
    torreB = Torre("Bianco")
    torreN = Torre("Nero")
    torreN.get_Prima_Mossa()
    torreB.set_Prima_Mossa() 
    assert torreB.get_Prima_Mossa() == torreB.Prima_mossa 
    assert torreN.get_Prima_Mossa() == torreN.Prima_mossa 