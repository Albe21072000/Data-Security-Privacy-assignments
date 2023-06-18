from numpy import *
import itertools
import occorrenze


def algoritmoEstesoEuclide(a, n):  # sfrutto l'algoritmo esteso di Euclide per trovare il MCD, e l'inverso se MCD==1
    x = 0
    inva = 1
    resto = n
    MCD = a
    while resto != 0:
        quoziente = MCD // resto
        MCD, resto = resto, MCD - quoziente * resto  # evito di creare due variabili temporanee per scambiare i valori
        inva, x = x, inva - quoziente * x  # applico la formula per il calcolo iterativo dell'inverso di a
    return MCD, inva % n


def invertibile(matrice: ndarray, n=26) -> bool:  # controlla se la matrice è invertibile modulo n
    mcd = algoritmoEstesoEuclide(round(linalg.det(matrice)), n)[0]  # ricavo il MCD del determinante della matrice
    return mcd == 1


def costruisciElementoMatriceInversa(x, y, matrice: ndarray, detinv):
    arrdet = delete(matrice, y, 0)  # elimino la riga y e a colonna x
    arrdet = delete(arrdet, x, 1)
    return ((-1) ** ((x + 1) - (y + 1)) * detinv * round(linalg.det(arrdet))) % 26  # applico la formula per ottenere
    # un elemento della matrice inversa


def invertiMatrixMod(matrice: ndarray, base=26):
    det = round(linalg.det(matrice))  # ottengo il determinante della matrice
    dim = matrice.size ** 0.5  # ottengo il numero di righe/colonne della matrice quadrata
    # come radice quadrata del numero di elementi totali
    mat1 = zeros((int(dim), int(dim)))  # creo una matrice vuota
    mcddet = algoritmoEstesoEuclide(det, base)
    if mcddet[0] != 1:
        return None  # matrice non invertibile
    detinv = mcddet[1]  # determinante della matrice inversa
    for i in range(int(dim)):
        for j in range(int(dim)):
            mat1[i, j] = costruisciElementoMatriceInversa(i, j, matrice, detinv)  # costruisco la matrice inversa
            # elemento per elemento
    return mat1


def moltMatrixMod(matA, matB, base=26):  # moltiplica due matrici in modulo m
    return matmul(matA, matB) % base


def creaMatrBlocchi(text, dimblocco):  # metodo che genera una matrice che ha come colonne i blocchi in cui è diviso
    # il testo
    numvet = len(text) // dimblocco
    lista = [ord(x) - 97 for x in text]
    arr = []
    for i in range(numvet):
        arr.append(array(lista[dimblocco * i:dimblocco * (i + 1)]))
    return column_stack(arr)


def traformavetstr(vett: ndarray) -> str:  # trasforma un vettore in una stringa
    lista = vett.transpose().tolist()
    lista = [chr(int(el) + 97) for el in lista]  # trasformo i valori del vettore in caratteri
    return "".join(lista)


def encrypt(mess: str, chiave: ndarray):
    mess = occorrenze.testoBase(mess)  # elimino i caratteri che non siano lettere e rendo tutte le lettere minuscole
    lunchiave = chiave.shape[0]
    if lunchiave != chiave.shape[1]:  # numero di righe diverso da quello delle colonne
        print("Matrice della chiave non quadrata")
        return None
    if not invertibile(chiave):
        print("Matrice della chiave non invertibile, provare un'altra chiave!")
        return None
    if len(mess) % lunchiave != 0:
        print("Testo di lunghezza non adeguata, inserire caratteri di riempimento!")
        return None
    matrblocchi = creaMatrBlocchi(mess,
                                  lunchiave)  # genero la matrice contenente i vettori dei blocchi di testo cifrato
    fin = ""  # stringa che conterrà il testo cifrato
    for i in range(len(mess) // lunchiave):  # considero un blocco alla volta
        p = matrblocchi[:, i]  # prendo il vettore corrispondente al blocco e lo moltiplico per la chiave
        c = moltMatrixMod(chiave, p)  # ottengo il blocco cifrato
        fin += traformavetstr(c)  # concateno il blocco cifrato con la parte di testo che ho già cifrato
    return fin


def decrypt(ctext, chiave: ndarray):  # simile a quanto visto per la cifratura
    ctext = occorrenze.testoBase(ctext)
    lunchiave = chiave.shape[0]
    if lunchiave != chiave.shape[1]:
        print("Matrice della chiave non quadrata")
        return None
    if not invertibile(chiave):
        print("Matrice della chiave non invertibile, provare un'altra chiave!")
        return None
    if len(ctext) % lunchiave != 0:
        print("Testo di lunghezza non adeguata, inserire caratteri di riempimento!")
        return None
    matrblocchi = creaMatrBlocchi(ctext, lunchiave)
    fin = ""
    for i in range(len(ctext) // lunchiave):
        c = matrblocchi[:, i]
        p = moltMatrixMod(invertiMatrixMod(chiave), c)  # decifro il blocco moltiplicando la matrice della chiave
        # inversa per il vettore del blocco di testo cifrato
        fin += traformavetstr(p)  # concateno il testo decifrato volta volta
    return fin


def crittanalisiHill(plaintext, cyphertext, lunghchiave):
    if len(plaintext) != len(cyphertext):
        print("Il plaintext ed il cyphertext devono avere la stessa lunghezza")
        return None
    if len(plaintext) < lunghchiave ** 2:
        print("La lunghezza non è sufficiente per eseguire la crittanalisi!")
        return None
    matpt = creaMatrBlocchi(plaintext, lunghchiave)  # matrice composta dai vettori colona dei blocchi del testo in
    # chiaro
    matct = creaMatrBlocchi(cyphertext, lunghchiave)  # matrice composta dai vettori colona dei blocchi del testo
    # cifrato
    for i in itertools.combinations(range(len(plaintext) // lunghchiave), lunghchiave):  # ciclo su ogni possibile
        # combinazione dei blocchi di testo in chiaro di lunghezza pari a quella della chiave finché non ne trovo una
        # che dà origine a una matrice invertibile in modulo 26
        pstar = empty([lunghchiave, lunghchiave])
        c = empty([lunghchiave, lunghchiave])
        cont = 0
        for j in i:
            pstar[:, cont] = matpt[:, j]  # costruisco una possibile matrice del testo in chiaro
            c[:, cont] = matct[:, j]  # e la relativa matrice del testo cifrato
            cont += 1
        if invertibile(pstar):  # controllo se la matrice costruita è invertibile
            return moltMatrixMod(c, invertiMatrixMod(pstar))
    return None


pt = "Three Rings for the Elven-kings under the sky," \
     "Seven for the Dwarf-lords in their halls of stone, " \
     "Nine for Mortal Men doomed to die," \
     "One for the Dark Lord on his dark throne" \
     "In the Land of Mordor where the Shadows lie." \
     "One Ring to rule them all, One Ring to find them," \
     "One Ring to bring them all, and in the darkness bind them " \
     "In the Land of Mordor where the Shadows lie. "
if __name__ == '__main__':
    key = array([[3, 7, 9], [2, 1, 7], [1, 9, 2]])
    print(key)
    ct = encrypt(pt, key)
    print(ct)
    pt = decrypt(ct, key)
    print(pt)
    key = crittanalisiHill(pt, ct, 3)
    print(key)
