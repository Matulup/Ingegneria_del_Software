from scacchi.control.Gestore_Mosse import Gestore_Mosse
from scacchi.entity.Comandi import Comandi


class Gioco:
    """<<Boundary>>.

    Classe che si occupa di dialogare con i giocatori. 
    - Permette l'avvio del programma. 
    - Gestisce le fasi principali della partita.
    - Consente l'utilizzo dei comandi del gioco.
    - Stampa a video messaggi, 'oggetti' come la scacchiera e i pezzi del gioco per 
        dialogare con gli utenti finali.
    - Stampa a video i messaggi di errore qualora necessari.
    """

    def __init__(self):
        self.comandi = Comandi()
        self.gestore = Gestore_Mosse()
        self.partita_iniziata = 0
        self.giocatore = "Bianco"
        self.avversario = "Nero"  
        self.cronologia_mosse = [] 
    
    def inizia(self):
        # Fa partire il programma (e non il gioco) e permette di 
        # digitare i comandi principali (/gioca, /help, ecc)
        # #

        #si controlla la validità del comando
        comando_valido = 0
        uscita = 0

        self.benvenuto()

        while comando_valido == 0 and uscita == 0 or uscita == 3:
            comando = input()
            comando_valido = self.comandi.esiste_commando(comando)
            if comando_valido == 0:
                self.stampa_comando_non_valido()
            
            else: 
                match self.comandi.get_numero_comando(comando):
                    case 0: # comando /gioca
                           uscita = self.gioca()
                           comando_valido = 0
                           if uscita == 0:
                             self.gestore = Gestore_Mosse()
                             self.giocatore = "Bianco"
                             self.avversario = "Nero" 
                             self.cronologia_mosse = []
                           if uscita != 2:
                               self.partita_finita()
                               self.partita_iniziata = 0
                    case 1: # comando /help
                            comando_valido=0 
                            self.help()
                    case 2: #comando /scacchiera
                            self.suggerimento_gioca()
                            comando_valido=0
                    case 3: #comando /esci
                            uscita = self.esci()
                            comando_valido=0
                    case _:
                        self.stampa_comando_non_valido()
                        comando_valido=0
        self.addio()
    
    def gioca(self):
        # Gestisce una partita in cui si alternano il giocatore bianco 
        # e il giocatore nero.
        # #
        partita_finita = 0
        uscita = 0

        if self.partita_iniziata == 0:
           self.partita_iniziata = 1
           self.stampa_scacchiera()


           while partita_finita == 0 and uscita == 0: # finché la partita non è conclusa
            print(self.giocatore, " :", end="")
            comando = input()

            # Verifica se il giocatore ha inserito una MOSSA e non un COMANDO
            if self.comandi.esiste_commando(comando) == 0: 
                                
                #Se la MOSSA non è valida 
                match self.gestore.gestore(comando, self.giocatore, self.avversario):
                    case 0:#il comando non è valido
                        self.stampa_comando_non_valido()

                    case 1:# il comando era valido ed è stato eseguito
                        self.cronologia_mosse.append(comando)
                        self.scambia_giocatori()
                        self.stampa_scacchiera()

                    case 2:#due o più pezzi potrebbero eseguire quella mossa
                        self.stampa_mossa_compatibile_con_piu_pezzi() 

                    case 3:# se la mossa potrebbe generare uno scacco
                        self.stampa_mossa_illegale()

                    case 5:# se il re è sotto scacco                      
                        self.cronologia_mosse.append(comando)
                        self.scambia_giocatori()
                        self.stampa_scacchiera()
                        self.stampa_scacco(self.giocatore)

                    case 6:# se la partita è finita per scacco matto
                        self.stampa_scacchiera()
                        self.stampa_scacco_matto(self.giocatore)
                        partita_finita = 1      
                        uscita = 0

                    case 7:# se la partita è finita per stallo
                        self.stampa_scacchiera()
                        self.stampa_stallo()
                        partita_finita = 1  
                        uscita = 0   

            else:
                match self.comandi.get_numero_comando(comando):
                    case 0: #/gioca
                        self.stampa_comando_non_valido()
                    case 1: #/help
                        self.help()  
                    case 2:#/scacchiera
                        self.stampa_scacchiera()
                    case 3: #comando /esci
                        uscita = self.esci()
                    case 4: #comando /abbandona
                        partita_finita = self.abbandona()
                    case 5: #comando /cronologia mosse
                        self.mostra_cronologia_mosse()
                    case 6 : #patta
                        partita_finita = self.patta()
                        
        return uscita

    def help(self):
        print ("""
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
        in italiano"""
    )
          
    def scambia_giocatori(self):
        # Inverte i ruoli dei giocatori (per indicare che si passa 
        # dal turno del giocatore bianco al turno del giocatore nero e viceversa)
        # #
        temp = self.giocatore 
        self.giocatore = self.avversario
        self.avversario = temp    

    def stampa_comando_non_valido(self):
        # Stampa a video un messaggio di errore per informare l'utente che
        # ha scritto male il comando/mossa
        # #
        print("|==============------> Il comando non è valido!!")
    
    def stampa_mossa_illegale(self):
        print("|==============------> mossa illegale!!")

    def stampa_mossa_compatibile_con_piu_pezzi(self): 
        print("|=======----> Ci sono 2 o più pezzi che possono eseguire questa mossa!!")
        print("|===========-----> (Specifica la riga o la colonna di partenza)")

    def stampa_aiuto(self):
        print("________________________________\
_________________________________________")
        print("\n                             \
                   Comandi utili: /help     ")
        print("                                 \
                              /esci     ")

    def stampa_scacchiera(self):
        # Stampa la scacchiera
        # #

        self.stampa_aiuto()
        print("     ", "           ", end="") 
        for i in range(8):
            
            for _j in range(8):
                print("-----", end="")
            print("-\n ","           ", 8-i, " ", end="")

            for j in range(8):
                if self.gestore.scacchiera is not None:
                    print("|", self.gestore.scacchiera.\
                          get_pezzo(i,j).get_icona()," ", end="")
                else:
                    print( "|  |", end="") 
            print("|\n     ", "           ", end="")

        for _j in range(8):
                print("-----", end="")
        print("-\n        ", end="")
        
        c ='a'
        print("           ", end="")
        while c <'i':
            print( c, "   ",end="")
            c = chr(ord(c) +1)
        print("\n")

    def suggerimento_gioca(self):
        #se il gioco non è iniziato l'app suggerisce il comando /gioca
        print("|========----> Forse volevi digiatre il comando /gioca per giocare")
    
    def esci(self):
        print( "|===================---------------------------\
-----====================|")
        print("|                  Confermi di uscire? (si o no)\
                        |")
        print("|----------------------------------------------\
-------------------------|")
        print(" V")
        i = input()
        while i!="si" and i!= "no":
            print("|=============-----> Prova a scrivere solo si o no (minuscoli)")
            i = input()
        if i == "si": 
            uscita = 2
        if i== "no":
            uscita = 0
        return uscita
    
    def abbandona(self):
        print("|----------------------------------------------\
-------------------------|")
        print("|                Confermi di voler abbandonare? (si o no)\
               |")
        print("|----------------------------------------------\
-------------------------|")
        print(" V")
        i = input()
        while i!="si" and i!= "no":
            print("|=============-----> Prova a scrivere solo si o no (minuscoli)")
            i = input()
        if i == "si": 
            uscita = 1
            self.partita_iniziata = 0
            print( "|===================---------------------------\
-----====================|")
            print( "|                                           \
                            |")
            print("|=======---->   Il giocatore",self.avversario,
                   "ha vinto per abbandono!!")
            print( "|                                           \
                            |")
        if i== "no":
            uscita = 0
        return uscita
    
    def mostra_cronologia_mosse(self):
        print("|------------------------------\
-----------------------------------------|")
        print("|====---> Cronologia delle mosse:")
        k = 1
        for i in range(0, len(self.cronologia_mosse), 2):
            print(f"|                                   {k}.",end="")
            for _j in range(0,2):
                if i!=len(self.cronologia_mosse):
                    print(" ",self.cronologia_mosse[i],end="")
                    i = i + 1
                else:
                    print("  ",end="")
            print("")
            k = k + 1
        print("|-------------------------------------\
----------------------------------|")
            
    def patta(self):
        print("|----------------------------------------------\
-------------------------|")
        print("|              Giocatore",self.avversario,"confermi la patta? (si o no)")
        print("|----------------------------------------------\
-------------------------|")
        print(" V")
        print(self.avversario, " :", end="")
        i=input()
        while i!="si" and i!= "no":
            print("|==============------> Prova a scrivere solo si o no (minuscoli)")
            i = input()
        if i == "si": 
            partita_finita = 1
            self.partita_iniziata = 0 
            print(" _______________________________\
________________________________________")
            print("|                                 \
                                      |")
            print("|                     E' stata dichiarata patta!! \
                      |")
            print("|                                 \
                                      |")
            
        if i== "no":
            partita_finita= 0
        return partita_finita
    
    def stampa_scacco(self, colore):
        print("|=====---> Il re del giocatore", colore, "si trova sotto scacco!!")
        print("|=======--------> Giocatore", colore,"libera il re !!")

    def stampa_scacco_matto(self, colore):
        print( "\n  ___________________________\
__________________________________________ ")
        print( " /                             \
                                        \\")
        print( "|========-----> Il giocare", colore,\
 "ha vinto per Scacco-Matto  !!!        ")
        print( "|                                   \
                                    |")

    def stampa_stallo(self):
        print( "\n                    __________________________________")
        print( "|==========---------|  Si è verificato uno Stallo !! \
|--------==========|")
        print( "|                                       \
                                |")

    def benvenuto(self):
        messaggio = [
        "|===================--------------------------------====================|",
        "|                                                                       |",
        "|   |-|-|-|                                                   |-|-|-|   |",
        "    |.....|                                                   |.....|",
        "     \\___/                                                     \\___/",
        "      | |                                                       | |",
        "      | |                                                       | |",
        "      |_|                                                       | |",
        "     /___\\                                                     /___\\",
        "    [_____] 	 _______________________________________      [_____]",
        "   /       \\     |                                     |     /       \\",
        " _|_________|_  _|  Benvenuto al gioco degli scacchi!! |_  _|_________|_",
        "|================|_____________________________________|================|",
        "._______________________________________________________________________.",
        "|                                                                       |",
        "|====| Digita un comando per cominciare |===============================|",
        "\\_______________________________________________________________________|" ]
        for riga in messaggio:
            print(riga)
        print(" V")

    def addio(self):
        messaggio = [
        "|===================--------------------------------====================|",
        "|                                                                       |",
        "|                                                                       |",
        "       _                                                         _",
        "     _/_\\_                                                     _/_\\_",
        "    |     |                                                   |     |",
        "   (-------)                                                 (-------)",
        "    \\	  /                                                   \\     /",
        "     |___|                                                     |___|",
        "    [_____] 	 _______________________________________      [_____]",
        "   /       \\     |                                     |     /       \\",
        " _|_________|_  _|  	 Grazie di aver giocato!!      |_  _|_________|_",
        "|================|_____________________________________|================|",
        "._______________________________________________________________________." ]
        for riga in messaggio:
            print(riga)
        print("")

    def partita_finita(self):
        messaggio = [
        "/=====================-----------------------------=====================\\",
        "|                  ___________________________________                  |",
        "|                 /                                   \\                 |",
        "|=========------ |        La partita è finita          | ------=========|", 
        "|                 \\___________________________________/                 |",
        "|_______________________________________________________________________|",
        " |                     _________________________                       |",
        " |==================-- |   Digita un comando   | --====================|",
        " \\_____________________\\________(/help)________/______________________/"]

        for riga in messaggio:
            print(riga)
        print("  V")
