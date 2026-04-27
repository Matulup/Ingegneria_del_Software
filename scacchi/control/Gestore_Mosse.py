import copy

from scacchi.entity.Scacchiera import Scacchiera


class Gestore_Mosse:
    """<<Control>>.

    Classe che contiene una scacchiera ed effettua le mosse passate. 
    - Permette di Usare i pezzi effettuando tutti i controlli necessari (sia per
        muovere i pezzi, sia per catturare).
    - Consente di verificare se il re è sotto Scacco.
    - Permette di verificare se è stato provocato uno Scacco Matto.
    - Permette di verificare se è stata provocata una situazione di Stallo.
    """

    def __init__(self):
        self.scacchiera = Scacchiera()
        self.possibile_en_passant = 0
        self.colore_en_passant = "Nero"
        self.colonna_en_passant = 0
        self.riga_en_passant = 0

    def gestore(self, mossa, colore, colore_avversario):
        # Funzione principale che, in base al pezzo che viene interpellato dalla mossa,
        # inoltra la gestione della mossa alla fuonzione di utilizzo associata 
        # al pezzo ( Usa_Pedone(), Usa_Torre(), ecc ).
        # Restituisce un valore che indica la correttezza/validità della mossa passata
        # input:
        # - mosa: generica mossa da valutare ed effettuare
        # - colore: colore del pezzo da utilizzare (cioè il colore del giocatore)
        # output:
        #  1) 0 se la mossa non è valida (Errore)
        #  2) 1 se la mossa è andata a buon fine
        #  3) 2 se la mossa potrebbe essere effettuata da più pezzi 
        #  4) 5 se la mossa ha messo sotto scacco l'avversario 
        # #
        flag = 0
        if len(mossa) < 7 and len(mossa) > 0:
            match mossa[0]: #match = switch 
                case 'A': # Per chiamare la funzione che muove l'Alfiere
                    if mossa[0]=='A' and len(mossa)<=5:
                        flag = self.Usa_Alfiere(mossa, colore)
                        if flag == 1:
                            self.possibile_en_passant = 0

                case 'C': # Per chiamare la funzione che muove il Cavallo
                    if mossa[0]=='C' and len(mossa)<=5:
                        flag = self.Usa_Cavallo(mossa, colore)
                        if flag == 1:
                            self.possibile_en_passant = 0

                case 'T': # Per chiamare la funzione che muove la Torre
                    if mossa[0]=='T' and len(mossa)<=5:
                        flag = self.Usa_Torre(mossa, colore)
                        if flag == 1:
                            self.possibile_en_passant = 0

                case 'R': # Per chiamare la funzione che muove il Re
                    flag = self.Usa_Re(mossa, colore)
                    if flag == 1:
                            self.possibile_en_passant = 0

                case 'D': # Per chiamare la funzione che muove la Donna
                    if mossa[0]=='D' and len(mossa)<=5:
                        flag = self.Usa_Donna(mossa, colore)
                        if flag == 1:
                            self.possibile_en_passant = 0
                
                case "0":
                    flag=self.arrocco(mossa,colore)
                    if flag == 1:
                            self.possibile_en_passant = 0


                case _:  # Per chiamare la funzione che muove il Pedone
                    if (mossa[0]>='a' and mossa[0]<='h') or \
                        (mossa[0] == 'x'  and \
                    mossa[1] >= 'a' and mossa[1] <= 'h' and \
                    mossa[2] >= '1' and mossa[2] <= '8' and len(mossa)<4) or \
                        (mossa[0]=='x' and len(mossa)<=6): 
                        flag = self.Usa_Pedone(mossa, colore)      

        if self.mossa_legale(colore_avversario) == 3:
            flag = 5
            if self.possibile_scacco_matto(colore_avversario) == 1:
                flag = 6
        else:
            if self.possibile_stallo(colore_avversario) == 1:
                flag = 7
           
        return flag



    def possibile_stallo(self, colore):
        # il colore che potrebbe andare in stallo
        # restituisce 1 se si è verificato lo stallo
        flag = 1
        i = 0
        temp_scacchiera = copy.deepcopy(self.scacchiera)
        temp_possibile_en_passant = self.possibile_en_passant 
        temp_colore_en_passant = self.colore_en_passant 
        temp_colonna_en_passant = self.colonna_en_passant
        temp_riga_en_passant = self.riga_en_passant


        while flag == 1 and i < 8:
            j = 0
            while flag == 1 and j < 8:
                pezzo = self.scacchiera.get_pezzo(i,j)
                if pezzo.get_nome()!= "Vuoto" and pezzo.get_colore() == colore:
                    match pezzo.get_nome():
                        case "Alfiere":
                            for i_ in range(0,8):
                                for j_ in range(0,8):
                                    pezzo_temp = self.scacchiera.get_pezzo(i_,j_)
                                    # alfiere si potrebbe spostare senza cattura
                                    if pezzo_temp.get_nome() == "Vuoto":
                                        if pezzo.mossa_lecita(i,j, i_, j_) == 1 and \
                                        self.alfiere_ha_pista_libera(i,j,i_,j_) == 1:
                                            if self.prova_mossa(i,j,i_,j_)== 1:
                                                
                                                self.possibile_en_passant = \
                                                    temp_possibile_en_passant 
                                                self.colore_en_passant = \
                                                    temp_colore_en_passant 
                                                self.colonna_en_passant = \
                                                      temp_colonna_en_passant
                                                self.riga_en_passant = \
                                                      temp_riga_en_passant
                                                self.scacchiera = temp_scacchiera
                                                return 0
                                            else:
                                                pass
                                    # alfiere si potrebbe spostare con cattura
                                    elif pezzo_temp.get_colore() != colore:
                                        if pezzo.cattura_lecita(i,j, i_, j_) == 1 and \
                                        self.alfiere_ha_pista_libera(i,j,i_,j_) == 1:
                                            if self.prova_mossa(i,j,i_,j_)== 1:
                                                self.possibile_en_passant = \
                                                    temp_possibile_en_passant 
                                                self.colore_en_passant = \
                                                    temp_colore_en_passant 
                                                self.colonna_en_passant = \
                                                    temp_colonna_en_passant
                                                self.riga_en_passant = \
                                                    temp_riga_en_passant
                                                self.scacchiera = \
                                                    temp_scacchiera
                                                return 0
                                        else:
                                            pass
                                    
                                    else:
                                        pass


                        case "Torre":
                            for i_ in range(0,8):
                                for j_ in range(0,8):
                                    pezzo_temp = self.scacchiera.get_pezzo(i_,j_)
                                    # torre si potrebbe spostare senza cattura
                                    if pezzo_temp.get_nome() == "Vuoto":
                                        if pezzo.mossa_lecita(i,j, i_, j_) == 1 and\
                                         self.torre_ha_pista_libera(i,j,i_,j_) == 1:
                                            if self.prova_mossa(i,j,i_,j_)== 1:
                                                self.possibile_en_passant = \
                                                    temp_possibile_en_passant 
                                                self.colore_en_passant = \
                                                    temp_colore_en_passant 
                                                self.colonna_en_passant = \
                                                    temp_colonna_en_passant
                                                self.riga_en_passant = \
                                                    temp_riga_en_passant
                                                self.scacchiera = \
                                                    temp_scacchiera
                                                return 0
                                        else:
                                            pass

                                    # torre si potrebbe spostare con cattura
                                    elif pezzo_temp.get_colore() != colore:
                                        if pezzo.cattura_lecita(i,j, i_, j_) == 1 and \
                                        self.torre_ha_pista_libera(i,j,i_,j_) == 1:
                                            if self.prova_mossa(i,j,i_,j_)== 1:
                                                self.possibile_en_passant = \
                                                    temp_possibile_en_passant 
                                                self.colore_en_passant = \
                                                    temp_colore_en_passant 
                                                self.colonna_en_passant = \
                                                    temp_colonna_en_passant
                                                self.riga_en_passant = \
                                                    temp_riga_en_passant
                                                self.scacchiera = \
                                                    temp_scacchiera
                                                return 0
                                        else:
                                            pass
                                    else:
                                        pass


                        case "Donna":
                            for i_ in range(0,8):
                                for j_ in range(0,8):
                                    pezzo_temp = self.scacchiera.get_pezzo(i_,j_)
                                    # donna si potrebbe spostare senza cattura
                                    if pezzo_temp.get_nome() == "Vuoto":
                                        if pezzo.mossa_lecita(i,j, i_, j_) == 1 and \
                                        self.donna_ha_pista_libera(i,j,i_,j_) == 1:
                                            if self.prova_mossa(i,j,i_,j_)== 1:
                                                self.possibile_en_passant = \
                                                    temp_possibile_en_passant 
                                                self.colore_en_passant = \
                                                    temp_colore_en_passant 
                                                self.colonna_en_passant = \
                                                    temp_colonna_en_passant
                                                self.riga_en_passant = \
                                                    temp_riga_en_passant
                                                self.scacchiera = \
                                                    temp_scacchiera
                                                return 0
                                        else:
                                            pass
                                    
                                    # donna si potrebbe spostare con cattura
                                    elif pezzo_temp.get_colore() != colore:
                                        if pezzo.cattura_lecita(i,j, i_, j_) == 1 and\
                                         self.donna_ha_pista_libera(i,j,i_,j_) == 1:
                                            if self.prova_mossa(i,j,i_,j_)== 1:
                                                self.possibile_en_passant = \
                                                    temp_possibile_en_passant 
                                                self.colore_en_passant = \
                                                    temp_colore_en_passant 
                                                self.colonna_en_passant = \
                                                    temp_colonna_en_passant
                                                self.riga_en_passant = \
                                                    temp_riga_en_passant
                                                self.scacchiera = \
                                                    temp_scacchiera
                                                return 0
                                        else:
                                            pass
                                    else:
                                        pass


                        case "Pedone":
                            for i_ in range(0,8):
                                for j_ in range(0,8):
                                    pezzo_temp = self.scacchiera.get_pezzo(i_,j_)
                                    # pedone si potrebbe spostare senza cattura
                                    if pezzo_temp.get_nome() == "Vuoto":
                                        if pezzo.mossa_lecita(i,j, i_, j_) == 1:
                                            if self.prova_mossa(i,j,i_,j_)== 1:
                                                self.possibile_en_passant = \
                                                    temp_possibile_en_passant 
                                                self.colore_en_passant = \
                                                    temp_colore_en_passant 
                                                self.colonna_en_passant = \
                                                    temp_colonna_en_passant
                                                self.riga_en_passant = \
                                                    temp_riga_en_passant
                                                self.scacchiera = \
                                                    temp_scacchiera

                                                return 0

                                        else:#se potrebbe fare l'en passant
                                            pass #En passant

                                    # pedone si potrebbe spostare con cattura
                                    elif pezzo_temp.get_colore() != colore:
                                        if pezzo.cattura_lecita(i,j, i_, j_) == 1:
                                            if self.prova_mossa(i,j,i_,j_)== 1:
                                                self.possibile_en_passant = \
                                                    temp_possibile_en_passant 
                                                self.colore_en_passant = \
                                                    temp_colore_en_passant 
                                                self.colonna_en_passant = \
                                                    temp_colonna_en_passant
                                                self.riga_en_passant = \
                                                    temp_riga_en_passant
                                                self.scacchiera = \
                                                    temp_scacchiera
                                                return 0
                                        else:
                                            pass
                                    else:
                                        pass

                            
                        case "Cavallo":
                            for i_ in range(0,8):
                                for j_ in range(0,8):
                                    pezzo_temp = self.scacchiera.get_pezzo(i_,j_)
                                    # cavallo si potrebbe spostare senza cattura
                                    if pezzo_temp.get_nome() == "Vuoto":
                                        if pezzo.mossa_lecita(i,j, i_, j_) == 1 :
                                            if self.prova_mossa(i,j,i_,j_) == 1:
                                                self.possibile_en_passant = \
                                                    temp_possibile_en_passant 
                                                self.colore_en_passant = \
                                                    temp_colore_en_passant 
                                                self.colonna_en_passant = \
                                                    temp_colonna_en_passant
                                                self.riga_en_passant = \
                                                    temp_riga_en_passant
                                                self.scacchiera = \
                                                    temp_scacchiera
                                                return 0
                                        else:
                                            pass

                                    # cavallo si potrebbe spostare con cattura
                                    elif pezzo_temp.get_colore() != colore:
                                        if pezzo.cattura_lecita(i,j, i_, j_) == 1:
                                            if self.prova_mossa(i,j,i_,j_)== 1:
                                                self.possibile_en_passant = \
                                                    temp_possibile_en_passant 
                                                self.colore_en_passant = \
                                                    temp_colore_en_passant 
                                                self.colonna_en_passant = \
                                                    temp_colonna_en_passant
                                                self.riga_en_passant = \
                                                    temp_riga_en_passant
                                                self.scacchiera = \
                                                    temp_scacchiera
                                                return 0
                                        else:
                                            pass
                                    else:
                                        pass
                        case "Re":
                            if self.re_potrebbe_muoversi(colore, i, j) == 0:
                                flag = 1
                            else: 
                                flag = 0
      
                j = j + 1
            i = i + 1

        return flag

    def re_potrebbe_muoversi(self, colore_re, i_re, j_re):
        flag = 0
        temp_scacchiera = copy.deepcopy(self.scacchiera)
        temp_possibile_en_passant = self.possibile_en_passant 
        temp_colore_en_passant = self.colore_en_passant 
        temp_colonna_en_passant = self.colonna_en_passant
        temp_riga_en_passant = self.riga_en_passant

         
        if self.scacchiera.get_pezzo(i_re, j_re).get_nome()=="Re" \
        and self.scacchiera.get_pezzo(i_re, j_re).get_colore()== colore_re:
            
            # si cerca una possibile mossa nella riga precedente e quella successiva
            i_temp = i_re - 1
            while flag == 0 and i_temp <= i_re + 1:
                j_temp = j_re - 1
                while flag == 0 and j_temp <= j_re + 1:
                    arrivo = str(self.scacchiera.converti_ascissa_algebrica(j_temp))\
                     + str(self.scacchiera.converti_ordinata_algebrica(i_temp))
                    mossa_spostamento = "R" + arrivo
                    mossa_cattura = "Rx" + arrivo
                    if self.Usa_Re(mossa_spostamento, colore_re) == 1 or \
                    self.Usa_Re(mossa_cattura, colore_re) == 1:
                        flag = 1
                        self.scacchiera = temp_scacchiera


                    j_temp = j_temp + 1
                
                i_temp = i_temp + 2
            
            #cerchiamo nella stessa riga, prima a sinistra e poi a destra
            j_temp = j_re - 1
            while flag == 0 and j_temp <= j_re + 1:
                arrivo = str(self.scacchiera.converti_ascissa_algebrica(j_temp)) \
                + str(self.scacchiera.converti_ordinata_algebrica(i_re))
                mossa_spostamento = "R" + arrivo
                mossa_cattura = "Rx" + arrivo
                if self.Usa_Re(mossa_spostamento, colore_re) == 1 or\
                self.Usa_Re(mossa_cattura, colore_re) == 1:
                    flag = 1
                    self.scacchiera = temp_scacchiera

                j_temp = j_temp + 2

        self.possibile_en_passant = temp_possibile_en_passant 
        self.colore_en_passant = temp_colore_en_passant 
        self.colonna_en_passant = temp_colonna_en_passant
        self.riga_en_passant = temp_riga_en_passant

        return flag

    def possibile_scacco_matto(self, colore_re):
        # colore_re : colore del re che potrebbe aver subito uno scacco matto
        # restituisce: 0 se non è scacco matto
        #              1 se è scacco matto
        flag = 0
        caselle_incriminate = []
        caselle_dei_criminali = []

        # si individua il re che si trova sotto scacco 
        i = 0
        i_re = j_re = 0
        trovato = 0
        while i < 8 and trovato == 0:
            j = 0
            while j < 8 and trovato == 0:
                if self.scacchiera.get_pezzo(i,j).get_nome()=="Re" and\
                self.scacchiera.get_pezzo(i,j).get_colore()==colore_re:
                    i_re = i
                    j_re = j
                    trovato = 1
                j = j + 1
            i = i + 1 

        if self.re_potrebbe_muoversi(colore_re, i_re, j_re) == 0:
            #se il re effettivamente non può muoversi

            #vediamo su quali caselle si può intervenire per evitare lo scacco
            i = 0
            while i < 8:
                j = 0
                while j < 8:
                    if self.scacchiera.get_pezzo(i,j).get_nome() != "Vuoto"\
                        and self.scacchiera.get_pezzo(i,j).get_colore() != colore_re:
                        i_temp = j_temp = 0
                        match self.scacchiera.get_pezzo(i,j).get_nome():
                            case 'Pedone':
                                if self.scacchiera.get_pezzo(i,j).cattura_lecita(i,\
                                j, i_re, j_re ) == 1:
                                    
                                    coordinate = str(i)+str(j) 
                                    # aggiungiamo la casella del Pedone
                                    caselle_dei_criminali.append(coordinate)
                                    
                            case 'Alfiere': 
                                # Per chiamare la funzione che muove l'Alfiere
                                if (self.scacchiera.get_pezzo(i,j).cattura_lecita(i,\
                                j, i_re, j_re )==1 and self.alfiere_ha_pista_libera(i,\
                                j,i_re, j_re)):
                                    coordinate = str(i)+str(j) 
                                    #aggiungiamo la casella dell'alfiere
                                    caselle_dei_criminali.append(coordinate)
                                    if i_re < i: #re si trova in alto
                                        i_temp = i - 1
                                        if j_re > j: #re si trova in alto a destra
                                            j_temp = j + 1
                                            while (j_temp<j_re):
                                                coordinate = str(i_temp)+str(j_temp) 
                                                caselle_incriminate.append(coordinate)
                                                j_temp = j_temp + 1
                                                i_temp = i_temp -1

                                        else: #re si trova in alto a sinistra
                                            j_temp = j - 1
                                            while (j_temp > j_re):
                                                coordinate = str(i_temp)+str(j_temp) 
                                                caselle_incriminate.append(coordinate)
                                                j_temp = j_temp - 1
                                                i_temp = i_temp - 1
                                            
                                    else: #re si trova in basso 
                                        i_temp = i + 1
                                        if j_re >j: #alfiere va in basso a destra
                                            j_temp = j + 1
                                            while (j_temp < j_re):
                                                coordinate = str(i_temp)+str(j_temp) 
                                                caselle_incriminate.append(coordinate)
                                                j_temp = j_temp + 1
                                                i_temp = i_temp + 1
                                        else: #va in basso a sinistra
                                            j_temp = j - 1
                                            while (j_temp > j_re):
                                                coordinate = str(i_temp)+str(j_temp) 
                                                caselle_incriminate.append(coordinate)
                                                j_temp = j_temp - 1
                                                i_temp = i_temp + 1

                            case 'Cavallo': 
                                # Per chiamare la funzione che muove il Cavallo
                                if (self.scacchiera.get_pezzo(i,j).cattura_lecita( i, \
                                j,i_re, j_re) == 1):
                                    coordinate = str(i)+str(j) 
                                    # aggiungiamo la casella del cavallo
                                    caselle_dei_criminali.append(coordinate)

                            case 'Torre': # Per chiamare la funzione che muove la Torre
                                if (self.scacchiera.get_pezzo(i,j).cattura_lecita(i,\
                                j, i_re, j_re )==1 and self.torre_ha_pista_libera(i,\
                                j,i_re, j_re)):
                                    coordinate = str(i)+str(j) 
                                    # aggiungiamo la casella della torre
                                    caselle_dei_criminali.append(coordinate)

                                    if i == i_re: #il re si trova sulla stessa riga
                                        if j_re > j: # il re si trova a destra
                                            j_temp = j + 1
                                            while j_temp < j_re:
                                                coordinate = str(i)+str(j_temp) 
                                                caselle_incriminate.append(coordinate)
                                                j_temp = j_temp + 1
                                        else:# il re si trova a sinistra
                                            j_temp = j - 1
                                            while j_temp > j_re:
                                                coordinate = str(i)+str(j_temp) 
                                                caselle_incriminate.append(coordinate)
                                                j_temp = j_temp - 1

                                    else:# il re si trova sulla stessa colonna
                                        if i_re > i:# il re si trova in basso
                                            i_temp = i + 1
                                            while i_re > i_temp:
                                                coordinate = str(i_temp)+str(j) 
                                                caselle_incriminate.append(coordinate)
                                                i_temp = i_temp + 1
                                        else:#il re si trova in alto
                                            i_temp = i - 1
                                            while i_re < i_temp:
                                                coordinate = str(i_temp)+str(j) 
                                                caselle_incriminate.append(coordinate)
                                                i_temp = i_temp - 1

                            case 'Re': # Per chiamare la funzione che muove il Re
                                pass

                            case 'Donna': # Per chiamare la funzione che muove la Donna
                                if (self.scacchiera.get_pezzo(i,j).cattura_lecita( i, \
                                j,i_re, j_re)==1) and self.donna_ha_pista_libera(i, \
                                j,i_re, j_re ):
                                    coordinate = str(i)+str(j) 
                                    # aggiungiamo la casella della Donna
                                    caselle_dei_criminali.append(coordinate)

                                    if i == i_re: # se si trovano sulla stessa riga
                                        if j_re > j: # il re si trova a destra
                                            j_temp = j + 1
                                            while j_temp < j_re:
                                                coordinate = str(i)+str(j_temp) 
                                                caselle_incriminate.append(coordinate)
                                                j_temp = j_temp + 1
                                        else:# il re si trova a sinistra
                                            j_temp = j - 1
                                            while j_temp > j_re:
                                                coordinate = str(i)+str(j_temp) 
                                                caselle_incriminate.append(coordinate)
                                                j_temp = j_temp - 1
                                    elif j == j_re: # se si trovano sulla stessa colonna
                                        if i_re > i:# il re si trova in basso
                                            i_temp = i + 1
                                            while i_re > i_temp:
                                                coordinate = str(i_temp)+str(j) 
                                                caselle_incriminate.append(coordinate)
                                                i_temp = i_temp + 1
                                        else:#il re si trova in alto
                                            i_temp = i - 1
                                            while i_re < i_temp:
                                                coordinate = str(i_temp)+str(j) 
                                                caselle_incriminate.append(coordinate)
                                                i_temp = i_temp - 1
                                    else:
                                        if i_re < i: #re si trova in alto
                                            i_temp = i - 1
                                            if j_re > j: #re si trova in alto a destra
                                                j_temp = j + 1
                                                while (j_temp<j_re):
                                                    coordinate = str(i_temp) + \
                                                    str(j_temp) 
                                                    caselle_incriminate.\
                                                    append(coordinate)
                                                    j_temp = j_temp + 1
                                                    i_temp = i_temp -1

                                            else: #re si trova in alto a sinistra
                                                j_temp = j - 1
                                                while (j_temp > j_re):
                                                    coordinate =str(i_temp)+str(j_temp) 
                                                    caselle_incriminate.\
                                                    append(coordinate)
                                                    j_temp = j_temp - 1
                                                    i_temp = i_temp - 1
                                            
                                        else: #re si trova in basso 
                                            i_temp = i + 1
                                            if j_re >j: #alfiere va in basso a destra
                                                j_temp = j + 1
                                                while (j_temp < j_re):
                                                    coordinate =str(i_temp)+str(j_temp) 
                                                    caselle_incriminate.\
                                                    append(coordinate)
                                                    j_temp = j_temp + 1
                                                    i_temp = i_temp + 1
                                            else: #va in basso a sinistra
                                                j_temp = j - 1
                                                while (j_temp > j_re):
                                                    coordinate =str(i_temp)+str(j_temp) 
                                                    caselle_incriminate.\
                                                    append(coordinate)
                                                    j_temp = j_temp - 1
                                                    i_temp = i_temp + 1
                    j = j + 1
                i = i + 1

            # trovate le caselle che mettono il re in scacco, 
            # verifichiamo se questo è risolvibile

            # vediamo prima se qualcuno può salvare
            i_temp = 0
            flag = 0
            while i_temp < 8 and flag == 0:
                j_temp = 0
                while j_temp < 8 and flag == 0:
                    if self.scacchiera.get_pezzo(i_temp, j_temp).get_nome() != "Vuoto" \
                    and self.scacchiera.get_pezzo(i_temp, j_temp).get_colore() \
                    == colore_re :
                        if self.pezzo_puo_salvare(i_temp, j_temp,caselle_incriminate,\
                        caselle_dei_criminali, colore_re ) == 1:
                            return 0
                        else:
                            pass
                    j_temp = j_temp + 1
                i_temp = i_temp + 1

            return 1

        else:
            flag = 0

        return flag
    
    def pezzo_puo_salvare(self, i_partenza, j_partenza,caselle_incriminate,\
                                                    caselle_dei_criminali, colore):
        # controlla se il pezzo nella data posizione
        # può salvare il re dallo scacco sulla base 
        flag = 0
        temp_scacchiera = copy.deepcopy(self.scacchiera)
        temp_possibile_en_passant = self.possibile_en_passant 
        temp_colore_en_passant = self.colore_en_passant 
        temp_colonna_en_passant = self.colonna_en_passant
        temp_riga_en_passant = self.riga_en_passant


        if self.scacchiera.get_pezzo(i_partenza, j_partenza).get_colore() == colore:
            #verifichiamo se può mettersi in mezzo
            i = 0
            while i < len(caselle_incriminate) and flag == 0:
                i_arrivo = int(caselle_incriminate[i][0])
                j_arrivo = int(caselle_incriminate[i][1])
                arrivo = str(self.scacchiera.converti_ascissa_algebrica(j_arrivo))\
                + str(self.scacchiera.converti_ordinata_algebrica(i_arrivo))

                if self.scacchiera.get_pezzo(i_partenza, j_partenza).mossa_lecita(\
                i_partenza, j_partenza, i_arrivo, j_arrivo):
                    match self.scacchiera.get_pezzo(i_partenza, j_partenza).get_nome():
                        case 'Alfiere':
                            if(self.Usa_Alfiere("A"+arrivo, colore) == 0):
                                flag = 0
                            elif(self.Usa_Alfiere("A"+arrivo, colore) == 2):
                                #controlliamo la riga
                                match self.Usa_Alfiere("A"+self.scacchiera.\
                                converti_ascissa_algebrica(j_partenza)+arrivo, colore):
                                    case 2:
                                        if self.Usa_Alfiere("A"+self.scacchiera.\
                                        converti_ordinata_algebrica(i_partenza)+\
                                        arrivo, colore) == 0:
                                            flag = 0
                                        else: 
                                            flag = 1
                                    case 1: 
                                        flag = 1
                            else :
                                flag = 1
                            
                        case 'Torre':
                            if(self.Usa_Torre("T" + arrivo, colore) == 0):
                                flag = 0
                            elif(self.Usa_Torre("T"+arrivo, colore) == 2):
                                #controlliamo la riga
                                match self.Usa_Torre("T"+self.\
                                scacchiera.converti_ascissa_algebrica(j_partenza)\
                                +arrivo, colore):
                                    case 2:
                                        if self.Usa_Torre("T"+self.\
                                        scacchiera.converti_ordinata_algebrica(\
                                        i_partenza)+arrivo, colore) == 0:
                                            flag = 0
                                        else: 
                                            flag = 1
                                    case 1: 
                                        flag = 1
                            else :
                                flag = 1

                        case 'Donna':
                            if(self.Usa_Donna("D" + arrivo, colore) == 0):
                                flag = 0
                            elif(self.Usa_Donna("D"+arrivo, colore) == 2):
                                #controlliamo la riga
                                match self.Usa_Donna("D"+\
                                self.scacchiera.converti_ascissa_algebrica(\
                                j_partenza) + arrivo, colore):
                                    case 2:
                                        if self.Usa_Donna("D"+self.scacchiera.\
                                        converti_ordinata_algebrica(i_partenza)+\
                                        arrivo, colore) == 0:
                                            flag = 0
                                        else: 
                                            flag = 1
                                    case 1: 
                                        flag = 1
                            else :
                                flag = 1

                        case 'Cavallo':
                            if(self.Usa_Cavallo("C" + arrivo, colore) == 1):
                                flag = 1
                            elif(self.Usa_Cavallo("C"+arrivo, colore) == 2):
                                #controlliamo la riga
                                match self.Usa_Cavallo("C"+\
                                self.scacchiera.converti_ascissa_algebrica(\
                                j_partenza)+arrivo, colore):
                                    case 2:
                                        if self.Usa_Cavallo("C"+self.scacchiera.\
                                        converti_ordinata_algebrica(i_partenza) + \
                                        arrivo, colore) == 0:
                                            flag = 0
                                        else: 
                                            flag = 1
                                    case 1: 
                                        flag = 1
                            else:
                                flag = 0

                        case 'Pedone':

                            flag = 0 if self.Usa_Pedone(arrivo, colore) == 0 else 1

                i = i + 1

            # verifichiamo se qualcuno può mangiare
            i = 0
            while flag == 0 and i < len(caselle_dei_criminali):
                i_arrivo = int(caselle_dei_criminali[i][0])
                j_arrivo = int(caselle_dei_criminali[i][1])
                arrivo = "x" + str(self.scacchiera.converti_ascissa_algebrica(\
                j_arrivo)) + str(self.scacchiera.converti_ordinata_algebrica(i_arrivo))

                if self.scacchiera.get_pezzo(i_partenza, j_partenza).cattura_lecita(\
                i_partenza, j_partenza, i_arrivo, j_arrivo):
                    match self.scacchiera.get_pezzo(i_partenza, j_partenza).get_nome():
                        case 'Alfiere':
                            if(self.Usa_Alfiere("A"+arrivo, colore) == 0):
                                flag = 0
                            elif(self.Usa_Alfiere("A"+arrivo, colore) == 2):
                                #controlliamo la riga
                                match self.Usa_Alfiere("A"+self.scacchiera.\
                                converti_ascissa_algebrica(j_partenza) + \
                                 arrivo, colore):
                                    case 2:
                                        if self.Usa_Alfiere("A"+\
                                        self.scacchiera.converti_ordinata_algebrica(\
                                        i_partenza)+arrivo, colore) == 0:
                                            flag = 0
                                        else: 
                                            flag = 1
                                    case 1: 
                                        flag = 1
                            else :
                                flag = 1

                        case 'Torre':
                            if(self.Usa_Torre("T" + arrivo, colore) == 0):
                                flag = 0
                            elif(self.Usa_Torre("T"+arrivo, colore) == 2):
                                #controlliamo la riga
                                match self.Usa_Torre("T"+self.\
                                scacchiera.converti_ascissa_algebrica(j_partenza)\
                                +arrivo, colore):
                                    case 2:
                                        if self.Usa_Torre("T"+\
                                        self.scacchiera.converti_ordinata_algebrica(\
                                        i_partenza)+arrivo, colore) == 0:
                                            flag = 0
                                        else: 
                                            flag = 1
                                    case 1: 
                                        flag = 1
                            else :
                                flag = 1

                        case 'Donna':
                            if(self.Usa_Donna("D" + arrivo, colore) == 0):
                                flag = 0
                            elif(self.Usa_Donna("D"+arrivo, colore) == 2):
                                #controlliamo la riga
                                match self.Usa_Donna("D"+self.scacchiera.\
                                converti_ascissa_algebrica(j_partenza)+\
                                arrivo, colore):
                                    case 2:
                                        if self.Usa_Donna("D"+\
                                        self.scacchiera.converti_ordinata_algebrica(\
                                        i_partenza)+arrivo, colore) == 0:
                                            flag = 0
                                        else: 
                                            flag = 1
                                    case 1: 
                                        flag = 1
                            else :
                                flag = 1

                        case 'Cavallo':
                            if(self.Usa_Cavallo("C" + arrivo, colore) == 0):
                                flag = 0
                            elif(self.Usa_Cavallo("C"+arrivo, colore) == 2):
                                #controlliamo la riga
                                match self.Usa_Cavallo("C"+\
                                self.scacchiera.converti_ascissa_algebrica(\
                                j_partenza)+arrivo, colore):
                                    case 2:
                                        if self.Usa_Cavallo("C"+self.scacchiera.\
                                        converti_ordinata_algebrica(i_partenza)+\
                                        arrivo, colore) == 0:
                                            flag = 0
                                        else: 
                                            flag = 1
                                    case 1: 
                                        flag = 1
                            else :
                                flag = 1

                        case 'Pedone':
                            if(self.Usa_Pedone(arrivo, colore) == 0):
                                flag = 0
                            elif (self.Usa_Pedone(arrivo, colore) == 2): 
                                if (self.Usa_Pedone(self.scacchiera.\
                                converti_ascissa_algebrica(j_partenza)\
                                +arrivo, colore) == 1 ):
                                #EN PASSANT
                                    flag = 1
                            else:
                                flag = 1

                i = i + 1

            if flag == 1:
                self.scacchiera = temp_scacchiera
                    
        self.possibile_en_passant = temp_possibile_en_passant 
        self.colore_en_passant = temp_colore_en_passant 
        self.colonna_en_passant = temp_colonna_en_passant
        self.riga_en_passant = temp_riga_en_passant

        return flag
    


    def Usa_Donna(self, mossa, colore):
        flag = 0
        if len(mossa)==3:#se si sposta senza specificare la colonna o la riga
            # se mossa è valida
            if mossa[1] >= 'a' and mossa[1] <= 'h' \
                and mossa[2] >= '1' and mossa[2] <= '8':
                #verifichiamo che sia è una semplice mossa (senza cattura)
                if self.scacchiera.get_pezzo(self.scacchiera.converti_ordinata_reale(\
                    int(mossa[2])),self.scacchiera.converti_ascissa_reale(mossa[1]))\
                        .get_nome()== "Vuoto":
                    flag = self.trova_e_sposta_donna(mossa, colore, 0)
                else:
                    flag = 0
            else:
                flag = 0
        else:
            #se si sposta specificando la colonna
            if len(mossa) == 4 and mossa[1]>='a' and mossa[1]<='h' \
                and mossa[2] >= 'a' and mossa[2] <= 'h' \
                and mossa[3] >= '1' and mossa[3] <= '8':
                if self.scacchiera.get_pezzo(self.scacchiera.converti_ordinata_reale(\
                int(mossa[3])),self.scacchiera.converti_ascissa_reale(mossa[2]))\
                .get_nome()== "Vuoto":
                    flag = self.trova_e_sposta_donna(mossa, colore, 1)
            else:# se si specifica la riga
                if len(mossa) == 4 and mossa[1]>='1' and mossa[1]<='8'\
                and mossa[2] >= 'a' and mossa[2] <= 'h' \
                and mossa[3] >= '1' and mossa[3] <= '8':
                    if self.scacchiera.get_pezzo(self.scacchiera\
                    .converti_ordinata_reale(int(mossa[3])),\
                    self.scacchiera.converti_ascissa_reale(mossa[2]))\
                    .get_nome()== "Vuoto":
                        flag = self.trova_e_sposta_donna(mossa, colore, 2)
                else:
                    #se vuole mangiare
                    if len(mossa) == 4 and mossa[1]=='x' and \
                    mossa[2] >= 'a' and mossa[2] <= 'h' and \
                    mossa[3] >= '1' and mossa[3] <= '8':
                        if self.scacchiera.get_pezzo(\
                        self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                        self.scacchiera.converti_ascissa_reale(mossa[2]))\
                        .get_nome() != "Vuoto" and self.scacchiera.get_pezzo(\
                        self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                        self.scacchiera.converti_ascissa_reale(mossa[2])).\
                        get_colore() != colore :
                            nuova_mossa = str(mossa[0])+str(mossa[2])+str(mossa[3])
                            flag = self.trova_e_sposta_donna(nuova_mossa, colore, 0)
                    else:
                        #se vuole mangiare specificando la colonna o la riga
                        if len(mossa) == 5 and mossa[2]=='x' and\
                        ((mossa[1]>='a' and mossa[1]<='h') or \
                        (mossa[1]>='1' and mossa[1]<='8') ) and \
                        mossa[3] >= 'a' and mossa[3] <= 'h' and \
                        mossa[4] >= '1' and mossa[4] <= '8':
                            nuova_mossa = str(mossa[0]) + str(mossa[1]) + \
                            str(mossa[3]) + str(mossa[4])
                            if (mossa[1]>='a' and mossa[1]<='h'):
                                flag = self.trova_e_sposta_donna(nuova_mossa, colore, 1)
                            else: 
                                flag = self.trova_e_sposta_donna(nuova_mossa, colore, 2)

        return flag

    def trova_e_sposta_donna(self, mossa, colore, riga_o_colonna):
        # riga_o_colonna è 0 se si sta cercando una generica donna
        #                  1 se si sta cercando la donna specificando la colonna
        #                  2 se si sta cercando la donna specificando la riga
        
        flag = 0
        trovati = 0
        i_copia = 0
        j_copia = 0

        if riga_o_colonna == 0:#se non specifica né colonna né riga
            i = 0
            while i<8 and trovati < 2 and flag <=2:
                j = 0
                while j<8 and trovati < 2:
                    if self.scacchiera.get_pezzo(i,j).get_nome()=="Donna" and\
                    self.scacchiera.get_pezzo(i,j).get_colore()==colore:

                        #se la donna è stata trovata, verifichiamo se 
                        #fa una mossa valida per lei
                        if self.scacchiera.get_pezzo(i,j).mossa_lecita(i,j,\
                        self.scacchiera.converti_ordinata_reale(int(mossa[2])),\
                        self.scacchiera.converti_ascissa_reale(mossa[1])) == 1:

                            #se la mossa è valida, verifichiamo che non ci siano pezzi 
                            #sul tragitto e indichiamo che abbiamo trovato una 
                            #delle possibili regine
                            if self.donna_ha_pista_libera(i, j, \
                            self.scacchiera.converti_ordinata_reale(int(mossa[2])),\
                            self.scacchiera.converti_ascissa_reale(mossa[1])) == 1:
                                trovati = trovati + 1
                                i_copia = i
                                j_copia = j
                            else:
                                flag = 0

                        else:
                            flag = 0
                            
                    j = j + 1
                i = i + 1

            if trovati == 1:
                trovati=self.prova_mossa(i_copia, j_copia, \
                self.scacchiera.converti_ordinata_reale(int(mossa[2])),\
                self.scacchiera.converti_ascissa_reale(mossa[1]))
               # self.scacchiera.sposta_pezzo(i_copia, j_copia, \
                #self.scacchiera.converti_ordinata_reale(int(mossa[2])),\
                #self.scacchiera.converti_ascissa_reale(mossa[1]))

        else:
            if riga_o_colonna == 1:# se si sta cercando su una colonna
                i = 0
                colonna = self.scacchiera.converti_ascissa_reale(str(mossa[1]))
                if colonna>=0 and colonna<=7:
                    while i < 8:
                        
                        if self.scacchiera.get_pezzo(i, colonna).get_nome()=="Donna" \
                        and self.scacchiera.get_pezzo(i,colonna).get_colore()==colore:

                            #se la donna è stata trovata, verifichiamo se 
                            #fa una mossa valida per lei
                            if self.scacchiera.get_pezzo(i,colonna).mossa_lecita(i,\
                            colonna,self.scacchiera.converti_ordinata_reale(\
                            int(mossa[3])),self.scacchiera.converti_ascissa_reale(\
                            mossa[2])) == 1:

                                #se la mossa è valida, verifichiamo che non ci siano 
                                #pezzi sul tragitto e indichiamo che abbiamo 
                                #trovato una delle possibili regine
                                if self.donna_ha_pista_libera(i, colonna, \
                                self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                                self.scacchiera.converti_ascissa_reale(mossa[2])) == 1:
                                    trovati = trovati + 1
                                    i_copia = i
                                    j_copia = colonna
                                else:
                                    flag = 0

                            else:
                                flag = 0
                        
                        i = i + 1

                    if trovati == 1:
                        trovati=self.prova_mossa(i_copia, j_copia, \
                        self.scacchiera.converti_ordinata_reale(int(mossa[3])), \
                        self.scacchiera.converti_ascissa_reale(mossa[2]))
                        #self.scacchiera.sposta_pezzo(i_copia, j_copia, \
                        #self.scacchiera.converti_ordinata_reale(int(mossa[3])), \
                        #self.scacchiera.converti_ascissa_reale(mossa[2]))
                else:
                    trovati = 0
            else:
                if riga_o_colonna == 2:
                    j = 0
                    riga = self.scacchiera.converti_ordinata_reale(int(mossa[1]))
                    if riga>=0 and riga<=7:
                        while j < 8:
                            if self.scacchiera.get_pezzo(riga, j).get_nome()=="Donna"\
                            and self.scacchiera.get_pezzo(riga, j).get_colore()==colore:

                                #se la donna è stata trovata, verifichiamo se 
                                #fa una mossa valida per lei
                                if self.scacchiera.get_pezzo(riga, j).\
                                mossa_lecita(riga, j,self.scacchiera.\
                                converti_ordinata_reale(int(mossa[3])), \
                                self.scacchiera.converti_ascissa_reale(mossa[2])) == 1:

                                    #se la mossa è valida, verifichiamo che non ci 
                                    #siano pezzi sul tragitto e indichiamo che abbiamo 
                                    #trovato una delle possibili regine
                                    if self.donna_ha_pista_libera(riga, j, \
                                    self.scacchiera.converti_ordinata_reale(\
                                    int(mossa[3])),self.scacchiera.\
                                    converti_ascissa_reale(mossa[2])) == 1:
                                        trovati = trovati + 1
                                        i_copia = riga
                                        j_copia = j
                                    else:
                                        flag = 0

                                else:
                                    flag = 0
                        
                            j = j + 1

                    if trovati == 1:
                        trovati=self.prova_mossa(i_copia, j_copia, \
                        self.scacchiera.converti_ordinata_reale(int(mossa[3])), \
                        self.scacchiera.converti_ascissa_reale(mossa[2]))
                        #self.scacchiera.sposta_pezzo(i_copia, j_copia, \
                        #self.scacchiera.converti_ordinata_reale(int(mossa[3])), \
                        #self.scacchiera.converti_ascissa_reale(mossa[2]))
                else:
                    trovati = 0
                    
        return trovati

    def donna_ha_pista_libera(self, i_partenza_reale, j_partenza_reale,\
                         i_arrivo_reale, j_arrivo_reale):
        flag = 1
        i_copia = i_partenza_reale
        j_copia = j_partenza_reale

        #si muove in riga
        if i_partenza_reale == i_arrivo_reale and j_partenza_reale != j_arrivo_reale:
            if j_partenza_reale > j_arrivo_reale: #verso sinistra
                while j_copia != j_arrivo_reale + 1 and flag == 1:
                    j_copia = j_copia -1
                    if self.scacchiera.get_pezzo(i_copia, j_copia).get_nome()!="Vuoto":
                        flag = 0
            else: #verso destra
                while j_copia != j_arrivo_reale - 1 and flag == 1:
                    j_copia = j_copia + 1
                    if self.scacchiera.get_pezzo(i_copia, j_copia).get_nome()!="Vuoto":
                        flag = 0
        else:
            #si muove in colonna
            if i_partenza_reale != i_arrivo_reale and j_partenza_reale ==j_arrivo_reale:
                if i_partenza_reale>i_arrivo_reale:#verso alto
                     while i_copia != i_arrivo_reale + 1 and flag == 1:
                        i_copia = i_copia - 1
                        if self.scacchiera.get_pezzo(i_copia, j_copia).\
                        get_nome()!="Vuoto":
                            flag = 0
                else:#verso il basso
                    while i_copia != i_arrivo_reale - 1 and flag == 1:
                        i_copia = i_copia + 1
                        if self.scacchiera.get_pezzo(i_copia, j_copia).\
                        get_nome()!="Vuoto":
                            flag = 0
            else:
                if i_arrivo_reale > i_partenza_reale:# va verso il basso
                    if j_arrivo_reale > j_partenza_reale: #va in basso a destra 
                        while flag == 1 and i_copia != i_arrivo_reale - 1:
                            i_copia = i_copia + 1
                            j_copia = j_copia + 1
                            if self.scacchiera.get_pezzo(i_copia, j_copia).\
                            get_nome()!="Vuoto":
                                flag = 0
                    else: #va in basso a sinistra
                        while flag == 1 and i_copia != i_arrivo_reale - 1:
                            i_copia = i_copia + 1
                            j_copia = j_copia - 1
                            if self.scacchiera.get_pezzo(i_copia, j_copia).\
                            get_nome()!="Vuoto":
                                flag = 0
                else:#va verso l'alto
                    if j_arrivo_reale > j_partenza_reale: #va in alto a destra 
                        while flag == 1 and i_copia != i_arrivo_reale + 1:
                            i_copia = i_copia - 1
                            j_copia = j_copia + 1
                            if self.scacchiera.get_pezzo(i_copia, j_copia).\
                            get_nome()!="Vuoto":
                                flag = 0
                    else: #va in alto a sinistra
                        while flag == 1 and i_copia != i_arrivo_reale + 1:
                            i_copia = i_copia - 1
                            j_copia = j_copia - 1
                            if self.scacchiera.get_pezzo(i_copia, j_copia).\
                            get_nome()!="Vuoto":
                                flag = 0

        return flag

        
    def Usa_Pedone(self, mossa, colore):
       # Funzione principale che usa un pedone: sulla base della mossa specificata 
        # sposta un pedone (o, in seguito, usa il pedone per catturare un altro pezzo).
        # Restituisce un valore che indica la riuscita dell'operazione
        # input:
        # - mossa: mossa che deve essere eseguita dal PEDONE, la mossa è descritta
        #          nella notazione algebrica corta o lunga
        # - colore: colore del pedone da usare
        # output:
        #  1) 0 se la mossa non è andata a buon fine(Errore)
        #  2) 1 se la mossa è andata a buon fine
        # #
        flag = 0
        if len(mossa) == 2: # nel caso di notazione corta
            # se la mossa in notazione corta è corretta
            if mossa[0] >= 'a' and mossa[0] <= 'h' and \
                mossa[1] > '1' and mossa[1] < '8':

                # mossa o cattura
                # pensare ad if: per controllare che la mossa non provochi uno scacco
                if self.scacchiera.get_pezzo( \
                    self.scacchiera.converti_ordinata_reale(int(mossa[1])), \
                        self.scacchiera.converti_ascissa_reale(mossa[0])).get_nome()\
                              == "Vuoto": #se è una semplice mossa (senza cattura)
                    
                    flag = self.Sposta_Pedone_Notazione_Corta(int(mossa[1]), \
                                                              (mossa[0]), colore)
            else:
                flag = 0    
                # pensare ad else: per la futura cattura con notazione corta
        else:
            
            if len(mossa) == 3:
                count = 0  
                
                if mossa[0] == 'x'  and \
                mossa[1] >= 'a' and mossa[1] <= 'h' and \
                mossa[2] > '1' and mossa[2] < '8':
                    
                    
                    if self.scacchiera.get_pezzo( \
                    self.scacchiera.converti_ordinata_reale(int(mossa[2])), \
                    self.scacchiera.converti_ascissa_reale(mossa[1])).get_nome()\
                    != "Vuoto" and self.scacchiera.get_pezzo( \
                    self.scacchiera.converti_ordinata_reale(int(mossa[2])), \
                    self.scacchiera.converti_ascissa_reale(mossa[1])).get_colore()\
                    != colore :
                        if colore =="Bianco":
                            i= self.scacchiera.converti_ordinata_reale(int(mossa[2]))+1
                        else :
                            i= self.scacchiera.converti_ordinata_reale(int(mossa[2]))-1
                        
                        j_temp = 0
                        for j in range(8):
                            if self.scacchiera.get_pezzo(i,j).get_nome() \
                            == "Pedone" and \
                            (self.scacchiera.get_pezzo(i,j).get_colore() \
                            == colore) :
                                if self.scacchiera.get_pezzo(i,j).cattura_lecita(i,j,\
                                self.scacchiera.converti_ordinata_reale(int(mossa[2])),\
                                self.scacchiera.converti_ascissa_reale(mossa[1])):
                                    count = count + 1
                                    j_temp = j
                            else:
                                pass
                                    
                                    
                        if count == 1:
                            flag=self.prova_mossa(i,j_temp,self.scacchiera.\
                            converti_ordinata_reale(int(mossa[2])),\
                            self.scacchiera.converti_ascissa_reale(mossa[1]))
                            if flag == 1:
                                self.scacchiera.get_pezzo(self.scacchiera.\
                                converti_ordinata_reale(int(mossa[2])),\
                                self.scacchiera.converti_ascissa_reale(mossa[1]))\
                                .set_prima_mossa()
                                self.possibile_en_passant = 0
                        else:
                            flag = 0 if count == 0 else 2 if count > 1 else 0
                else:
                    pass

            elif len(mossa)==4 and mossa[2]=="="and\
                mossa[0] >= 'a' and mossa[0] <= 'h' and \
                ((mossa[1] == '8' and colore=="Bianco") or (mossa[1] \
                == '1' and colore=="Nero")) and self.scacchiera.get_pezzo( \
                self.scacchiera.converti_ordinata_reale(int(mossa[1])), \
                self.scacchiera.converti_ascissa_reale(mossa[0])).get_nome()\
                == "Vuoto" :
                    #se è una semplice mossa (senza cattura)               
                    
                    match mossa[3]:
                        case 'A': # Per chiamare la funzione che muove l'Alfiere
                            flag=self.promozione(int(mossa[1]),mossa[0]\
                            , colore, self.scacchiera.get_alfiere(colore))
                        case 'C': # Per chiamare la funzione che muove il Cavallo
                            flag=self.promozione(int(mossa[1]),mossa[0]\
                            , colore, self.scacchiera.get_cavallo(colore))
                        case 'T': # Per chiamare la funzione che muove la Torre
                            flag=self.promozione(int(mossa[1]),mossa[0]\
                            , colore, self.scacchiera.get_torre(colore))
                        case 'D': # Per chiamare la funzione che muove la Donna
                            flag=self.promozione(int(mossa[1]),mossa[0]\
                            , colore, self.scacchiera.get_Donna(colore))
            elif len(mossa) == 4:
                if mossa[0] >= 'a' and mossa[0] <= 'h' and \
                    mossa[1] == 'x'  and \
                    mossa[2] >= 'a' and mossa[2] <= 'h' and \
                    mossa[3] > '1' and mossa[3] < '8':   
                    
                    if self.scacchiera.get_pezzo( \
                        self.scacchiera.converti_ordinata_reale(int(mossa[3])), \
                        self.scacchiera.converti_ascissa_reale(mossa[2])).get_nome()\
                        != "Vuoto" and self.scacchiera.get_pezzo( \
                        self.scacchiera.converti_ordinata_reale(int(mossa[3])), \
                        self.scacchiera.converti_ascissa_reale(mossa[2])).get_colore()\
                        != colore :
                        
                        if colore =="Bianco":
                            i= self.scacchiera.converti_ordinata_reale(int(mossa[3]))+1
                        else :
                            i= self.scacchiera.converti_ordinata_reale(int(mossa[3]))-1
                        j=self.scacchiera.converti_ascissa_reale(mossa[0])
                        if self.scacchiera.get_pezzo(i,j).get_nome() == "Pedone" \
                            and (self.scacchiera.get_pezzo(i,j).get_colore() \
                                 == colore) :
                            
                            if self.scacchiera.get_pezzo(i,j).cattura_lecita\
                                (i,j,self.scacchiera.converti_ordinata_reale\
                                 (int(mossa[3])),\
                                 self.scacchiera.converti_ascissa_reale(mossa[2])):
                                
                                flag = self.prova_mossa(i,j,\
                                self.scacchiera.converti_ordinata_reale(int(mossa[3]))\
                                ,self.scacchiera.converti_ascissa_reale(mossa[2]))
                                if flag == 1:
                                    self.possibile_en_passant = 0
                                    self.scacchiera.get_pezzo(self.scacchiera.\
                                    converti_ordinata_reale(int(mossa[3])),\
                                    self.scacchiera.converti_ascissa_reale(mossa[2]))\
                                    .set_prima_mossa()
                        else:
                            pass

                    elif self.possibile_en_passant == 1 :
                        if self.scacchiera.get_pezzo(\
                        self.scacchiera.converti_ordinata_reale(int(mossa[3]))\
                        ,self.scacchiera.converti_ascissa_reale(mossa[2])).\
                        get_nome() == "Vuoto":
                            c=1 if colore == "Bianco" else -1
                             
                            if(self.scacchiera.converti_ordinata_reale(int(mossa[3]))\
                            + c == self.riga_en_passant and \
                            self.scacchiera.converti_ascissa_reale(mossa[2])\
                            == self.colonna_en_passant and \
                            self.colore_en_passant != colore):
                                if self.scacchiera.get_pezzo(self.riga_en_passant,\
                                self.scacchiera.converti_ascissa_reale(mossa[0]))\
                                .get_nome() == "Pedone"\
                                and self.scacchiera.get_pezzo(self.riga_en_passant,\
                                self.scacchiera.converti_ascissa_reale(mossa[0])).\
                                get_colore() == colore:
                                    flag = self.prova_en_passant(self.riga_en_passant,\
                                    self.scacchiera.converti_ascissa_reale(mossa[0])\
                                    ,self.scacchiera.converti_ordinata_reale\
                                    (int(mossa[3])) + c\
                                    , self.scacchiera.converti_ascissa_reale(mossa[2]),\
                                    self.scacchiera.converti_ordinata_reale\
                                    (int(mossa[3]))\
                                    ,self.scacchiera.converti_ascissa_reale(mossa[2]))
                            else:
                                pass
                                    


                    else: 
                        flag=0
            elif len(mossa) == 6:
                if mossa[0] >= 'a' and mossa[0] <= 'h' and \
                    mossa[1] == 'x' and  \
                    mossa[2] >= 'a' and mossa[2] <= 'h' and \
                    mossa[3] >= '1' and mossa[3] <= '8' and \
                    mossa[4] == "=" :
                    if self.scacchiera.get_pezzo( \
                    self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                    self.scacchiera.converti_ascissa_reale(mossa[2])).get_nome()\
                    != "Vuoto" and self.scacchiera.get_pezzo( \
                    self.scacchiera.converti_ordinata_reale(int(mossa[3])), \
                    self.scacchiera.converti_ascissa_reale(mossa[2])).get_colore()\
                    != colore :
                            if colore =="Bianco":
                                i= self.scacchiera.converti_ordinata_reale\
                                (int(mossa[3]))+1
                            else :
                                i= self.scacchiera.converti_ordinata_reale\
                                    (int(mossa[3]))-1
                            match mossa[5]:
                                case 'A': # Per chiamare la funzione che muove l'Alfiere
                                    flag=self.cattura_con_promozione(mossa[0],\
                                    int(mossa[3]),mossa[2]\
                                    , colore, self.scacchiera.get_alfiere(colore))
                                case 'C':# Per chiamare la funzione che muove il Cavallo
                                    flag=self.cattura_con_promozione(mossa[0],\
                                    int(mossa[3]),mossa[2]\
                                    , colore, self.scacchiera.get_cavallo(colore))
                                case 'T': # Per chiamare la funzione che muove la Torre
                                    flag=self.cattura_con_promozione(mossa[0],\
                                    int(mossa[3]),mossa[2]\
                                    , colore, self.scacchiera.get_torre(colore))
                                case 'D': # Per chiamare la funzione che muove la Donna
                                    flag=self.cattura_con_promozione(mossa[0],\
                                    int(mossa[3]),mossa[2]\
                                    , colore, self.scacchiera.get_Donna(colore))
                else:
                    pass
                                
                
                    

        return flag
    def prova_en_passant (self,i_partenza,j_partenza,riga_primo_arrivo_reale,\
                          colonna_primo_arrivo_reale, riga_arrivo_finale\
                            , colonna_arrivo_finale):
        primo_pezzo_da_sostituire=self.scacchiera.get_pezzo(i_partenza, j_partenza)
        secondo_pezzo_da_sostituire=self.scacchiera.get_pezzo(riga_primo_arrivo_reale, \
                                                            colonna_primo_arrivo_reale)
        terzo_pezzo_da_sostituire=self.scacchiera.get_pezzo(riga_arrivo_finale, \
                                                            colonna_arrivo_finale)
        temp = self.possibile_en_passant
        temp_possibile_en_passant = self.possibile_en_passant 
        temp_colore_en_passant = self.colore_en_passant 
        temp_colonna_en_passant = self.colonna_en_passant
        temp_riga_en_passant = self.riga_en_passant


        self.scacchiera.sposta_pezzo(i_partenza,j_partenza,\
                                    riga_arrivo_finale, colonna_arrivo_finale)
        self.scacchiera.sposta_pezzo(i_partenza,j_partenza,\
                                    riga_primo_arrivo_reale, colonna_primo_arrivo_reale)
        self.possibile_en_passant = 0

        if (self.mossa_legale(self.scacchiera.get_pezzo( riga_arrivo_finale, \
            colonna_arrivo_finale).get_colore()) == 3):

            self.scacchiera.set(i_partenza,j_partenza, primo_pezzo_da_sostituire)
            self.scacchiera.set(riga_primo_arrivo_reale, colonna_primo_arrivo_reale, \
                                secondo_pezzo_da_sostituire)
            self.scacchiera.set(riga_arrivo_finale, colonna_arrivo_finale, \
                                terzo_pezzo_da_sostituire)
            self.possibile_en_passant = temp
            self.possibile_en_passant = temp_possibile_en_passant 
            self.colore_en_passant = temp_colore_en_passant 
            self.colonna_en_passant = temp_colonna_en_passant
            self.riga_en_passant = temp_riga_en_passant
            flag=3
        else:
            flag=1
        return flag    

    def promozione(self, riga_arrivo, colonna_arrivo, \
                   colore,pezzo):

        if colore=="Bianco":
            riga_partenza=self.scacchiera.converti_ordinata_reale(riga_arrivo-1)
        else:
            riga_partenza=self.scacchiera.converti_ordinata_reale(riga_arrivo+1)

        riga_arrivo_reale = self.scacchiera.converti_ordinata_reale(riga_arrivo)
        colonna_arrivo_reale = self.scacchiera.converti_ascissa_reale(colonna_arrivo)
        flag=0
        #(riga_partenza, \
        #colonna_arrivo_reale).get_nome(), self.scacchiera.get_pezzo(riga_partenza, \
        #colonna_arrivo_reale).get_colore() )

        if self.scacchiera.get_pezzo(riga_partenza, \
        colonna_arrivo_reale).get_nome()=="Pedone"and\
        self.scacchiera.get_pezzo(riga_partenza,\
        colonna_arrivo_reale).get_colore()==colore:
            self.scacchiera.set(riga_arrivo_reale,colonna_arrivo_reale,pezzo)
            self.scacchiera.set_vuoto(riga_partenza,colonna_arrivo_reale)
            flag=1
           ## elif colore=="Nero" and riga_arrivo_reale==1:
             #   set(riga_arrivo_reale,colonna_arrivo_reale,pezzo)
              #  self.scacchiera.set_vuoto(riga_partenza,colonna_arrivo_reale)
               # self.scacchiera.set(riga_arrivo_reale,colonna_arrivo_reale,)
                #flag=1
        
        return flag
    
    def cattura_con_promozione(self, colonna_partenza, riga_arrivo,\
        colonna_arrivo, colore,pezzo):

        if colore=="Bianco":
            riga_partenza=self.scacchiera.converti_ordinata_reale(riga_arrivo-1)
        else:
            riga_partenza=self.scacchiera.converti_ordinata_reale(riga_arrivo+1)

        riga_arrivo_reale = self.scacchiera.converti_ordinata_reale(riga_arrivo)
        colonna_arrivo_reale = self.scacchiera.converti_ascissa_reale(colonna_arrivo)
        colonna_partenza_reale= self.scacchiera.converti_ascissa_reale(colonna_partenza)
        flag=0
        
        if self.scacchiera.get_pezzo(riga_partenza, \
        colonna_partenza_reale).get_nome()=="Pedone"and\
        self.scacchiera.get_pezzo(riga_partenza,\
        colonna_partenza_reale).get_colore()==colore:
            self.scacchiera.set(riga_arrivo_reale,colonna_arrivo_reale,pezzo)
            self.scacchiera.set_vuoto(riga_partenza,colonna_partenza_reale)
            flag=1
           
        
        return flag
    
    def Sposta_Pedone_Notazione_Corta(self, riga_arrivo, colonna_arrivo, colore):
        # Sposta il pedone (l'unico compatibile con tale mossa) nella cella indicata
        # dalle coordinate espresse nella notazione algebrica formulate nella 
        # notazione corta.
        # Restituisce un valore che indica la riuscita dello spostamento
        # input:
        # - riga_arrivo: ordinata di arrivo espressa nel formato algebrico 
        #                (valori di input in [1,8] )
        # - colonna_arrivo: ascissa di arrivo espressa nel formato algebrico
        #                   (valori di input in  ['a','h'] ) 
        # - colore: colore del pezzo da spostare ("Bianco" o "Nero")
        # output: 
        #  1) 0 se nessun pedone può effettuare tale mossa (Errore)
        #  2) 1 se la mossa è andata a buon fine
        # #
        riga_arrivo_reale = self.scacchiera.converti_ordinata_reale(riga_arrivo)
        colonna_arrivo_reale = self.scacchiera.converti_ascissa_reale(colonna_arrivo)
        i = flag = 0
        while i < 8 and flag == 0:
            j = 0
            while j < 8 and flag == 0:
                if self.scacchiera.get_pezzo(i,j).get_nome() == "Pedone" and\
                      self.scacchiera.get_pezzo(i,j).get_colore() == colore:
                    if self.scacchiera.get_pezzo(i,j).mossa_lecita(\
                            i,j,riga_arrivo_reale,colonna_arrivo_reale) == 1:
                        if (self.scacchiera.get_pezzo(i,j).get_colore() == "Bianco" \
                            and self.scacchiera.get_pezzo(i-1,j).get_nome() == "Vuoto")\
                                  or (self.scacchiera.get_pezzo(i,j).get_colore() ==\
                                       "Nero" and \
                                        self.scacchiera.get_pezzo(i+1,j).get_nome() \
                                            == "Vuoto"):
                            #self.scacchiera.sposta_pezzo(i,j,riga_arrivo_reale, \
                                                         #colonna_arrivo_reale)

                            #flag = 1
                            flag = self.prova_mossa(i,j,riga_arrivo_reale, \
                                                    colonna_arrivo_reale)  
                             
                            if flag == 1:
                                self.scacchiera.get_pezzo(riga_arrivo_reale,\
                                colonna_arrivo_reale).set_prima_mossa()                        
                            if(abs(i-riga_arrivo_reale) == 2 and flag == 1):
                                self.possibile_en_passant = 1
                                self.colore_en_passant = colore
                                self.colonna_en_passant = colonna_arrivo_reale
                                self.riga_en_passant = riga_arrivo_reale
                            else:
                                self.possibile_en_passant = 0                    
                        else:
                            flag = 0
                    else:
                        flag = 0
                else :
                    flag = 0
                j = j + 1
            i = i + 1
        return flag
    
    
    def Usa_Re(self,mossa,colore):  # noqa: D103
     # Funzione principale che usa il re: sulla base della mossa specificata 
        # sposta re 
        # cattura con re
        # Restituisce un valore che indica la riuscita dell'operazione
        # input:
        # - mossa: mossa che deve essere eseguita dal re, la mossa è descritta
        #          nella notazione algebrica corta o lunga
        # - colore: colore del pedone da usare
        # output:
        #  1) 0 se la mossa non è andata a buon fine(Errore)
        #  2) 1 se la mossa è andata a buon fine
        # #
        flag = 0
        if mossa[0]== 'R' and mossa[1]>='a' and mossa[1] <= 'h' and \
            mossa[2] >= '1' and mossa[2] <= '8':  # noqa: SIM102

            # mossa o cattura
            # pensare ad if: per controllare che la mossa non provochi uno scacco
            if self.scacchiera.get_pezzo( \
                self.scacchiera.converti_ordinata_reale(int(mossa[2])), \
                    self.scacchiera.converti_ascissa_reale(mossa[1])).get_nome()\
                            == "Vuoto":
                
                flag = self.Sposta_Re_Notazione_Corta(int(mossa[2]), \
                                                            (mossa[1]), colore)

        elif (mossa[0] == 'R' and mossa[1]=='x'\
            and mossa[2]>='a' and mossa[2] <= 'h' and \
            mossa[3] >= '1' and mossa[3] <= '8')  :  # noqa: SIM102

            if self.scacchiera.get_pezzo( \
                self.scacchiera.converti_ordinata_reale(int(mossa[3])), \
                    self.scacchiera.converti_ascissa_reale(mossa[2])).get_nome() !=\
                        "Vuoto" and\
                self.scacchiera.get_pezzo( \
                self.scacchiera.converti_ordinata_reale(int(mossa[3])), \
                    self.scacchiera.converti_ascissa_reale(mossa[2])).get_colore()!=\
                        colore: 
                
                #se è una semplice mossa (senza cattura) 
                
                flag = self.Cattura_Re_Notazione_Corta\
                (int(mossa[3]), mossa[2], colore)


        return flag

    def Cattura_Re_Notazione_Corta(self, riga_arrivo, colonna_arrivo, colore):
        riga_arrivo_reale = self.scacchiera.converti_ordinata_reale(riga_arrivo)
        colonna_arrivo_reale = self.scacchiera.converti_ascissa_reale(colonna_arrivo)
        i = flag = 0
        while i < 8 and flag == 0:
            j = 0
            while j < 8 and flag == 0:
                if self.scacchiera.get_pezzo(i,j).get_nome() == "Re" \
                and self.scacchiera.get_pezzo(i,j).get_colore() == \
                    colore and self.scacchiera.get_pezzo(i,j)\
                        .cattura_lecita(i,j,riga_arrivo_reale\
                            ,colonna_arrivo_reale) == 1:
                    #vediamo se la mossa e lecita, nel caso in cui lo sia lo si esegue
                
                    #salviamo il pezzo catturato e poi muoviamo
                    flag=self.prova_mossa(i,j,riga_arrivo_reale,colonna_arrivo_reale)
                    
                    
                    
                j = j + 1
            i = i + 1
        return flag
    

    def Sposta_Re_Notazione_Corta(self, riga_arrivo, colonna_arrivo, colore):
        
        riga_arrivo_reale = self.scacchiera.converti_ordinata_reale(riga_arrivo)
        colonna_arrivo_reale = self.scacchiera.converti_ascissa_reale(colonna_arrivo)
        i = flag = 0
        while i < 8 and flag == 0:
            j = 0
            while j < 8 and flag == 0: 
                
                #vediamo se la mossa e lecita, nel caso in cui lo sia lo si esegue
                if self.scacchiera.get_pezzo(i,j).get_nome() == "Re" \
                and self.scacchiera.get_pezzo(i,j).get_colore() == colore\
                    and self.scacchiera.get_pezzo(i,j).mossa_lecita(\
                            i,j,riga_arrivo_reale,colonna_arrivo_reale):
                   
                    flag=self.prova_mossa(i,j,riga_arrivo_reale,colonna_arrivo_reale)

                    ####
                


                j = j + 1
            i = i + 1
        return flag     
    
    def Usa_Torre(self, mossa, colore):
        flag = 0
        
        if len(mossa)==3:#se si sposta senza specificare la colonna o la riga
            # se mossa è valida
            if mossa[1] >= 'a' and mossa[1] <= 'h' \
                and mossa[2] >= '1' and mossa[2] <= '8':
                #verifichiamo che sia è una semplice mossa (senza cattura)
                if self.scacchiera.get_pezzo(self.scacchiera.converti_ordinata_reale(\
                    int(mossa[2])),self.scacchiera.converti_ascissa_reale(mossa[1]))\
                        .get_nome()== "Vuoto":
                    flag = self.trova_e_sposta_torre(mossa, colore, 0)
                else:
                    flag = 0
            else:
                flag = 0
        else:
            #se si sposta specificando la colonna
            if len(mossa) == 4 and mossa[1]>='a' and mossa[1]<='h' \
                and mossa[2] >= 'a' and mossa[2] <= 'h' \
                and mossa[3] >= '1' and mossa[3] <= '8':
                if self.scacchiera.get_pezzo(self.scacchiera.converti_ordinata_reale(\
                int(mossa[3])),self.scacchiera.converti_ascissa_reale(mossa[2]))\
                .get_nome()== "Vuoto":
                    flag = self.trova_e_sposta_torre(mossa, colore, 1)
            else:# se si specifica la riga
                if len(mossa) == 4 and mossa[1]>='1' and mossa[1]<='8'\
                and mossa[2] >= 'a' and mossa[2] <= 'h' \
                and mossa[3] >= '1' and mossa[3] <= '8':
                    if self.scacchiera.get_pezzo(self.scacchiera\
                    .converti_ordinata_reale(int(mossa[3])),\
                    self.scacchiera.converti_ascissa_reale(mossa[2]))\
                    .get_nome()== "Vuoto":
                        flag = self.trova_e_sposta_torre(mossa, colore, 2)
                else:
                    #se vuole mangiare
                    if len(mossa) == 4 and mossa[1]=='x' and \
                    mossa[2] >= 'a' and mossa[2] <= 'h' and \
                    mossa[3] >= '1' and mossa[3] <= '8':
                        if self.scacchiera.get_pezzo(\
                        self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                        self.scacchiera.converti_ascissa_reale(mossa[2]))\
                        .get_nome() != "Vuoto" and self.scacchiera.get_pezzo(\
                        self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                        self.scacchiera.converti_ascissa_reale(mossa[2])).\
                        get_colore() != colore :
                            nuova_mossa = str(mossa[0])+str(mossa[2])+str(mossa[3])
                            flag = self.trova_e_sposta_torre(nuova_mossa, colore, 0)
                    else:
                        #se vuole mangiare specificando la colonna o la riga
                        if len(mossa) == 5 and mossa[2]=='x' and\
                        ((mossa[1]>='a' and mossa[1]<='h') or \
                        (mossa[1]>='1' and mossa[1]<='8') ) and \
                        mossa[3] >= 'a' and mossa[3] <= 'h' and \
                        mossa[4] >= '1' and mossa[4] <= '8':
                            nuova_mossa = str(mossa[0]) + str(mossa[1]) + \
                            str(mossa[3]) + str(mossa[4])
                            if (mossa[1]>='a' and mossa[1]<='h'):
    
                                flag = self.trova_e_sposta_torre(nuova_mossa, colore, 1)
                            else: 
                               
                                flag = self.trova_e_sposta_torre(nuova_mossa, colore, 2)

        return flag
    
    
    def trova_e_sposta_torre(self, mossa, colore, riga_o_colonna) :
         # riga_o_colonna è 0 se si sta cercando una generica torre
        #                  1 se si sta cercando la torre specificando la colonna
        #                  2 se si sta cercando la torre specificando la riga
        
        flag = 0
        trovati = 0
        i_copia = 0
        j_copia = 0

        if riga_o_colonna == 0:#se non specifica né colonna né riga
            i = 0
            while i<8 and trovati < 2 and flag <=2:
                j = 0
                while j<8 and trovati < 2:
                    if self.scacchiera.get_pezzo(i,j).get_nome()=="Torre" and\
                    self.scacchiera.get_pezzo(i,j).get_colore()==colore:

                        #se la torre è stata trovata, verifichiamo se 
                        #fa una mossa valida per lei
                        if self.scacchiera.get_pezzo(i,j).mossa_lecita(i,j,\
                        self.scacchiera.converti_ordinata_reale(int(mossa[2])),\
                        self.scacchiera.converti_ascissa_reale(mossa[1])) == 1:

                            #se la mossa è valida, verifichiamo che non ci siano pezzi 
                            #sul tragitto e indichiamo che abbiamo trovato una 
                            #delle possibili torri
                            if self.torre_ha_pista_libera(i, j, \
                            self.scacchiera.converti_ordinata_reale(int(mossa[2])),\
                            self.scacchiera.converti_ascissa_reale(mossa[1])) == 1:
                                trovati = trovati + 1
                                i_copia = i
                                j_copia = j
                            else:
                                flag = 0

                        else:
                            flag = 0
                            
                    j = j + 1
                i = i + 1

            if trovati == 1:
                trovati=self.prova_mossa(i_copia, j_copia, \
                self.scacchiera.converti_ordinata_reale(int(mossa[2])),\
                self.scacchiera.converti_ascissa_reale(mossa[1]))
            
                if trovati==1:
                    self.scacchiera.get_pezzo( self.scacchiera.\
                    converti_ordinata_reale(int(mossa[2])),\
                    self.scacchiera.converti_ascissa_reale\
                    (mossa[1])).set_Prima_Mossa()
                #self.scacchiera.sposta_pezzo(i_copia, j_copia, \
                #self.scacchiera.converti_ordinata_reale(int(mossa[2])),\
                #self.scacchiera.converti_ascissa_reale(mossa[1]))
                

        else:
            
            if riga_o_colonna == 1:# se si sta cercando su una colonna
                i = 0

                colonna = self.scacchiera.converti_ascissa_reale(str(mossa[1]))
                
                if colonna>=0 and colonna<=7:
                    while i < 8:
                        if self.scacchiera.get_pezzo(i, colonna).get_nome()=="Torre" \
                        and self.scacchiera.get_pezzo(i,colonna).get_colore()==colore:

                            #se la torre è stata trovata, verifichiamo se 
                            #fa una mossa valida per lei
                            if self.scacchiera.get_pezzo(i,colonna).mossa_lecita(i,\
                            colonna,self.scacchiera.converti_ordinata_reale(\
                            int(mossa[3])),self.scacchiera.converti_ascissa_reale(\
                            mossa[2])) == 1:

                                #se la mossa è valida, verifichiamo che non ci siano 
                                #pezzi sul tragitto e indichiamo che abbiamo 
                                #trovato una delle possibili torri
                                if self.torre_ha_pista_libera(i, colonna, \
                                self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                                self.scacchiera.converti_ascissa_reale(mossa[2])) == 1:
                                    trovati = trovati + 1
                                    i_copia = i
                                    j_copia = colonna
                                else:
                                    flag = 0

                            else:
                                flag = 0
                        
                        i = i + 1

                    if trovati == 1:
                       
                        trovati=self.prova_mossa(i_copia, j_copia, \
                        self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                        self.scacchiera.converti_ascissa_reale(mossa[2]))
                        
                    


                       # self.scacchiera.get_pezzo(i_copia,j_copia).set_Prima_Mossa()
                       # self.scacchiera.sposta_pezzo(i_copia, j_copia, \
                       # self.scacchiera.converti_ordinata_reale(int(mossa[3])), \
                       # self.scacchiera.converti_ascissa_reale(mossa[2]))
                else:
                    trovati = 0
            else:
                if riga_o_colonna == 2:
                    j = 0
                    riga = self.scacchiera.converti_ordinata_reale(int(mossa[1]))
                    if riga>=0 and riga<=7:
                        while j < 8:
                            if self.scacchiera.get_pezzo(riga, j).get_nome()=="Torre"\
                            and self.scacchiera.get_pezzo(riga, j).get_colore()==colore:

                                #se la torre è stata trovata, verifichiamo se 
                                #fa una mossa valida per lei
                                if self.scacchiera.get_pezzo(riga, j).\
                                mossa_lecita(riga, j,self.scacchiera.\
                                converti_ordinata_reale(int(mossa[3])), \
                                self.scacchiera.converti_ascissa_reale(mossa[2])) == 1:

                                    #se la mossa è valida, verifichiamo che non ci 
                                    #siano pezzi sul tragitto e indichiamo che abbiamo 
                                    #trovato una delle possibili torri
                                    if self.torre_ha_pista_libera(riga, j, \
                                    self.scacchiera.converti_ordinata_reale(\
                                    int(mossa[3])),self.scacchiera.\
                                    converti_ascissa_reale(mossa[2])) == 1:
                                        trovati = trovati + 1
                                        i_copia = riga
                                        j_copia = j
                                    else:
                                        flag = 0

                                else:
                                    flag = 0
                        
                            j = j + 1

                    if trovati == 1:
                        
                        trovati=self.prova_mossa(i_copia, j_copia, \
                        self.scacchiera.converti_ordinata_reale(int(mossa[3])), \
                        self.scacchiera.converti_ascissa_reale(mossa[2]))
                        
                            

                        #self.scacchiera.get_pezzo(i_copia,j_copia).set_Prima_Mossa()
                        #self.scacchiera.sposta_pezzo(i_copia, j_copia, \
                        #self.scacchiera.converti_ordinata_reale(int(mossa[3])), \
                        #self.scacchiera.converti_ascissa_reale(mossa[2]))
                else:
                    trovati = 0
                    
        return trovati
    
    def torre_ha_pista_libera(self, i_partenza_reale, j_partenza_reale,\
                         i_arrivo_reale, j_arrivo_reale):
        flag = 1
        i_copia = i_partenza_reale
        j_copia = j_partenza_reale

        #si muove in riga
        if i_partenza_reale == i_arrivo_reale and j_partenza_reale != j_arrivo_reale:
            if j_partenza_reale > j_arrivo_reale: #verso sinistra
                while j_copia != j_arrivo_reale + 1 and flag == 1:
                    j_copia = j_copia -1
                    if self.scacchiera.get_pezzo(i_copia, j_copia).get_nome()!="Vuoto":
                        flag = 0
            else: #verso destra
                while j_copia != j_arrivo_reale - 1 and flag == 1:
                    j_copia = j_copia + 1
                    if self.scacchiera.get_pezzo(i_copia, j_copia).get_nome()!="Vuoto":
                        flag = 0
        else:
            #si muove in colonna
            if i_partenza_reale != i_arrivo_reale and j_partenza_reale ==j_arrivo_reale:
                if i_partenza_reale>i_arrivo_reale:#verso alto
                     while i_copia != i_arrivo_reale + 1 and flag == 1:
                        i_copia = i_copia - 1
                        if self.scacchiera.get_pezzo(i_copia, j_copia).\
                        get_nome()!="Vuoto":
                            flag = 0
                else:#verso il basso
                    while i_copia != i_arrivo_reale - 1 and flag == 1:
                        i_copia = i_copia + 1
                        if self.scacchiera.get_pezzo(i_copia, j_copia).\
                        get_nome()!="Vuoto":
                            flag = 0

        return flag
        

    
    def mossa_legale(self, colore):
        i = flag = 0

        #localiziamo il re del pezzo che viene mosso
        while i < 8 and flag == 0:
            j = 0
            while j < 8 and flag == 0:
                if self.scacchiera.get_pezzo(i,j).get_nome() == "Re" \
                and self.scacchiera.get_pezzo(i,j).get_colore() == colore:
                    i_re=i
                    j_re=j
                j = j + 1
            i = i + 1

        #vediamo se un qualunque atro pezzo della 
        # scacchiera lo può catturare nella prossima mossa 
        i= 0
        while i < 8 and flag == 0:
            j = 0
            while j < 8 and flag == 0:
                if self.scacchiera.get_pezzo(i,j).get_nome() != "Vuoto"\
                    and self.scacchiera.get_pezzo(i,j).get_colore() != colore:
                    match self.scacchiera.get_pezzo(i,j).get_nome():
                        case 'Pedone':
                            if self.scacchiera.get_pezzo(i,j).cattura_lecita( \
                            i, j, i_re, j_re )==1:
                                i = 8
                                j = 8
                                flag = 3
                        case 'Alfiere': # Per chiamare la funzione che muove l'Alfiere
                            if (self.scacchiera.get_pezzo(i,j).cattura_lecita( \
                            i, j, i_re, j_re )==1 and self.\
                            alfiere_ha_pista_libera(i, j,i_re, j_re)):
                                
                                i=8
                                j=8
                                flag = 3
                        case 'Cavallo': # Per chiamare la funzione che muove il Cavallo
                            if (self.scacchiera.get_pezzo(i,j).cattura_lecita( \
                            i, j,i_re, j_re)==1):
                                
                                i=8
                                j=8
                                flag = 3
                        case 'Torre': # Per chiamare la funzione che muove la Torre
                            if (self.scacchiera.get_pezzo(i,j).cattura_lecita( \
                            i, j, i_re, j_re )==1 and self.\
                            torre_ha_pista_libera(i, j,i_re, j_re)):
                                
                                i=8
                                j=8
                                flag = 3
                        case 'Re': # Per chiamare la funzione che muove il Re
                            if (self.scacchiera.get_pezzo(i,j).cattura_lecita \
                            ( i, j,i_re, j_re)==1):
                                
                                i=8
                                j=8
                                flag = 3
                        case 'Donna': # Per chiamare la funzione che muove la Donna
                            if (self.scacchiera.get_pezzo(i,j).cattura_lecita \
                            ( i, j,i_re, j_re)==1) and \
                                self.donna_ha_pista_libera(i, j,i_re, j_re):
                                
                                i=8
                                j=8
                                flag = 3
                
                j = j + 1
            i = i + 1
        return flag
    

    def prova_mossa(self,i,j,riga_arrivo_reale,colonna_arrivo_reale):
        pezzo_da_sostituire=self.scacchiera.get_pezzo\
        (riga_arrivo_reale, colonna_arrivo_reale)
        self.scacchiera.sposta_pezzo(i,j,\
        riga_arrivo_reale, colonna_arrivo_reale)
        flag = 0


        temp_possibile_en_passant = self.possibile_en_passant 
        temp_colore_en_passant = self.colore_en_passant 
        temp_colonna_en_passant = self.colonna_en_passant
        temp_riga_en_passant = self.riga_en_passant 
        

        if (self.mossa_legale(self.scacchiera.\
        get_pezzo(riga_arrivo_reale,\
        colonna_arrivo_reale).get_colore())==3):
        
            pezzo_spostato=self.scacchiera.\
            get_pezzo(riga_arrivo_reale, \
            colonna_arrivo_reale)
            self.scacchiera.set(riga_arrivo_reale,\
            colonna_arrivo_reale,pezzo_da_sostituire)
            self.scacchiera.set(i,j,pezzo_spostato)
            flag=3
        else:
            flag=1


        self.possibile_en_passant = temp_possibile_en_passant 
        self.colore_en_passant = temp_colore_en_passant 
        self.colonna_en_passant = temp_colonna_en_passant
        self.riga_en_passant = temp_riga_en_passant

        return flag
    
    
    
    def Usa_Alfiere(self, mossa, colore):
        flag = 0
        
        if len(mossa)==3:#se si sposta senza specificare la colonna o la riga
            # se mossa è valida
            if mossa[1] >= 'a' and mossa[1] <= 'h' \
                and mossa[2] >= '1' and mossa[2] <= '8':
                #verifichiamo che sia è una semplice mossa (senza cattura)
                if self.scacchiera.get_pezzo(self.scacchiera.converti_ordinata_reale(\
                    int(mossa[2])),self.scacchiera.converti_ascissa_reale(mossa[1]))\
                        .get_nome()== "Vuoto":
                    flag = self.trova_e_sposta_alfiere(mossa, colore, 0)
                else:
                    flag = 0
            else:
                flag = 0
        else:
            #se si sposta specificando la colonna
            if len(mossa) == 4 and mossa[1]>='a' and mossa[1]<='h' \
                and mossa[2] >= 'a' and mossa[2] <= 'h' \
                and mossa[3] >= '1' and mossa[3] <= '8':
                if self.scacchiera.get_pezzo(self.scacchiera.converti_ordinata_reale(\
                int(mossa[3])),self.scacchiera.converti_ascissa_reale(mossa[2]))\
                .get_nome()== "Vuoto":
                    flag = self.trova_e_sposta_torre(mossa, colore, 1)
            else:# se si specifica la riga
                if len(mossa) == 4 and mossa[1]>='1' and mossa[1]<='8'\
                and mossa[2] >= 'a' and mossa[2] <= 'h' \
                and mossa[3] >= '1' and mossa[3] <= '8':
                    if self.scacchiera.get_pezzo(self.scacchiera\
                    .converti_ordinata_reale(int(mossa[3])),\
                    self.scacchiera.converti_ascissa_reale(mossa[2]))\
                    .get_nome()== "Vuoto":
                        flag = self.trova_e_sposta_alfiere(mossa, colore, 2)
                else:
                    #se vuole mangiare
                    if len(mossa) == 4 and mossa[1]=='x' and \
                    mossa[2] >= 'a' and mossa[2] <= 'h' and \
                    mossa[3] >= '1' and mossa[3] <= '8':
                        if self.scacchiera.get_pezzo(\
                        self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                        self.scacchiera.converti_ascissa_reale(mossa[2]))\
                        .get_nome() != "Vuoto" and self.scacchiera.get_pezzo(\
                        self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                        self.scacchiera.converti_ascissa_reale(mossa[2])).\
                        get_colore() != colore :
                            nuova_mossa = str(mossa[0])+str(mossa[2])+str(mossa[3])
                            flag = self.trova_e_sposta_alfiere(nuova_mossa, colore, 0)
                    else:
                        #se vuole mangiare specificando la colonna o la riga
                        if len(mossa) == 5 and mossa[2]=='x' and\
                        ((mossa[1]>='a' and mossa[1]<='h') or \
                        (mossa[1]>='1' and mossa[1]<='8') ) and \
                        mossa[3] >= 'a' and mossa[3] <= 'h' and \
                        mossa[4] >= '1' and mossa[4] <= '8':
                            nuova_mossa = str(mossa[0]) + str(mossa[1]) + \
                            str(mossa[3]) + str(mossa[4])
                            if (mossa[1]>='a' and mossa[1]<='h'):
    
                                flag = self.trova_e_sposta_alfiere(nuova_mossa,\
                                         colore, 1)
                            else: 
                               
                                flag = self.trova_e_sposta_alfiere(nuova_mossa, \
                                        colore, 2)

        return flag
    def trova_e_sposta_alfiere(self, mossa, colore, riga_o_colonna) :
         # riga_o_colonna è 0 se si sta cercando una generica torre
        #                  1 se si sta cercando la torre specificando la colonna
        #                  2 se si sta cercando la torre specificando la riga
        
        flag = 0
        trovati = 0
        i_copia = 0
        j_copia = 0

        if riga_o_colonna == 0:#se non specifica né colonna né riga
            i = 0
            while i<8 and trovati < 2 and flag <=2:
                j = 0
                while j<8 and trovati < 2:
                    if self.scacchiera.get_pezzo(i,j).get_nome()=="Alfiere" and\
                    self.scacchiera.get_pezzo(i,j).get_colore()==colore:

                        #se la torre è stata trovata, verifichiamo se 
                        #fa una mossa valida per lei
                        if self.scacchiera.get_pezzo(i,j).mossa_lecita(i,j,\
                        self.scacchiera.converti_ordinata_reale(int(mossa[2])),\
                        self.scacchiera.converti_ascissa_reale(mossa[1])) == 1:

                            #se la mossa è valida, verifichiamo che non ci siano pezzi 
                            #sul tragitto e indichiamo che abbiamo trovato una 
                            #delle possibili torri
                            if self.alfiere_ha_pista_libera(i, j, \
                            self.scacchiera.converti_ordinata_reale(int(mossa[2])),\
                            self.scacchiera.converti_ascissa_reale(mossa[1])) == 1:
                                trovati = trovati + 1
                                i_copia = i
                                j_copia = j
                            else:
                                flag = 0

                        else:
                            flag = 0
                            
                    j = j + 1
                i = i + 1

            if trovati == 1:
                trovati=self.prova_mossa(i_copia, j_copia, \
                self.scacchiera.converti_ordinata_reale(int(mossa[2])),\
                self.scacchiera.converti_ascissa_reale(mossa[1]))
            
                    
                #self.scacchiera.sposta_pezzo(i_copia, j_copia, \
                #self.scacchiera.converti_ordinata_reale(int(mossa[2])),\
                #self.scacchiera.converti_ascissa_reale(mossa[1]))
                

        else:
            
            if riga_o_colonna == 1:# se si sta cercando su una colonna
                i = 0
                colonna = self.scacchiera.converti_ascissa_reale(str(mossa[1]))
                
                if colonna>=0 and colonna<=7:
                    
                    while i < 8:
                        if self.scacchiera.get_pezzo(i, colonna).get_nome()=="Alfiere" \
                        and self.scacchiera.get_pezzo(i,colonna).get_colore()==colore:

                            #se la torre è stata trovata, verifichiamo se 
                            #fa una mossa valida per lei
                            if self.scacchiera.get_pezzo(i,colonna).mossa_lecita(i,\
                            colonna,self.scacchiera.converti_ordinata_reale(\
                            int(mossa[3])),self.scacchiera.converti_ascissa_reale(\
                            mossa[2])) == 1:

                                #se la mossa è valida, verifichiamo che non ci siano 
                                #pezzi sul tragitto e indichiamo che abbiamo 
                                #trovato una delle possibili torri
                                if self.alfiere_ha_pista_libera(i, colonna, \
                                self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                                self.scacchiera.converti_ascissa_reale(mossa[2])) == 1:
                                    trovati = trovati + 1
                                    i_copia = i
                                    j_copia = colonna
                                else:
                                    flag = 0

                            else:
                                flag = 0
                        
                        i = i + 1

                    if trovati == 1:
                       
                        trovati=self.prova_mossa(i_copia, j_copia, \
                        self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                        self.scacchiera.converti_ascissa_reale(mossa[2]))
                        


                       # self.scacchiera.sposta_pezzo(i_copia, j_copia, \
                       # self.scacchiera.converti_ordinata_reale(int(mossa[3])), \
                       # self.scacchiera.converti_ascissa_reale(mossa[2]))
                else:
                    trovati = 0
            else:
                if riga_o_colonna == 2:
                    
                    j = 0
                    riga = self.scacchiera.converti_ordinata_reale(int(mossa[1]))
                    if riga>=0 and riga<=7:
                        while j < 8:
                            if self.scacchiera.get_pezzo(riga, j).get_nome()=="Alfiere"\
                            and self.scacchiera.get_pezzo(riga, j).get_colore()==colore:

                                #se la torre è stata trovata, verifichiamo se 
                                #fa una mossa valida per lei
                                if self.scacchiera.get_pezzo(riga, j).\
                                mossa_lecita(riga, j,self.scacchiera.\
                                converti_ordinata_reale(int(mossa[3])), \
                                self.scacchiera.converti_ascissa_reale(mossa[2])) == 1:

                                    #se la mossa è valida, verifichiamo che non ci 
                                    #siano pezzi sul tragitto e indichiamo che abbiamo 
                                    #trovato una delle possibili torri
                                    if self.alfiere_ha_pista_libera(riga, j, \
                                    self.scacchiera.converti_ordinata_reale(\
                                    int(mossa[3])),self.scacchiera.\
                                    converti_ascissa_reale(mossa[2])) == 1:
                                        trovati = trovati + 1
                                        i_copia = riga
                                        j_copia = j
                                    else:
                                        flag = 0

                                else:
                                    flag = 0
                        
                            j = j + 1

                    if trovati == 1:
                        
                        trovati=self.prova_mossa(i_copia, j_copia, \
                        self.scacchiera.converti_ordinata_reale(int(mossa[3])), \
                        self.scacchiera.converti_ascissa_reale(mossa[2]))
                            
                        #self.scacchiera.sposta_pezzo(i_copia, j_copia, \
                        #self.scacchiera.converti_ordinata_reale(int(mossa[3])), \
                        #self.scacchiera.converti_ascissa_reale(mossa[2]))
                else:
                    trovati = 0
                    
        return trovati
   
   
    def alfiere_ha_pista_libera(self, i_partenza_reale, j_partenza_reale,\
             i_arrivo_reale, j_arrivo_reale):
        flag = 1
        i_copia = i_partenza_reale
        
        j_copia = j_partenza_reale
        if i_arrivo_reale > i_partenza_reale:# va verso il basso
            if j_arrivo_reale > j_partenza_reale: #va in basso a destra 
                while flag == 1 and i_copia != i_arrivo_reale - 1:
                    i_copia = i_copia + 1
                    j_copia = j_copia + 1
                    if self.scacchiera.get_pezzo(i_copia, j_copia).\
                        get_nome()!="Vuoto":
                            flag = 0
            else: #va in basso a sinistra
                 while flag == 1 and i_copia != i_arrivo_reale - 1:
                        i_copia = i_copia + 1
                        j_copia = j_copia - 1
                        if self.scacchiera.get_pezzo(i_copia, j_copia).\
                        get_nome()!="Vuoto":
                            flag = 0
        else:#va verso l'alto
            if j_arrivo_reale > j_partenza_reale: #va in alto a destra 
                while flag == 1 and i_copia != i_arrivo_reale + 1:
                    i_copia = i_copia - 1
                    j_copia = j_copia + 1
                    if self.scacchiera.get_pezzo(i_copia, j_copia).\
                        get_nome()!="Vuoto":
                        flag = 0
            else: #va in alto a sinistra
                while flag == 1 and i_copia != i_arrivo_reale + 1:
                    i_copia = i_copia - 1
                    j_copia = j_copia - 1
                    if self.scacchiera.get_pezzo(i_copia, j_copia).\
                        get_nome()!="Vuoto":
                        flag = 0
        return flag


    def arrocco(self,mossa,colore ):
        flag=0

        if mossa[0]=="0" and  mossa[1]=="-" and mossa[2]=="0" and len(mossa)==3:
            flag=self.arrocco_corto(colore)
        elif mossa[0]=="0" and  mossa[1]=="-" and mossa[2]=="0" and  mossa[3]=="-"\
        and mossa[4]=="0" and len(mossa)==5:
            flag=self.arrocco_lungo(colore)

        return flag


    def arrocco_lungo(self,colore):
        flag = 0
        j=1
        

        if colore=="Bianco":
            while j < 4 and flag == 0:
                
                if self.scacchiera.get_pezzo(7,j).get_nome()!="Vuoto":
                    flag=0
                    return flag
                j = j + 1

            if (self.scacchiera.get_pezzo(7,4).get_nome()=="Re" and \
            self.scacchiera.get_pezzo(7,4).get_mosso()==0)\
            and (self.scacchiera.get_pezzo(7,0).get_nome()=="Torre" and \
            self.scacchiera.get_pezzo(7,0).get_Prima_Mossa()==0):
                    #vedi se le caselle sono minacciate
                    if (self.arrocco_lecito(colore,0)==0):
                        self.scacchiera.set(7,2,self.scacchiera.get_re(colore))
                        self.scacchiera.set(7,3,self.scacchiera.get_torre(colore))
                        self.scacchiera.set_vuoto(7,4)
                        self.scacchiera.set_vuoto(7,0)
                        return 1
                    else:
                        #fa return flag=4
                        return 0   
            else:
                flag=0
            
        else:
            while j < 4 and flag == 0:
                if self.scacchiera.get_pezzo(0,j).get_nome()!="Vuoto":
                    flag=0 #c'è un pezzo non vuoto
                    return flag
                j = j + 1
            if (self.scacchiera.get_pezzo(0,4).get_nome()=="Re" and \
            self.scacchiera.get_pezzo(0,4).get_mosso()==0)\
            and (self.scacchiera.get_pezzo(0,0).get_nome()=="Torre" and \
            self.scacchiera.get_pezzo(0,0).get_Prima_Mossa()==0):
                    #vedi se le caselle sono minacciate
                    if (self.arrocco_lecito(colore,0)==0):
                        self.scacchiera.set(0,2,self.scacchiera.get_re(colore))
                        self.scacchiera.set(0,3,self.scacchiera.get_torre(colore))
                        self.scacchiera.set_vuoto(0,4)
                        self.scacchiera.set_vuoto(0,0)
                        return 1
                    else:
                        #si passa flag =4 
                        return 0
            else:
                flag=0
        
        return flag



    def arrocco_corto(self,colore):
        
        flag = 0
        j=5
        

        if colore=="Bianco":
            while j < 7 and flag == 0:
                if self.scacchiera.get_pezzo(7,j).get_nome()!="Vuoto":
                    flag=0 #c'è un pezzo non vuoto
                    return flag
                j = j + 1

            if (self.scacchiera.get_pezzo(7,4).get_nome()=="Re" and \
            self.scacchiera.get_pezzo(7,4).get_mosso()==0)\
            and (self.scacchiera.get_pezzo(7,7).get_nome()=="Torre" and \
            self.scacchiera.get_pezzo(7,7).get_Prima_Mossa()==0):
                    #vedi se le caselle sono minacciate
                    if (self.arrocco_lecito(colore,1)==0):
                        self.scacchiera.set(7,6,self.scacchiera.get_re(colore))
                        self.scacchiera.set(7,5,self.scacchiera.get_torre(colore))
                        self.scacchiera.set_vuoto(7,4)
                        self.scacchiera.set_vuoto(7,7)
                        return 1
                    else:
                        #fa return flag=4
                        return 0

            else:
                flag=0



        else:
            while j < 7 and flag == 0:
                if self.scacchiera.get_pezzo(0,j).get_nome()!="Vuoto":
                    flag=0 #c'è un pezzo non vuoto
                    return flag
                j = j + 1

            if (self.scacchiera.get_pezzo(0,4).get_nome()=="Re" and \
            self.scacchiera.get_pezzo(0,4).get_mosso()==0)\
            and (self.scacchiera.get_pezzo(0,7).get_nome()=="Torre" and \
            self.scacchiera.get_pezzo(0,7).get_Prima_Mossa()==0):
                    #vedi se le caselle sono minacciate
                    if (self.arrocco_lecito(colore,1)==0):
                        self.scacchiera.set(0,6,self.scacchiera.get_re(colore))
                        self.scacchiera.set(0,5,self.scacchiera.get_torre(colore))
                        self.scacchiera.set_vuoto(0,4)
                        self.scacchiera.set_vuoto(0,7)
                        return 1
                    else:
                        #si passa flag =4 
                        return 0
                       
                    
            else:
                flag=0
        return flag




    ##tutte le caselle tra re e torre sono non minacciate
    def arrocco_lecito(self,colore,lungo_corto): 
        flag=0
        if lungo_corto==0: #lungo
            j=1
            if colore =="Bianco":
                if self.minaccia_pezzo(7,4,colore)==4 or self.minaccia_pezzo\
                (7,0,colore)==4:
                    flag=1
                while j<4 and flag==0:
                    self.scacchiera.set(7,j,self.scacchiera.get_pedone("Bianco"))
                    if self.minaccia_pezzo(7,j,colore)==4:
                        #pezzo minacciato
                        flag=self.minaccia_pezzo(7,j,colore)#false
                    self.scacchiera.set_vuoto(7,j)
                    j=j+1
                j=1
            else:
                if self.minaccia_pezzo(0,4,colore)==4 or self.minaccia_pezzo\
                (0,0,colore)==4:
                    flag=1
                while j<4 and flag==0:
                    self.scacchiera.set(0,j,self.scacchiera.get_pedone("Nero"))
                    if self.minaccia_pezzo(0,j,colore)==4:
                        #pezzo minacciato
                        flag=self.minaccia_pezzo(0,j,colore)#false
                    self.scacchiera.set_vuoto(0,j)
                    j=j+1
                j=1


        elif lungo_corto==1: #corto
            j=5
            if colore =="Bianco":
                if self.minaccia_pezzo(7,4,colore)==4 or self.minaccia_pezzo\
                (7,7,colore)==4:
                    flag=1

                while j<7 and flag==0:
                    self.scacchiera.set(7,j,self.scacchiera.get_pedone("Bianco"))
                    if self.minaccia_pezzo(7,j,colore)==4:
                        #pezzo minacciato
                        flag=self.minaccia_pezzo(7,j,colore)#false
                    self.scacchiera.set_vuoto(7,j)
                    j=j+1
                j=1
            else:
                if self.minaccia_pezzo(0,4,colore)==4 or self.minaccia_pezzo\
                (0,7,colore)==4:
                    flag=1

                while j<7 and flag==0:
                    self.scacchiera.set(0,j,self.scacchiera.get_pedone("Bianco"))
                    if self.minaccia_pezzo(0,j,colore)==4:
                        #pezzo minacciato
                        flag=self.minaccia_pezzo(0,j,colore)#false
                    self.scacchiera.set_vuoto(0,j)
                    j=j+1
                j=1
        return flag

    


    def minaccia_pezzo(self,i,j,colore):
        #pezzo minacciato
        flag=0#non minacciato
        

        i_re=i
        j_re=j
        
        #vediamo se un qualunque atro pezzo della 
        # scacchiera lo può catturare nella prossima mossa 
        i= 0
        while i < 8 and flag == 0:
            j = 0
            while j < 8 and flag == 0:
                if self.scacchiera.get_pezzo(i,j).get_nome() != "Vuoto"\
                    and self.scacchiera.get_pezzo(i,j).get_colore() != colore:
                    match self.scacchiera.get_pezzo(i,j).get_nome():
                        case 'Alfiere': # Per chiamare la funzione che muove l'Alfiere
                            if (self.scacchiera.get_pezzo(i,j).cattura_lecita( \
                            i, j, i_re, j_re )==1 and self.\
                            alfiere_ha_pista_libera(i, j,i_re, j_re)):
                                
                                i=8
                                j=8
                                flag = 4
                        case 'Cavallo': # Per chiamare la funzione che muove il Cavallo
                            if (self.scacchiera.get_pezzo(i,j).cattura_lecita \
                            ( i, j,i_re, j_re)==1):
                                
                                i=8
                                j=8
                                flag = 4
                        case 'Torre': # Per chiamare la funzione che muove la Torre
                            if (self.scacchiera.get_pezzo(i,j).cattura_lecita( \
                            i, j, i_re, j_re )==1 and self.\
                            torre_ha_pista_libera(i, j,i_re, j_re)):
                                
                                i=8
                                j=8
                                flag = 4
                        case 'Re': # Per chiamare la funzione che muove il Re
                            if (self.scacchiera.get_pezzo(i,j).cattura_lecita \
                            ( i, j,i_re, j_re)==1):
                                
                                i=8
                                j=8
                                flag = 4
                        case 'Donna': # Per chiamare la funzione che muove la Donna
                            if (self.scacchiera.get_pezzo(i,j).cattura_lecita \
                            ( i, j,i_re, j_re)==1) and \
                                self.donna_ha_pista_libera(i, j,i_re, j_re):
                                
                                i=8
                                j=8
                                flag = 4         
                j = j + 1
            i = i + 1
        return flag
    
    def Usa_Cavallo(self, mossa, colore):
        flag = 0
        
        if len(mossa)==3:#se si sposta senza specificare la colonna o la riga
            # se mossa è valida
            
            if mossa[0]=='C' and mossa[1] >= 'a' and mossa[1] <= 'h' \
                and mossa[2] >= '1' and mossa[2] <= '8':
                #verifichiamo che sia è una semplice mossa (senza cattura)
                if self.scacchiera.get_pezzo(self.scacchiera.converti_ordinata_reale(\
                    int(mossa[2])),self.scacchiera.converti_ascissa_reale(mossa[1]))\
                        .get_nome()== "Vuoto":
                    flag = self.trova_e_sposta_cavallo(mossa, colore, 0)
                else:
                    flag = 0
            else:
                flag = 0
        else:
            #se si sposta specificando la colonna
            if len(mossa) == 4 and mossa[1]>='a' and mossa[1]<='h' \
                and mossa[2] >= 'a' and mossa[2] <= 'h' \
                and mossa[3] >= '1' and mossa[3] <= '8':
                if self.scacchiera.get_pezzo(self.scacchiera.converti_ordinata_reale(\
                int(mossa[3])),self.scacchiera.converti_ascissa_reale(mossa[2]))\
                .get_nome()== "Vuoto":
                    flag = self.trova_e_sposta_cavallo(mossa, colore, 1)
            else:# se si specifica la riga
                if len(mossa) == 4 and mossa[1]>='1' and mossa[1]<='8'\
                and mossa[2] >= 'a' and mossa[2] <= 'h' \
                and mossa[3] >= '1' and mossa[3] <= '8':
                    if self.scacchiera.get_pezzo(self.scacchiera\
                    .converti_ordinata_reale(int(mossa[3])),\
                    self.scacchiera.converti_ascissa_reale(mossa[2]))\
                    .get_nome()== "Vuoto":
                        flag = self.trova_e_sposta_cavallo(mossa, colore, 2)
                else:
                    #se vuole mangiare
                    if len(mossa) == 4 and mossa[1]=='x' and \
                    mossa[2] >= 'a' and mossa[2] <= 'h' and \
                    mossa[3] >= '1' and mossa[3] <= '8':
                        if self.scacchiera.get_pezzo(\
                        self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                        self.scacchiera.converti_ascissa_reale(mossa[2]))\
                        .get_nome() != "Vuoto" and self.scacchiera.get_pezzo(\
                        self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                        self.scacchiera.converti_ascissa_reale(mossa[2])).\
                        get_colore() != colore :
                            #nuova_mossa = str(mossa[0])+str(mossa[2])+str(mossa[3])
                            flag = self.trova_e_sposta_cavallo(mossa, colore, 0)
                    else:
                        #se vuole mangiare specificando la colonna o la riga
                        if len(mossa) == 5 and mossa[2]=='x' and\
                        ((mossa[1]>='a' and mossa[1]<='h') or \
                        (mossa[1]>='1' and mossa[1]<='8') ) and \
                        mossa[3] >= 'a' and mossa[3] <= 'h' and \
                        mossa[4] >= '1' and mossa[4] <= '8':
                            if (mossa[1]>='a' and mossa[1]<='h'):
    
                                flag = self.trova_e_sposta_cavallo(mossa,\
                                         colore, 1)
                            else: 
                               
                                flag = self.trova_e_sposta_cavallo(mossa, \
                                        colore, 2)

        return flag
    
    def trova_e_sposta_cavallo(self, mossa, colore, riga_o_colonna) :
             # riga_o_colonna è 0 se si sta cercando un generico cavallo
        #                  1 se si sta cercando il cavallo specificando la colonna
        #                  2 se si sta cercando il cavallo specificando la riga     
        flag=1
        i=0
        j=0
        conta_pezzi=0
        possibile =1
        if riga_o_colonna==0:
            if len(mossa) == 4: #cavallo deve mangiare
             #controllo della scacchiera per eventuali pezzi
                while i<=7 and conta_pezzi<=1 and possibile ==1:
                    j=0
                    while j <=7 and conta_pezzi<=1 and possibile ==1:
                        #verifica nome del pezzo
                        if self.scacchiera.get_pezzo(i,j).get_nome()=="Cavallo" and\
                            self.scacchiera.get_pezzo(i,j).get_colore()==colore:
                            #controllo spazio di arrivo
                            if self.scacchiera.get_pezzo(self.scacchiera.\
                                            converti_ordinata_reale(int(mossa[3])),\
                        self.scacchiera.converti_ascissa_reale(mossa[2])).\
                            get_nome() != "Vuoto"\
                            and self.scacchiera.get_pezzo(self.scacchiera.\
                                        converti_ordinata_reale(int(mossa[3])),\
                        self.scacchiera.converti_ascissa_reale(mossa[2])).get_colore()\
                              != colore:
                            #aggiornare numero pezzi trovati
                                
                                #validità mossa
                                if self.scacchiera.get_pezzo(i,j).mossa_lecita(i,j,\
                            self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                            self.scacchiera.converti_ascissa_reale(mossa[2])) == 1:
                                    conta_pezzi=conta_pezzi+1
                                    i_temp=i
                                    j_temp=j
                                else:
                            #movimento non possibile per il cavallo in quelle coordinate
                                    pass
                                    
                            else:
                            #spazio vuoto o occupato da un pezzo dello stesso colore
                                possibile =0
                        else:#non è un cavallo
                            pass
                        j=j+1
                    i=i+1
                if conta_pezzi==1:
                    flag= self.prova_mossa(i_temp,j_temp, \
                self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                self.scacchiera.converti_ascissa_reale(mossa[2]))  
                elif conta_pezzi>1:
                    flag=2
                

                            
                            
            
            
            
            else :#mosse senza mangiare
                
                i=0
                i_temp = 0
                j_temp = 0
                while i<=7 and conta_pezzi<=1 and possibile ==1:
                    j=0
                    while j <=7 and conta_pezzi<=1 and possibile ==1:
                        #verifica nome del pezzo
                        if self.scacchiera.get_pezzo(i,j).get_nome()=="Cavallo" and\
                            self.scacchiera.get_pezzo(i,j).get_colore()==colore:
                            #controllo se lo  spazio di arrivo è vuoto
                            if self.scacchiera.get_pezzo(self.scacchiera.\
                                            converti_ordinata_reale(int(mossa[2])),\
                                            self.scacchiera\
                            .converti_ascissa_reale(mossa[1])).get_nome() == "Vuoto":
                                #validità mossa
                                if self.scacchiera.get_pezzo(i,j).mossa_lecita(i,j,\
                            self.scacchiera.converti_ordinata_reale(int(mossa[2])),\
                            self.scacchiera.converti_ascissa_reale(mossa[1])) == 1:
                                    i_temp = i
                                    j_temp = j
                                    conta_pezzi = conta_pezzi + 1
                                else:
                            #movimento non possibile per il cavallo in quelle coordinate
                                    pass
                        else:#non è un cavallo
                            pass
                        j=j+1
                    i=i+1

                
                
                if conta_pezzi==1:
                    flag=1
                    flag=self.prova_mossa(i_temp, j_temp, self.scacchiera\
                            .converti_ordinata_reale(int(mossa[2])),\
                                    self.scacchiera.converti_ascissa_reale(mossa[1]))
                    
                elif conta_pezzi>1:
                    flag=2
                else:
                    flag=0
                            
                            
                            

                        
        
        if riga_o_colonna==1:#colonne

            if len(mossa) == 5: #cavallo deve mangiare
             #controllo della scacchiera per eventuali pezzi
                while i<=7 and conta_pezzi<=1 and possibile ==1:
                    
                    #verifica nome del pezzo
                    if self.scacchiera.get_pezzo(i,\
                        self.scacchiera.converti_ascissa_reale(mossa[1])).\
                            get_nome()=="Cavallo" and\
                        self.scacchiera.get_pezzo(i,\
                        self.scacchiera.converti_ascissa_reale(mossa[1]))\
                            .get_colore()==colore:
                        
                        #controllo spazio di arrivo
                        if self.scacchiera.get_pezzo\
                            (self.scacchiera.converti_ordinata_reale(int(mossa[4])),\
                        self.scacchiera.converti_ascissa_reale(mossa[3]))\
                            .get_nome() != "Vuoto"\
                            and self.scacchiera.get_pezzo\
                            (self.scacchiera.converti_ordinata_reale(int(mossa[4])),\
                        self.scacchiera.converti_ascissa_reale(mossa[3])).get_colore() \
                            != colore:
                            #aggiornare numero pezzi trovati
                                
                                #validità mossa
                            if self.scacchiera.get_pezzo(i,self.scacchiera.\
                                converti_ascissa_reale(mossa[1])).\
                                cattura_lecita(i,self.scacchiera.\
                                               converti_ascissa_reale(mossa[1]),\
                            self.scacchiera.converti_ordinata_reale(int(mossa[4])),\
                            self.scacchiera.converti_ascissa_reale(mossa[3])) == 1:

                                conta_pezzi=conta_pezzi+1
                                i_temp=i
                            else:
                            #movimento non possibile per il cavallo in quelle coordinate
                                pass
                                    
                        else:
                            #spazio vuoto o occupato da un pezzo dello stesso colore
                                possibile =0
                    else:#non è un cavallo
                            pass
                    i=i+1
                if conta_pezzi==1:
                    flag= self.prova_mossa(i_temp,self.scacchiera.\
                                           converti_ascissa_reale\
                                           (mossa[1]) , \
                self.scacchiera.converti_ordinata_reale(int(mossa[4])),\
                self.scacchiera.converti_ascissa_reale(mossa[3]))  
                elif conta_pezzi>1:
                    flag=2
                

                            
                            
            
            
            
            else :#mosse senza mangiare
                
                i=0
                i_temp = 0
                j_temp = 0
                conta_pezzi=0
                possibile =1
                while i<=7 and conta_pezzi<=1 and possibile ==1:
                    #verifica nome del pezzo
                    if self.scacchiera.get_pezzo(i,self.scacchiera.\
                        converti_ascissa_reale(mossa[1])).get_nome()=="Cavallo" and\
                        self.scacchiera.get_pezzo(i,self.scacchiera.\
                        converti_ascissa_reale(mossa[1])).get_colore()==colore:
                        #controllo se lo  spazio di arrivo è vuoto
                        if self.scacchiera.get_pezzo(self.scacchiera.\
                                converti_ordinata_reale(int(mossa[3])),\
                                    self.scacchiera.converti_ascissa_reale(mossa[2])).\
                                    get_nome() == "Vuoto":
                            #validità mossa
                            if self.scacchiera.get_pezzo(i,self.scacchiera.\
                                converti_ascissa_reale(mossa[1]))\
                            .mossa_lecita(i,self.scacchiera.\
                                        converti_ascissa_reale(mossa[1]),\
                            self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                            self.scacchiera.converti_ascissa_reale(mossa[2])) == 1:
                                i_temp = i
                                conta_pezzi = conta_pezzi + 1
                            else:
                            #movimento non possibile per il cavallo in quelle coordinate
                                pass
                    else:#non è un cavallo
                            pass
                    i=i+1

                
                
                if conta_pezzi==1:
                    flag=1
                    flag=self.prova_mossa(i_temp, self.scacchiera.\
                                          converti_ascissa_reale(mossa[1]), \
                        self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                            self.scacchiera.converti_ascissa_reale(mossa[2]))
                    
                elif conta_pezzi>1:
                    flag=2
                else:
                    flag=0
        if riga_o_colonna==2:
            
            if len(mossa) == 5: #cavallo deve mangiare
             #controllo della scacchiera per eventuali pezzi
                while i<=7 and conta_pezzi<=1 and possibile ==1:
                    #verifica nome del pezzo
                    
                    if self.scacchiera.get_pezzo(self.scacchiera.\
                                converti_ordinata_reale(int(mossa[1])),i).\
                                    get_nome()=="Cavallo" and\
                        self.scacchiera.get_pezzo(self.scacchiera.\
                                         converti_ordinata_reale(int(mossa[1])),\
                                          i).get_colore()==colore:
                        
                        #controllo dello spazio di arrivo
                        if self.scacchiera.get_pezzo(self.scacchiera.\
                                        converti_ordinata_reale(int(mossa[4])),\
                        self.scacchiera.converti_ascissa_reale(mossa[3])).\
                            get_nome() != "Vuoto"\
                            and self.scacchiera.get_pezzo(self.scacchiera.\
                                                converti_ordinata_reale(int(mossa[4])),\
                        self.scacchiera.converti_ascissa_reale(mossa[3])).\
                            get_colore() != colore:
                            
                            #aggiornare numero pezzi trovati
                                
                                #validità mossa
                            if self.scacchiera.get_pezzo(self.scacchiera.\
                                                         
                                        converti_ordinata_reale(int(mossa[1])),\
                                i).cattura_lecita(self.scacchiera.\
                                            converti_ordinata_reale(int(mossa[1])),i,\
                            self.scacchiera.converti_ordinata_reale(int(mossa[4])),\
                            self.scacchiera.converti_ascissa_reale(mossa[3])) == 1:
                                
                                conta_pezzi=conta_pezzi+1
                                i_temp=i
                            else:
                            #movimento non possibile per il cavallo in quelle coordinate
                                pass
                                    
                        else:
                        #spazio vuoto o occupato da un pezzo dello stesso colore
                                possibile =0
                    else:#non è un cavallo
                            pass
                    i=i+1
                if conta_pezzi==1:
                    
                    flag= self.prova_mossa(self.scacchiera.\
                            converti_ordinata_reale(int(mossa[1])),i_temp , \
                self.scacchiera.converti_ordinata_reale(int(mossa[4])),\
                self.scacchiera.converti_ascissa_reale(mossa[3]))  
                elif conta_pezzi>1:
                    flag=2
                

                            
                            
            
            
            
            else :#mosse senza mangiare
                
                
                i=0
                i_temp = 0
                j_temp = 0
                conta_pezzi=0
                possibile =1
                while i<=7 and conta_pezzi<=1 and possibile ==1:
                    #verifica nome del pezzo
                    if self.scacchiera.get_pezzo(self.scacchiera.\
                                            converti_ordinata_reale(int(mossa[1]))\
                                                 ,i).get_nome()=="Cavallo" and\
                        self.scacchiera.get_pezzo(self.scacchiera.\
                                            converti_ordinata_reale(int(mossa[1]))\
                                                  ,i).get_colore()==colore:
                        
                        #controllo se lo  spazio di arrivo è vuoto
                        if self.scacchiera.get_pezzo(self.scacchiera.\
                                            converti_ordinata_reale(int(mossa[3])),\
                            self.scacchiera.converti_ascissa_reale(mossa[2])).\
                                get_nome() == "Vuoto":
                            
                            #validità mossa
                            if self.scacchiera.get_pezzo(self.scacchiera.\
                                converti_ordinata_reale(int(mossa[1])),i)\
                            .mossa_lecita(self.scacchiera.\
                            converti_ordinata_reale(int(mossa[1])),i,\
                        self.scacchiera.converti_ordinata_reale(int(mossa[3])),\
                        self.scacchiera.converti_ascissa_reale(mossa[2])) == 1:
                               
                                i_temp = i
                                conta_pezzi = conta_pezzi + 1
                            else:
                         #movimento non possibile per il cavallo in quelle coordinate
                                pass
                    else:#non è un cavallo
                            pass
                    i=i+1

                
                
                if conta_pezzi==1:
                    flag=1
                    flag=self.prova_mossa(self.scacchiera.\
                                          converti_ordinata_reale(int(mossa[1])), \
                                          i_temp, self.scacchiera.\
                                            converti_ordinata_reale(int(mossa[3])),\
                                            self.scacchiera.\
                                                converti_ascissa_reale(mossa[2]))
                    
                elif conta_pezzi>1:
                    flag=2
                else:
                    flag=0
        return flag