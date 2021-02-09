#Classe per le eccezioni
class ExamException(Exception):
    pass

#Classe per lettura da file
class CSVTimeSeriesFile:

    #Costruttore
    def __init__(self, name):
        if((isinstance(name, str))!=True or name==""): #controllo che il parametro passato sia una stringa
            raise ExamException("NOME FILE ERRATO")
        else:
            self.name=name
            
    #Metodo per lettura e restituzione dati dal file
    def get_data(self):

        time_series = [] #creo una lista per i valori hce dovrò restituire

        try:
            my_file = open(self.name, 'r') #apro il file
        except:
            raise ExamException("---Impossibile aprire il file---")

        for line in my_file: #ciclo le righe
            elementi = line.split(',') #separo i valori
            if(elementi[0]!='epoch'): #controllo che non sia la riga dell'intestazione
                try:
                    assert(len(elementi)==2)
                    timestamp = int(float(elementi[0]))
                    temperatura = float(elementi[1])
                    time_series.append([timestamp, temperatura])
                except:
                    print("impossibile aggiungere la linea {} ".format(line))

        my_file.close() #Chiudo la lettura del file

        #controllo non sia vuota la lista da restituire ovvero il file
        try:
            assert(len(time_series)!=0)
        except:
            raise ExamException("---File vuoto o nessun dato preso---")

        #ciclo i time_series da restituire per controllare la correttezza
        for i in range(len(time_series)-1):
            if (time_series[i][0]>=time_series[i+1][0]):
                raise ExamException("-Cronologia delle misurazioni non ordinata o presenza di duplicati-")

        #se corretti, ritorno la lista annidata con i time_series
        return time_series

#Funzione per calcolare le statistiche giornaliere
def daily_stats(lista):
    controllo = isinstance(lista, list)
    if(lista==None or controllo!=True or len(lista)==0): #Controllo sia una lista
        raise ExamException("Errore: lista vuota o errata")

    for dati in lista:
        if(isinstance(dati, list)!=True): #Controllo sia una lista annidata
            raise ExamException("Errore: Non  tutti gli elementi della lista sono liste annidate")

    statistiche = [] #creo la lista delle statistiche giornaliere
    iniziogiorni = [] #creo la lista contenente l'inizio dei vari giorni

    for misurazione in lista:
        ini=misurazione[0]-misurazione[0]%86400 #prendo l'inizio del giorno delle varie misurazioni
        if(ini not in iniziogiorni): #controllo non sia già stato memorizzato
            iniziogiorni.append(ini) #aggiungo la mezzanotte dei giorni

    i=0
    j=0 #definisco due indici

    while(i<len(iniziogiorni)):
        giorno=[] #creo una lista vuota per i vari giorni ad ogni ciclo
        while(j<len(lista) and iniziogiorni[i]==(lista[j][0]-(lista[j][0]%86400))):
            giorno.append(lista[j][1]) #aggiungo solo la temperatura
            j=j+1
        statistiche.append([min(giorno), max(giorno), sum(giorno)/len(giorno)]) #aggiungo i time_series studiati
        i=i+1

    #ritorno la lista di liste con i risultati
    return statistiche