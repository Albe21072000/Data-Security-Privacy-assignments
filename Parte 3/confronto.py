from codiciLZ import *
from huffman import *


def testoBase(testo: str) -> str:  # restituisce il testo con lettere minuscole senza punteggiatura
    return "".join(x.lower() for x in testo if x.isalpha())


path = "testo"
for i in range(10):
    print("Analizzo il testo numero: "+str(i + 1))
    file = open(path + str(i + 1), "r", encoding="utf8")  # apro ogni file allegato e lo leggo
    stringaNonCompressa = file.read()
    file.close()  # chiudo il file
    stringaPulita = testoBase(stringaNonCompressa)  # pulisco la stringa contenente il testo
    lunghezzaStringaNonCompressa = len(stringaPulita) * 5  # calcolo la lunghezza della rappresentazione del testo
    # non compresso che usa cinque bit per ciascuna lettera
    print("Lunghezza testo non compresso: " + str(lunghezzaStringaNonCompressa))
    compressioneHuffman = comprimiHuffman(stringaPulita)  # comprimo la stringa com l'algoritmo di Huffman
    # e ricavo il dizionario delle frequenze delle lettere
    lunghezzaHuffman = len(compressioneHuffman[0])  # ricavo la lunghezza della stringa compressa con Huffman
    compressioneLZ = comprimiStringaLZ(stringaPulita)  # comprimo la stringa con l'algoritmo Lempel-Ziv
    lunghezzaLZ = len(compressioneLZ)   # calcolo la lunghezza della stringa compressa
    # controllo che le due stringhe decompresse siano uguali a quella di partenza
    assert (decomprimiStringaLZ(compressioneLZ) == stringaPulita and
            decomprimiPrefixFree(compressioneHuffman[0], compressioneHuffman[1]) == stringaPulita)
    print("Lunghezza testo compresso con Huffman: " + str(lunghezzaHuffman))
    print("Lunghezza testo compresso con LZ: " + str(lunghezzaLZ))
    # Calcolo la percentuale di compressione di entrambi i metodi
    percentualeCompressioneHuffman = 100 - lunghezzaHuffman / lunghezzaStringaNonCompressa * 100
    percentualeCompressioneLZ = 100 - lunghezzaLZ / lunghezzaStringaNonCompressa * 100
    print("Percentuale compressione ottenuta con l'algoritmo di Huffman: " + str(percentualeCompressioneHuffman) + "%")
    print("Percentuale compressione ottenuta con l'algoritmo Lempel-Ziv: " + str(percentualeCompressioneLZ) + "%")
