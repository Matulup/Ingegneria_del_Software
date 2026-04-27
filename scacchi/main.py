import argparse

from .boundary import Gioco


def main():
    """Classe main."""
    parser = argparse.ArgumentParser(
        description="Applicazione Scacchi - comandi disponibili:",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
        /gioca: se nessuna partita è in corso, l'app mostra la scacchiera con i pezzi
        in posizione iniziale e si predispone a ricevere la prima mossa di gioco del
        bianco o altri comandi. Per muovere i pezzi si usa la notazione algebrica corta.

        /help (oppure chiamando l'applicazione con il flag --help, -h): si ha come
        risultato una descrizione concisa seguita dalla lista di comandi disponibili,
        uno per riga.

        /esci: l'applicazione si chiude chiedendo prima conferma
        -- se la conferma è positiva, l'app si chiude restituendo il controllo al SO
        -- se la conferma è negativa, l'app si predispone a ricevere nuovi tentativi
            o comandi

        /patta: l'applicazione prende in carico la richiesta da parte dell'utente di
        chiudere la partita con la patta. Chiede conferma all’avversario
        -- se l’avversario accetta, la partita termina con il pareggio
        -- se l’avversario rifiuta, l'app si predispone a ricevere nuovi tentativi o
            comandi

        /abbandona: l'applicazione si predispone a chiudere la partita per abbandono da
        parte dell'utente che ha fatto la richiesta. Chiede conferma all'avversario
        -- se la conferma è positiva, l'app comunica che l’avversario ha vinto per
            abbandono
        -- se la conferma è negativa, l'app si predispone a ricevere nuovi tentativi
            o comandi

        /scacchiera:
        -- se il gioco non è iniziato, l'app suggerisce il comando /gioca
        -- se il gioco è iniziato, l'app mostra la posizione di tutti i pezzi sulla 
            scacchiera

        /mosse: l'app mostra la storia delle mosse con notazione algebrica abbreviata
        in italiano""",
        add_help=False  # Disabilita l'help predefinito per gestirlo manualmente
    )
    
    # Aggiungi manualmente le opzioni di help
    parser.add_argument('-h', '--help', action='store_true', \
                        help="Mostra tutti i comandi utilizzabili")
    
    args = parser.parse_args()
    
    if args.help:
        parser.print_help()
    
    """Chiama la classe Gioco."""
    #"""Run the Scacchi game and activate the GH workflows. """
    #ui = UI()
    #ui.set_accent_color("blue")
    #
    #name = input("Benvenuto in Scacchi! Inserisci il tuo nome: ")
    #print(
    #    f"Ciao [bold {ui.get_accent_color()}]{name}[/bold {ui.get_accent_color()}]! "
    #    "Iniziamo a giocare a [bold]scacchi[/bold]!"
    #)
    g = Gioco()
    g.inizia()


if __name__ == "__main__":
    main()