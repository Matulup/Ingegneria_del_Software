from scacchi.entity.Comandi import Comandi

comandi = Comandi()

def test_esiste_commando():
    """Verifica se i comandi validi vengono riconosciuti correttamente."""
    #Vengono accettati solo i seguenti comandi
    assert comandi.esiste_commando("/gioca") == 1
    assert comandi.esiste_commando("/esci") == 1
    assert comandi.esiste_commando("/abbandona") == 1
    assert comandi.esiste_commando("/mosse") == 1
    assert comandi.esiste_commando("/patta") == 1
    assert comandi.esiste_commando("/scacchiera") == 1
    assert comandi.esiste_commando("/help") == 1

    #Non vengono accettati altri comandi
    assert comandi.esiste_commando("/inizia") == 0
    assert comandi.esiste_commando("/chiudi gioco") == 0
    assert comandi.esiste_commando("/mostra mosse") == 0
    assert comandi.esiste_commando("/vuoi patteggiare") == 0
    assert comandi.esiste_commando("/finisci partita") == 0
    assert comandi.esiste_commando("/aiuti") == 0
    assert comandi.esiste_commando("/mostra scacchiera") == 0

def test_get_numero_comando():
    """Verifica che venga restituito il numero corretto associato a ciascun comando."""
    assert comandi.get_numero_comando("/gioca") == 0
    assert comandi.get_numero_comando("/help") == 1
    assert comandi.get_numero_comando("/scacchiera") == 2
    assert comandi.get_numero_comando("/esci") == 3
    assert comandi.get_numero_comando("/abbandona") == 4
    assert comandi.get_numero_comando("/mosse") == 5
    assert comandi.get_numero_comando("/patta") == 6






