from scacchi.entity.Pedone import Pedone

pedone = Pedone("Bianco")
pedonen = Pedone("Nero") 
def test_mossa_lecita():
    """Testa la validità dei movimenti leciti o meno del pedone bianco e nero."""
    #classe di equivalenza per il movimento del pedone Bianco 
    #Il pedone con la prima mossa si muove di 1 o 2 caselle,con le altre mosse può muov\
    # ersi
    #solo di una casella
    assert pedone.mossa_lecita(6,0,4,0) == 1 
    assert pedone.mossa_lecita(6,0,5,0) == 1 
    assert pedone.mossa_lecita(5,0,4,0) == 1 
    #Il pedone  non si può muovere di una o più caselle indietro caselle indietro
    assert pedone.mossa_lecita(6,0,7,0) == 0
    #Il pedone con la prima mossa si può muovere di massimo 2 caselle
    assert pedone.mossa_lecita(6,0,3,0) == 0
    #Il pedone con la prima mossa si può muovere di massimo 2 caselle ma sempre \
    # sulla stessa colonna
    assert pedone.mossa_lecita(6,0,2,2) == 0
    assert pedone.mossa_lecita(6,0,6,1) == 0
    
    #Il pedone non può muoversi in diagonale sulla scacchiera
    assert pedone.mossa_lecita(6,0,5,1) == 0
    assert pedone.mossa_lecita(6,1,5,0) == 0

    # classe di equivalenza per il pedone Nero
    #Il pedone con la prima mossa si muove di 1 o 2 caselle,\
    # con le altre mosse può muoversi solo di una casella

    assert pedonen.mossa_lecita(1,0,3,0) == 1
    assert pedonen.mossa_lecita(1,0,2,0) == 1
    assert pedonen.mossa_lecita(2,0,3,0) == 1

    #Il pedone  non si può muovere di una casella indietro
    assert pedonen.mossa_lecita(1,0,0,0) == 0

    #Il pedone con la prima mossa si può muovere di massimo 2 caselle
    assert pedonen.mossa_lecita(1,0,5,0) == 0

    #Il pedone con la prima mossa si può muovere di massimo 2 caselle ma sempre \
    # sulla stessa colonna
    assert pedonen.mossa_lecita(1,0,5,5) == 0
    assert pedonen.mossa_lecita(1,0,1,1) == 0

    #Il pedone non può muoversi in diagonale sulla scacchiera
    assert pedonen.mossa_lecita(1,0,2,1) == 0
    assert pedonen.mossa_lecita(2,2,1,1) == 0

def test_cattura_lecita():
    """Verifica che il pedone possa catturare solo in diagonale e quando non può."""
    #Il pedone può catturare soltanto spostandosi di una cella in diagonale 
    assert pedone.cattura_lecita(3,3,2,2) == 1
    assert pedone.cattura_lecita(3,3,2,4) == 1
    assert pedonen.cattura_lecita(1,1,2,2) == 1
    assert pedonen.cattura_lecita(1,4,2,3) == 1

    #Il pedone non può catturare sulla stessa colonna neanche tornando indietro
    assert pedone.cattura_lecita(6,2,5,2) == 0
    assert pedone.cattura_lecita(4,2,5,2) == 0
    assert pedonen.cattura_lecita(4,2,5,2) == 0
    assert pedonen.cattura_lecita(2,2,1,2) == 0

    #Il pedone non può cattuare sulla stessa riga neanche tornando indietro
    assert pedone.cattura_lecita(3,0,3,1) == 0
    assert pedone.cattura_lecita(3,2,3,1) == 0
    assert pedone.cattura_lecita(1,0,1,1) == 0
    assert pedone.cattura_lecita(2,2,2,3) == 0

def test_set_prima_mossa():
    """Verifica il corretto settaggio dello stato di prima mossa per i pedoni."""
    pedoneB = Pedone("Bianco")
    pedoneN = Pedone("Nero") 
    pedoneB.set_prima_mossa()
    pedoneN.set_prima_mossa()

    assert pedoneB.prima_mossa == 0
    assert pedoneN.prima_mossa == 0 








