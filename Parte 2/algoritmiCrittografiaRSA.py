import random
import time


def algoritmoEstesoEuclide(a, n):  # Algoritmo esteso di Euclide per ricavare il MCD tra a ed n e gli inversi in
    # modulo corrispondente all'altro valore se MCD=1
    x = 0
    y = 1
    inva = 1  # Variabile che conterrà i valori intermedi del coefficiente di rabin associato ad a
    invn = 0  # Variabile che conterrà i valori intermedi del coefficiente di rabin associato a n
    resto = n
    MCD = a  # variabile che conterrà il MCD tra a ed n
    while resto != 0:  # ciclo finché il resto della divisione non diventa pari a 0
        quoziente = MCD // resto
        MCD, resto = resto, MCD - quoziente * resto  # evito di creare due variabili temporanee per scambiare i valori
        inva, x = x, inva - quoziente * x  # applico la formula per il coefficiente di Rabin associato ad a
        invn, y = y, invn - quoziente * y  # applico la formula per ricavare il coefficiente di Rabin associato a n
    return MCD, inva % n, invn % a  # applico il modulo ai coefficienti di rabin per ricavare gli inversi di a ed
    # n in modulo rispettivamente n e a


def esponenziazioneVeloce(base, esponente, modulo):
    d = 1
    while esponente:  # Simulo le iterazioni sulla rappresentazione binaria invertendo l'ordine di scorrimento
        # rispetto all'algoritmo classico, con l'accortezza
        # d'invertire il controllo del bit e l'elevamento al quadrato
        esponente, bit = esponente // 2, esponente % 2
        if bit:
            d = d * base % modulo
        base = base * base % modulo

    return d


def testMillerRabin(numero, test):  # Test di compstezza per un qualsiasi numero (il valore di test dev'essere
    # coprimo con il numero in analisi ma in quel caso so gia che il numero è composto)
    if numero % 2 == 0:
        return True
    m = numero - 1
    r = 0
    while m % 2 == 0:  # divido per due fin fìnchè non trovo un numero dispari
        m //= 2
        r += 1
    x = esponenziazioneVeloce(test, m, numero)  # mi ricavo il valore risultante dall'iterazione iniziale
    # dell'algoritmo
    if x == 1 or x == numero - 1:  # se tale valore è pari a +-1 in modulo pari al numero in analisi il test fallisce
        return False
    for i in range(r + 1):  # altrimenti proseguo con le iterazioni fino a che
        # o non trovo un valore pari a -1 prima dell'ultima iterazione, il che fa fallire il test, o trovo un valore
        # pari ad 1 che invece mostra che il numero in analisi è certamente composto.
        # Se invece non si verifica nessuno di questi casi, allora termino le iterazioni e restiuisco vero
        x = esponenziazioneVeloce(x, 2, numero)
        if i != r and x == numero - 1:
            return False
        if x == 1:
            return True
    return True


def generaNumPrimo(ordine, sogliatoll):  # algoritmo per generare primi casuali grazie al test di Miller-Rabin
    while True:
        candidato = random.randrange(2 ** (ordine - 1) + 1, 2 ** ordine, 2)  # scelgo, dato in input l'ordine
        # di grandezza n, un numero a caso nell'intervallo 2^(n-1) e 2^n che sarà il mio candidato
        test = random.randrange(2, candidato - 1)  # genero il primo valore per eseguire
        # il test di compositezza del candidato
        toll = 1 / 4  # Probabilità di errore del test di Miller-Rabin se ritorna falso
        primo = not testMillerRabin(candidato, test) and algoritmoEstesoEuclide(candidato, test)[0] == 1
        while toll > sogliatoll and primo:  # controllo di non aver raggiunto la tolleranza desiderata
            primo = not testMillerRabin(candidato, test) and algoritmoEstesoEuclide(candidato, test)[0] == 1
            if primo:
                test = random.randrange(2, candidato - 1)
                toll *= 1 / 4  # considero le probabilità di errore indipendenti tra loro
        if toll <= sogliatoll and primo:
            return candidato


