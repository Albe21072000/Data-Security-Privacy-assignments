import string
import numpy as np
import occorrenze


def trovadistanzengmrammi(testo, lunghezza=3):
    testo = occorrenze.testoBase(testo)
    ngrammitot = np.array(
        [testo[i:lunghezza + i] for i in range(len(testo) - lunghezza + 1)])  # trovo tutti gli ngrammi del testo
    ngrammidist = np.unique(ngrammitot)  # trovo tutti gli ngrammi distinti
    distanze = {}
    for ngramma in ngrammidist:
        rip = np.where(ngrammitot == ngramma)[0]  # cerco tutte le occorrenze dello stesso ngramma
        if len(rip) > 1:
            distanze[ngramma] = (np.diff(rip)).tolist()  # se ne trovo più di uno calcolo la distanza tra essi
    return distanze


def vettcifrsost(txt, shift, passo):  # per ricavare testo cifrato a sostituzione
    return "".join(list(txt)[passo:len(txt):shift])  # restituisco la stringa di caratteri del testo che sono
    #  distanti per una lunghezza pari al valore del parametro passo partendo dal carattere indicato dal parametro shift


def trovalunghchiave(text: str, inf=2, sup=14):
    scartomin = 100000000
    lunghfin = 0
    icrighe = []  # lista per contenere gli indici di coincidenza associata alla lunghezza della chiave ricavata
    for lungchiave in range(inf, sup + 1):
        scartotemp = 0
        icrighetemp = []
        for shift in range(lungchiave):
            testoalternato = vettcifrsost(text, lungchiave,
                                          shift)  # trovo la sottostringa del testo che dovrebbe essere cifrata come
            # in un cifrario a sostituzione
            icrighetemp.append(occorrenze.indiceCoincidenza(testoalternato))
            scartotemp += (icrighetemp[shift] - 0.065) ** 2  # calcolo lo scarto quadratico
            # dell'indice di coincidenza della stringa da quello atteso per un testo in lingua inglese
        scartoquadmed = (scartotemp / lungchiave) ** 0.5
        if scartomin > scartoquadmed:  # confronto gli scarti quadratici medi
            scartomin = scartoquadmed  # se lo scarto quadratico medio trovato è minore di quelli calcolati
            # in precedenza aggiorno la lunghezza della chiave e il valore minimo di tale scarto
            icrighe = icrighetemp  # aggiorno anche gli indici di coincidenza associati alla lunghezza della chiave
            lunghfin = lungchiave
    print("Indici di coincidenza associati alla lunghezza della chiave: " + str(icrighe))
    print(
        "Scarto quadratico medio dal valore standard dell'indice di coindienza per un testo in lingua inglese: " + str(
            scartomin))
    return lunghfin


def vettord(testo):  # metodo per ordinare il vettore delle frequenze in ordine alfabetico, considerando anche le
    # lettere che non appaiono nella sottostringa, assegnando loro frequenza pari a zero
    contalettere = occorrenze.distngrammi(testo, 1)
    vettorelet = np.zeros(26)
    counter = 0
    for x in string.ascii_lowercase:
        vettorelet[counter] = contalettere.get(x)
        counter += 1
    vettorelet[np.isnan(vettorelet)] = 0
    return vettorelet


def trovachiave(testo, lungchiave):
    key = ""
    vetting = np.array(
        [0.082, 0.015, 0.028, 0.043, 0.13, 0.022, 0.02, 0.061, 0.07, 0.0015, 0.0077, 0.04, 0.024, 0.067, 0.075, 0.019,
         0.00095, 0.06, 0.063, 0.091, 0.028, 0.0098, 0.028, 0.0015, 0.02, 0.00074])  # vettore delle frequenze delle
    # lettere standard per un testo in lingua inglese
    for i in range(lungchiave):
        testosost = vettcifrsost(testo, lungchiave, i)  # ottengo testo cifrato con sostituzione
        vettlettere = vettord(testosost)  # ricavo il vettore della distribuzione di probabilità delle lettere nel testo
        prod = 0
        lett = 0  # variabile che conterrà il valore della lettera trovata
        for j in range(26):
            prodtemp = np.dot(vetting, np.roll(vettlettere, -1 * j))  # calcolo il prodotto scalare tra il
            # vettore delle frequenze delle lettere nella stringa shiftato di j posizioni verso sinistra ed il
            # vettore delle frequenze caratteristiche della lingua inglese
            if prod < prodtemp:
                prod = prodtemp  # scelgo il valore che massimizza il prodotto scalare
                lett = j
        key = key + chr(lett + 97)  # compongo la chiave di cifratura
        print("Carattere trovato: " + chr(lett + 97) + ", con prodotto scalare pari a: " + str(prod))
    return key


