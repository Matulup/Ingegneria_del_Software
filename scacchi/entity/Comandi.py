class Comandi:
    """<<Entity>>.

    Classe che modella i comandi utilizzabili nell'applicazione.
    - Verifica l'esistenza del comando passato.
    - Restituiscce un numero univoco associato allo specifico comando. 
    """

    def __init__(self):
        self.comandi = ["/gioca",
                        "/help",
                        "/scacchiera",
                        "/esci",
                        "/abbandona",
                        "/mosse",
                        "/patta"]
    
    def esiste_commando(self, comando):
    # Dice se il comando passato esiste (e quindi se è corretto)
    # input:
    # - comando: comando di cui verificare l'esistenza
    # output:
    # 1) 0 se il comando non esiste
    # 2) 1 se il comando esiste
    # #
        i = flag = 0
        while i < len(self.comandi) and flag == 0:
            if self.comandi[i] == comando:
                flag = 1
            i = i + 1
        return flag
    
    # Restituisce un identificativo univoco associato al comando passato (e quindi 
    # se è corretto)
    # input:
    # - comando: comando di cui si vuol conoscere l'identificativo
    # output: identificativo univoco del comando (cioè l'indice del comando 
    #          nel vettore 'comandi')
    # #
    def get_numero_comando(self, comando):
        i = flag = 0
        while i < len(self.comandi) and flag == 0:
            if self.comandi[i] == comando:
                flag = 1
            i = i + 1
        return i - 1