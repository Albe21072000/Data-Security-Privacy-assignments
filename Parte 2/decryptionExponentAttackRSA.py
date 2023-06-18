from algoritmiCrittografiaRSA import *
import time
import numpy as np


def decryptionexp(n, e, d):
    it = 0  # Tengo conto del numero di esecuzioni dell'algoritmo
    m = e * d - 1
    r = 0
    while m % 2 == 0:  # mi ricavo il numero dispari m e il numero d'iterazioni massimo (lo faccio solo
        # per chiarezza, potrei anche non calcolarlo
        # visto che prima o poi troverò comunque un valore di x pari a uno)
        m //= 2
        r += 1
    while True:  # ciclo finché non trovo un valore di x che mi permetta di ottenere la fattorizzazione
        it += 1  # aggiorno il numero di esecuzioni dell'algoritmo
        x = random.randrange(n)  # scelgo un numero casuale per impostare l'attacco
        if algoritmoEstesoEuclide(x, n)[0] != 1:
            print("Ho trovato subito la fattorizzazione!")
            return 0, algoritmoEstesoEuclide(x, n)[1], n // algoritmoEstesoEuclide(x, n)[1]
        x = esponenziazioneVeloce(x, m, n)  # mi ricavo il primo valore di x
        if x != n - 1 and x != 1:
            for _ in range(r + 1):  # ciclo finch non trovo un x pari a più o meno uno
                xtemp = x  # mi salvo il vecchio valore di x
                x = esponenziazioneVeloce(x, 2, n)
                if x == n - 1:  # nel caso (sfortunato) che trovi un valore di x congruente in modulo n a -1,
                    # riparto scegliendo un altro numero di partenza
                    break
                if x == 1:  # appena trovo un valore di x pari a uno calcolo il MCD tra il precedente x (che sono
                    # sicuro conterrà un fattore in comune con il modulo) e il modulo stesso
                    mcd = algoritmoEstesoEuclide(xtemp - 1, n)[0]
                    return it, mcd, n // mcd  # una volta trovato un fattore, l'altro lo ricavo con la
                    # divisione (intera) del modulo per il fattore


# Test con 100 moduli generati casualmente dell'ordine circa di 10^150
tempoexe = [0.0] * 100
numit = [0] * 100
for i in range(100):
    e1, d1, num, p1, q1 = generaModuloChiavi(500)  # genero chiavi e fattori per un modulo con ordine di grandezza 2^500
    inizio = time.time()
    ris = decryptionexp(num, e1, d1)  # applico l'attacco
    fine = time.time()
    numit[i] = ris[0]
    tempoexe[i] = fine - inizio  # ricavo il tempo impiegato a eseguire l'attacco
    assert (p1 == ris[1] or p1 == ris[2]) and (q1 == ris[1] or q1 == ris[2])  # controllo la correttezza
    # del risultato dell'attacco
print("Numero medio iterazioni per esecuzione: " + str(sum(numit) / 100))
print("Tempo medio per esecuzione: " + str(sum(tempoexe) / 100) + " secondi")
var = np.var(tempoexe)  # ricavo la varianza dei tempi di esecuzione
print("Varianza tempi di esecuzione: " + str(var) + " secondi al quadrato")
print("Deviazione standard: " + str(var ** 0.5) + " secondi")
