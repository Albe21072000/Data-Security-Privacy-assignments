from algoritmiCrittografiaRSA import *


def algoritmoEstesoEuclideBezout(a, n):  # modifico leggermente l'algoritmo esteso di Euclide per fare in modo che
    # restituisca i coefficienti di Bezout invece degli inversi modulari
    x = 0
    y = 1
    coefa = 1  # Variabile che conterrà i valori intermedi del coefficiente di rabin associato ad a
    coefn = 0  # Variabile che conterrà i valori intermedi del coefficiente di rabin associato a n
    resto = n
    MCD = a  # variabile che conterrà il MCD tra a ed n
    while resto != 0:  # ciclo finché il resto della divisione non diventa pari a 0
        quoziente = MCD // resto
        MCD, resto = resto, MCD - quoziente * resto  # evito di creare due variabili temporanee per scambiare i valori
        coefa, x = x, coefa - quoziente * x  # applico la formula per il coefficiente di Rabin associato ad a
        coefn, y = y, coefn - quoziente * y  # applico la formula per ricavare il coefficiente di Rabin associato a n
    return MCD, coefa, coefn  # restituisco i coefficienti di Rabin invece degli inversi modulari


def esponenziazioneVeloceNegativa(base, esp, modulo):  # Metodo per calcolare anche elevamenti a potenza modulari
    # con esponenti negativi
    if esp >= 0:  # Se l'esponente è positivo applico l'algoritmo classico
        return esponenziazioneVeloce(base, esp, modulo)
    inveucl = algoritmoEstesoEuclide(base, modulo)  # ricavo MCD e i coefficienti di Bezout
    if inveucl[0] == 1:  # Se la base è invertibile rispetto al modulo esponenzio l'inverso per l'esponente moltiplicato
        # per meno uno (quindi eleverò per un numero positivo)
        return esponenziazioneVeloce(inveucl[1], esp * -1, modulo)
    print("Elevamento a potenza negativa non fattibile!")


def commonModulusFailure(cyphertext1, cyphertext2, chiave1, chiave2, modulo):
    mcd, x, y = algoritmoEstesoEuclideBezout(chiave1, chiave2)  # Ricavo MCD e coefficienti di Bezout delle due
    # chiavi pubbliche
    if mcd != 1:
        print("Le chiavi fornite non risultano coprime tra loro! Impossibile procedere!")
        return None
    return (esponenziazioneVeloceNegativa(cyphertext1, x, modulo) * esponenziazioneVeloceNegativa(cyphertext2, y,
                                                                                                  modulo)) % modulo  # applico
    # la formula per ricavare il plaintext


# Applico l'attacco con i parametri indicati nell'esercizio per ricavare il messaggio decifrato
m = commonModulusFailure(41545998005971238876458051627852835754086854813200489396433,
                         88414116534670744329474491095339301121066308755769402836577, 3, 11,
                         825500608838866132701444300844117841826444264266030066831623)
print(m)  # stampo il messaggio ottenuto dall'attacco
c1 = crittaRSA(m, 3, 825500608838866132701444300844117841826444264266030066831623)
assert (c1 == 41545998005971238876458051627852835754086854813200489396433)  # controllo la correttezza del risultato
# ottenuto
print(c1)
c2 = crittaRSA(m, 11, 825500608838866132701444300844117841826444264266030066831623)
assert(c2 == 88414116534670744329474491095339301121066308755769402836577)
print(c2)
