from scacchi.entity.Re import Re

re = Re("Bianco")

def test_mossa_lecita():
    """Verifica che il Re si muova correttamente di una sola casella."""
    #Il Re si può muovere in tutte le direzioni purchè si muova di una sola casella
    assert re.mossa_lecita(2,3,1,2) == 1
    assert re.mossa_lecita(2,3,1,3) == 1
    assert re.mossa_lecita(2,3,1,4) == 1
    assert re.mossa_lecita(2,3,2,4) == 1
    assert re.mossa_lecita(2,3,3,4) == 1
    assert re.mossa_lecita(2,3,3,3) == 1
    assert re.mossa_lecita(2,3,3,2) == 1
    assert re.mossa_lecita(2,3,2,2) == 1

    #Il Re non si può muovere di due caselle
    assert re.mossa_lecita(2,2,0,4) == 0
    assert re.mossa_lecita(2,1,2,3) == 0
    assert re.mossa_lecita(3,3,3,0) == 0
    assert re.mossa_lecita(1,2,3,2) == 0

def test_cattura_lecita():
    """Verifica che il Re possa catturare a una casella di distanza."""
    #Il Re può catturare in tutte le direzioni purchè  ci sia la distanza\
    #  di una sola casella
    assert re.cattura_lecita(2,3,1,2) == 1
    assert re.cattura_lecita(2,3,1,3) == 1
    assert re.cattura_lecita(2,3,1,4) == 1
    assert re.cattura_lecita(2,3,2,4) == 1
    assert re.cattura_lecita(2,3,3,4) == 1
    assert re.cattura_lecita(2,3,3,3) == 1
    assert re.cattura_lecita(2,3,3,2) == 1
    assert re.cattura_lecita(2,3,2,2) == 1

    #Il Re non può catturare a distanza  di due caselle
    assert re.cattura_lecita(2,2,0,4) == 0
    assert re.cattura_lecita(2,1,2,3) == 0
    assert re.cattura_lecita(3,3,3,0) == 0
    assert re.cattura_lecita(1,2,3,2) == 0

def test_get_mosso():
    """Testa il metodo get_mosso per verificare che venga registrata la mossa del Re."""
    rem = Re("Bianco")
    rem.get_mosso() 
    assert rem.get_mosso() == rem.gia_mosso
   