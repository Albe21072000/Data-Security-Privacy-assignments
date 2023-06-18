from collections import Counter
import math
import matplotlib.pyplot as plt


# 1)
def testoBase(testo: str) -> str:  # restituisce il testo con lettere minuscole senza caratteri aggiuntivi
    return "".join(x.lower() for x in testo if x.isalpha())


def istogrammaLettere(testo):
    return Counter(testoBase(testo))  # restituisco il contatore delle lettere nel testo con solo lettere minuscole


# 2)

def contangrammi(testo, lungh=1):  # metodo per contare gli ngrammi del testo
    testo = testoBase(testo)
    return Counter([testo[numgramma:numgramma + lungh] for numgramma in
                    range(len(testo) - lungh + 1)])  # prendo tutte le possibili sottostringhe di una data lunghezza


def distngrammi(testo, lungh=1):
    cont = contangrammi(testo, lungh)  # conto tutti gli ngrammi presenti nel testo
    totale = sum(cont.values())  # calcolo quanti ngrammi sono presenti nel testo
    for x in cont:
        cont[x] /= totale  # ottengo la distribuzione di ogni ngramma nel testo
    return cont


# 3)
def indiceCoincidenza(testo, lunghmgram=1):
    cont = contangrammi(testo, lunghmgram)  # conto gli ngrammi presenti nel testo
    lunghtesto = sum(cont.values())
    ic = 0  # variabile che conterrà l'indice di coincidenza calcolato
    for x in cont:
        ic += cont[x] * (cont[x] - 1)  # applico la formula per il calcolo dell'indice di coincidenza
    return ic / (lunghtesto * (lunghtesto - 1))  # ho portato fuori dalla sommatoria la divisione visto che è
    # comune per tutti gli addendi


def entropiaShannon(testo, lunghmgram=1):
    cont = distngrammi(testo, lunghmgram)  # conto gli ngrammi distinti presenti nel testo
    entr = 0  # variabile che conterrà il valore dell'entropia calcolato
    for x in cont:
        prob = cont[x]
        entr += prob * math.log2(prob)  # applico la formula per il calcolo dell'entropia
    return entr * -1


if __name__ == '__main__':  # evito che questo codice venga eseguito quando importo i metodi visti prima
    moby_dick = open("moby.txt", "r", encoding="utf8")
    text = moby_dick.read()
    moby_dick.close()
    dizhist = dict(istogrammaLettere(text))
    dizhist = {k: v for k, v in reversed(sorted(dizhist.items(), key=lambda item: item[1]))}  # ordino l'istogramma per
    # renderlo più comprensibile, in ordine decrescente in base alla frequenza delle lettere nel testo
    print("Istogramma delle frequenze delle lettere nel testo: " + str(dizhist))
    plt.bar(dizhist.keys(), dizhist.values())
    plt.show()
    for i in range(4):
        print(
            "Indice di coincidenza dei " + str(i + 1) + "-grammi: " + str(indiceCoincidenza(text, i + 1)))
        print("Entropia dei " + str(i + 1) + "-grammi: " + str(entropiaShannon(text, i + 1)))
    for i in range(4):
        dist = distngrammi(text, i + 1)
        print("Distribuzione empirica " + str(i + 1) + "-grammi: " + str(  # anche qui ordino gli n-grammi in base
            # alla frequenza per mostrare prima gli n-grammi più frequenti
            {k: v for k, v in reversed(sorted(dist.items(), key=lambda item: item[1]))}))