def generaFattoriModulo(ordine):  # metodo che restituisce due possibili fattori casuali per il modulo RSA,
    # insieme al modulo stesso ottenuto moltiplicando i fattori
    p = generaNumPrimo(ordine // 2, 0.000001)  # genero casualmente due numeri primi
    q = generaNumPrimo(ordine // 2, 0.000001)
    while p == q:  # controllo di non aver generato due primi identici
        q = generaNumPrimo(ordine // 2, 0.000001)
    return p, q, p * q


def generaChiavi(p, q):  # Genero una chiave pubblica e una privata a partire dai due fattori primi del modulo RSA
    phi = (p - 1) * (q - 1)
    e = 3
    if phi % 3 != 0:
        d = algoritmoEstesoEuclide(e, phi)
        return e, d[1]
    while True:
        e += 1   # cerco una chiave pubblica che sia più piccola possibile
        d = algoritmoEstesoEuclide(e, phi)
        if d[0] == 1:
            return e, d[1]


def generaModuloChiavi(ordine):  # Metodo per generare chiavi, modulo e relativi fattori per la crittografia RSA
    p, q, n = generaFattoriModulo(ordine)  # genero i fattori e il modulo
    pub, priv = generaChiavi(p, q)  # genero la chiave pubblica e privata
    return pub, priv, n, p, q


def crittaRSA(messaggio, key, modulo):  # Metodo per cifrare e decifrare in maniera "classica" con RSA
    return esponenziazioneVeloce(messaggio, key, modulo)


def decifraCRT(c, d, p, q):  # Metodo di decifratura per il cifrario RSA che sfrutta il Teorema Cinese del Resto
    sp = esponenziazioneVeloce(c, d % (p - 1), p)  # computo i valori intermedi sp ed sq con esponente di ordine di
    # grandezza dimezzato rispetto all'algoritmo classico
    sq = esponenziazioneVeloce(c, d % (q - 1), q)
    invpq = algoritmoEstesoEuclide(p, q)  # calcolo i rispettivi inversi modulari di p e q tra loro stessi
    return (p * invpq[1] * sq + q * invpq[2] * sp) % (p * q)  # Applico la formula per ricavare il plaintext


if __name__ == '__main__':
    mcdinvtest = algoritmoEstesoEuclide(21072000, 3791)
    print("MCD tra 21072000 e 3791 ed inversi modulo 3791 ed 21072000: " + str(mcdinvtest))
    # testo la correttezza del'algoritmo esteso di Euclide
    assert (mcdinvtest[0] == 1)  # Testo il MCD
    assert ((21072000 * mcdinvtest[1]) % 3791 == 1)  # Testo la correttezza degli inversi modulari
    assert ((21072000 * mcdinvtest[1]) % 3791 == 1)
    # Testo la correttezza dell'algoritmo di esponenziazione veloce
    assert (esponenziazioneVeloce(5, 12, 21) == 1)
    print("Numero primo generato casualmente: " + str(generaNumPrimo(1700, 0.0001)))
    print()
    temposenzaCRT = [0.0] * 100
    tempoconCRT = [0.0] * 100
    e1, d1, mod, p1, q1 = generaModuloChiavi(3000)  # Genero modulo, con i rispettivi fattori, e chiavi casuali
    print("Inzio ciclo: ")
    for i in range(100):
        print("Esecuzione numero: " + str(i + 1))
        mess = random.randrange(2, 2 ** 2998)  # Genero un messaggio casuale minore del modulo con cui sto lavorando
        cyp = crittaRSA(mess, e1, mod)  # Cifro il messaggio generato
        inizio = time.time()
        m1 = crittaRSA(cyp, d1, mod)  # Cifro il messaggio "tradizionalmente"
        fine = time.time()
        temposenzaCRT[i] = fine - inizio  # Salvo il tempo di esecuzione
        inizioCRT = time.time()
        m2 = decifraCRT(cyp, d1, p1, q1)  # Cifro il messaggio sfruttando il CRT
        fineCRT = time.time()
        assert (m1 == m2 and m1 == mess)  # controllo che il messaggio originale e quelli decifrati siano identici
        tempoconCRT[i] = fineCRT - inizioCRT  # Salvo il tempo di esecuzione

    tempoSenzaRSA = sum(temposenzaCRT)  # ottengo la somma dei tempi di esecuzione
    tempoConRSA = sum(tempoconCRT)
    print("Tempo totale impiegato dall'implementazione senza CRT speed up: " + str(tempoSenzaRSA) + " secondi.")
    print("Tempo totale impiegato dall'implementazione con CRT speed up: " + str(tempoConRSA) + " secondi.")
    print("Speed up ottenuto complessivamente sulla decifratura di 100 messaggi: " + str(tempoConRSA / tempoSenzaRSA))
