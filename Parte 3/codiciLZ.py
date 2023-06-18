import math


def associaletterabin(lettera: str):  # associa a ciascuna lettera dell'alfabeto inglese la sua rappresentazione binaria
    val = ord(lettera) - 97
    binrappr = "{0:b}".format(val)  # metodo per rappresentare in binario un intero
    while len(binrappr) < 5:
        binrappr = "0" + binrappr
    return binrappr


def associanumbin(num: int, numbit):  # associo a un intero la rappresentazione binaria con il numero di bit desiderato
    binrappr = "{0:b}".format(num)  # metodo per rappresentare in binario un intero
    while len(binrappr) < numbit:
        binrappr = "0" + binrappr
    return binrappr


def comprimiStringaLZ(stringa: str):  # metodo per ottenere la compressione di una stringa in lingua inglese
    bufstr = stringa[1:len(stringa)]  # variabile contenente la parte di stringa rimasta da analizzare
    dizpar = {'': (0, ""), stringa[0]: (1, associaletterabin(stringa[0]) + "0")}  # creo il dizionario e ci inserisco
    # la entry relativa alla stringa vuota e quella relativa al primo carattere della stringa in ingresso
    blocco = ""  # variabile che conterrà una sottostringa del testo in ingresso, che inserirò nel dizionario se non
    # è già presente
    lettan = ""  # ultima lettera analizzata nel ciclo
    stringaFin = associaletterabin(stringa[0])  # Evito di aggiungere il puntatore a 0 in prima posizione
    # visto che è comune per tutte le stringhe compresse
    cont = 1  # tengo conto del numero di blocchi inseriti nel dizionario
    while bufstr != "":  # ciclo finché non ho terminato la stringa
        lettan = bufstr[0]  # leggo la prima lettera della stringa non ancora letta
        blocco += lettan  # la aggiungo al blocco in analisi
        if blocco not in dizpar:  # se ho recuperato un blocco che non avevo ancora trovato lo inserisco nel
            # dizionario e aggiorno la stringa compressa
            cont += 1  # tengo conto del numero di blocchi nel dizionario
            # genero la stringa binaria che rappresenterà il blocco in analisi,
            # concatenando il puntatore al blocco precedente da cui ha avuto origine quello attuale
            # insieme all'ultima lettera del nuovo blocco
            numbin = associanumbin(dizpar[blocco[:-1]][0], math.ceil(math.log2(cont))) + associaletterabin(lettan)
            dizpar[blocco] = (cont, numbin)  # aggiungo nel dizionario una entry relativa al blocco,
            # contenente il riferimento e la rappresentazione compressa appena ottenuta per il blocco stesso
            stringaFin += numbin  # concateno la rappresentazione del blocco con la parte di stringa già compressa
            blocco = ""  # resetto il blocco come la stringa vuota
        bufstr = bufstr[1:len(bufstr)]  # in ogni caso aggiorno la parte rimanente della stringa da analizzare
    if blocco != "":  # considero infine la parte di stringa finale che potrebbe non essere stata compressa
        # in quanto identica a un blocco osservato in precedenza
        cont += 1
        stringaFin += associanumbin(dizpar[blocco[:-1]][0], math.ceil(math.log2(cont))) + associaletterabin(lettan)
    return stringaFin


def decomprimiStringaLZ(stringaLZ: str):  # metodo per decomprimere una stringa compressa con l'algoritmo Lempel-Ziv
    cont = 1
    dizTrad = {}
    # decomprimo la prima lettera della stringa
    letterabin = stringaLZ[:5]
    stringadecompr = chr(int(letterabin, 2) + 97)
    stringaLZ = stringaLZ[5:]
    # tengo traccia nel dizionario dei blocchi già incontrati
    dizTrad[1] = stringadecompr
    dizTrad[0] = ""
    while stringaLZ:
        cont += 1
        puntatore = int(stringaLZ[:math.ceil(math.log2(cont))], 2)  # recupero il puntatore al blocco precedente
        # e lo converto in intero (in formato decimale)
        stringaLZ = stringaLZ[math.ceil(math.log2(cont)):]  # elimino il puntatore appena trovato dalla stringa
        letterabin = stringaLZ[:5]  # recupero la codifica della lettera da aggiungere alla fine blocco precedente
        stringaLZ = stringaLZ[5:]  # elimino la codifica della lettera dalla stringa compressa
        blocco = dizTrad[puntatore] + chr(int(letterabin, 2) + 97)  # "traduco" la rappresentazione della lettera in
        # carattere e la concateno al blocco precedente puntato dal puntatore
        stringadecompr += blocco  # concateno il blocco appena trovato alla stringa decompressa
        dizTrad[cont] = blocco  # aggiorno il dizionario con il nuovo blocco
    return stringadecompr