def decrittaVigenere(testo, chiave):  # metodo che esegue la decryption per il cifrario di Vigenère
    listatesto = [x for x in testo]
    listachiave = [ord(x) for x in chiave]
    for i in range(len(testo)):
        listatesto[i] = chr(((ord(listatesto[i]) - listachiave[i % len(chiave)]) % 26) + 97)  # eseguo la sottrazione
        # modulo 26 tra il carattere del testo cifrato e il valore della chiave corrispondente per ricavare il valore
        # della lettera originale nel testo in chiaro
    return "".join(listatesto)


def crittanalisiVigenere(testo: str, lungchiavemax=20):  # sfrutto tutti metodi definiti in precedenza per eseguire
    # l'attacco in automatico
    testo = occorrenze.testoBase(testo)
    lunghezza_chiave = trovalunghchiave(testo, sup=lungchiavemax)
    print('Lunghezza chiave: ' + str(lunghezza_chiave) + ' caratteri')
    chiave = trovachiave(testo, lunghezza_chiave)
    print('Chiave: "' + chiave + '"')
    return decrittaVigenere(testo, chiave)


testocrit = 'OKZARVGLNSLFOQRVVBPHHZAMOMEVHLBAITLZOWSXCSZFEQFICOOVDXCIISOOVXEIYWNHHLVQHSOWD' \
            'BRPTTZZOWJIYPJSAWQYNOYRDKBQKZPHHTLIHDEMICGYMSEVHKVXTQPBWMEWAZZKHLJMOVEVHJYSJR' \
            'ZTUMCVDGLZVBUIWOCPDZVEIGSOGZRGGOTAHLCSRSCXXAGPDYPSYMECRVPFHMYWZCYHKMCPVBPHYIF' \
            'WDZTGVIZEMONVYQYMCOOKDVQIMSOKLBUEBFZISWSTVFEWVIAWACCGHDRVVZOOBANRYHSSQBUIMSDW' \
            'VBNRXSSOGLVWKSCGHLNRYHSSQLVIYCFHVWJMOVEKRKBQMOOSVQAHDGLGWMEOMCYOXMEEIRTZBCFLZ' \
            'BVCVPRQVBLUHLGSBSEOUWHRYHSSEIEVDSCGHZRGOSOPBBUIQWNHRZFEIRPBWMEXCSPASBLXZFCWWW' \
            'EMZGLDDBUIOWNTHVPICOOTRZOMYRPBKMEIIHCOQKRWCSNFRAFIYWEKLBUSPHEVHAYMBVESVBGVZAZ' \
            'FVPRAJIWRQMIIMUZPDKXXJHSSRBUIMGTRHBUIMSHCXTQFZBZFHBHVIOYRWPRXCFPSRNGLZAVBHEVX' \
            'OVPMZMEIAIWZBIJEMSEVDBGLZMHSUMGVVWWWQOGLZCCPLARWYSNZLVRXCOEHKMLAZFPGLVXMIUHWW' \
            'PVXDBECWPRJDBLZQQTLOALFHBUIKOEVZWHPYPPRLNSMXIWHWPNXOCZHKMLOISH'
if __name__ == '__main__':
    print(trovadistanzengmrammi(testocrit))
    print("Testo decifrato: " + crittanalisiVigenere(testocrit))
