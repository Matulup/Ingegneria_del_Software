from scacchi.entity.Donna import Donna

donna = Donna("Bianco")

def test_mossa_lecita():
    """Verifica che la donna possa muoversi o meno."""
    #La donna può muoversi in verticale,in orizzontale e in obliquo purchè rimanga \
    #sulla diagonale principale
    assert donna.mossa_lecita(2,2,2,4) == 1
    assert donna.mossa_lecita(2,2,3,3) == 1
    assert donna.mossa_lecita(2,2,3,2) == 1
    assert donna.mossa_lecita(2,2,2,0) == 1
    assert donna.mossa_lecita(3,1,4,0) == 1
    assert donna.mossa_lecita(3,1,2,0) == 1
    assert donna.mossa_lecita(2,3,0,1) == 1

    #la donna non si può muovere su caselle che comprendono la sua riga o la sua colonna

    assert donna.mossa_lecita(2,3,3,1) == 0
    assert donna.mossa_lecita(3,2,1,3) == 0
    assert donna.mossa_lecita(2,3,0,2) == 0
    assert donna.mossa_lecita(2,3,3,5) == 0
    assert donna.mossa_lecita(2,0,3,2) == 0
    assert donna.mossa_lecita(2,0,0,1) == 0

def test_cattura_lecita():
    """Verifica che la donna possa catturare in verticale, orizzontale e diagonale."""
    #La donna può catturare in verticale,in orizzontale e in obliquo purchè rimanga \
    #sulla sua  diagonale principale
    assert donna.cattura_lecita(2,2,2,4) == 1
    assert donna.cattura_lecita(2,2,3,3) == 1
    assert donna.cattura_lecita(2,2,3,2) == 1
    assert donna.cattura_lecita(2,2,2,0) == 1
    assert donna.cattura_lecita(3,1,4,0) == 1
    assert donna.cattura_lecita(3,1,2,0) == 1
    assert donna.cattura_lecita(2,3,0,1) == 1

    #la donna non  può catturare su caselle che comprendono la sua riga o la sua colonna

    assert donna.cattura_lecita(2,3,3,1) == 0
    assert donna.cattura_lecita(3,2,1,3) == 0
    assert donna.cattura_lecita(2,3,0,2) == 0
    assert donna.cattura_lecita(2,3,3,5) == 0
    assert donna.cattura_lecita(2,0,3,2) == 0
    assert donna.cattura_lecita(2,0,0,1) == 0  
