from collections import Counter


def trovaMinimiUnisci(diz: dict):  # metodo che, dato un dizionario contenente una distribuzione su più simboli
    # accorpa i due simboli meno frequenti e restituisce la probabilità del nuovo simbolo generato
    lettmenoprob = min(diz, key=diz.get)
    prob1 = diz.pop(lettmenoprob)
    lett2menoprob = min(diz, key=diz.get)
    prob2 = diz.pop(lett2menoprob)
    diz[(lettmenoprob, lett2menoprob)] = prob1 + prob2
    return diz, prob1 + prob2


def primoPassoHuffman(dizProb: dict):  # metodo vhe ritorna una tupla contenente tutte le tuple di unioni di simboli
    # meno probabili che accorpo a ogni passo
    probtot = 0
    while probtot < 1:  # ciclo finché non arrivo a ottenere un unico simbolo che possiede probabilità pari ad 1
        dizProb, probtot = trovaMinimiUnisci(dizProb)  # unisco i due simboli con probabilità più piccola
    return list(dizProb.keys())[0]  # elimino l'informazione che la probabilità di tale simbolo sia uguale a uno
    # perché ovvia avendo unito tutti i possibili simboli


def secondoPasso(tuplaUnioni: tuple, dizFin):  # Metodo che, data la tupla ricavata al punto precedente,
    # restituisce il dizionario che associa a ogni lettera la relativa codifica ottenuta con l'algoritmo di Huffman
    if not dizFin:  # se ho passato in input un dizionario vuoto (ovvero quando chiamo il metodo esternamente),
        # ci inserisco il simbolo unione passato in input associandoci la stringa vuota
        dizFin[tuplaUnioni] = ""
    dizFin[tuplaUnioni[0]] = dizFin[tuplaUnioni] + "0"  # associo poi il simbolo a sinistra e a destra della tupla
    # rappresentante il simbolo unito la stringa associata al simbolo unione concatenata rispettivamente con 0 ed 1
    dizFin[tuplaUnioni[1]] = dizFin[tuplaUnioni] + "1"
    if type(tuplaUnioni[0]) == tuple:  # se il simbolo a sinistra o destra del simbolo unione è a sua volta
        # l'unione di due simboli, chiamo ricorsivamente il metodo con il dizionario già ottenuto su tale tupla
        # concatenando poi il dizionario ottenuto con quello passato in input
        dizFin |= secondoPasso(tuplaUnioni[0], dizFin)
    if type(tuplaUnioni[1]) == tuple:
        dizFin |= secondoPasso(tuplaUnioni[1], dizFin)
    dizFin.pop(tuplaUnioni)  # elimino dal dizionario il simbolo unione che ho appena scomposto
    return dizFin  # ritorno il dizionario così ottenuto


def comprimiHuffman(testo: str):  # metodo che codifica una stringa di lettere con il codice ricavato dall'algoritmo
    # di Huffman
    dizfreq = dict(Counter(testo))  # conto la frequenza delle lettere nel testo
    lungh = len(testo)  # misuro il numero di lettere nella stringa
    for i in dizfreq:
        dizfreq[i] = dizfreq[i] / lungh  # ottengo la proporzione di ogni lettera nella stringa
    # applico i due passi dell'algoritmo di Huffman per ottenere il codice istantaneo desiderato
    raggruppamento = primoPassoHuffman(dizfreq)
    dizCompressione = secondoPasso(raggruppamento, {})
    testofin = testo
    for i in dizCompressione:  # rimpiazzo ogni lettera con la relativa codifica ottenuta
        testofin = testofin.replace(i, dizCompressione[i])
    return testofin, dizCompressione  # restituisco la stringa codificata e il dizionario
    # contenente il codice istntaneo generato


def decomprimiPrefixFree(strcompr: str, dizionario_codice: dict):
    # Metodo per decomprimere una qualsiasi stringa compressa con un codice prefix-free
    strbuff = ""  # stringa temporanea in cui concateno tutti i bit che incontro finché non trovo una codeword
    # corrispondente
    strfin = ""  # stringa che conterrà il testo decompresso
    dizinv = {v: k for k, v in dizionario_codice.items()}  # inverto le chiavi e i valori del dizionario in input per
    # poter cercare la lettera associata a una codeword
    for carattere in strcompr:  # ciclo sulla stringa in ingresso
        strbuff += carattere   # concateno un carattere alla volta
        if strbuff in dizinv:  # finché non trovo la lettera corrispondente nel dizionario della codifica
            lett = dizinv[strbuff]
            strfin += lett  # concateno la lettera recuperata alla stringa decompressa
            strbuff = ""
    return strfin
