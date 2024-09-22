import gurobipy as gp
from gurobipy import GRB
import numpy
import json
import math
import glob
import os
import pandas as pd

from ModuloSeparatoreVertici import vertex_separator
from ModuloConteggio import numero_nodi
from ModuloConversione import leggi_file_e_trasforma_in_tuple
from ModuloEuristica import euristica
from ModuloFormmattazione import schema
def main():
    titoli = ["Nome File", "Funzione obiettivo", "Best Bound", "Ottimalità", "Cardinalità Grafo", "Tempo di Elaborazione", "F. Obiettivo E", "BB E", "T. E. E", "Tipo Sol. E", "Somma tempi eu", "Precisione Euristica"]
    tabella =  [30, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25]
    with open("risultati_1su2_TL300.txt", "w") as doc:
        doc.write(schema(titoli, tabella)+"\n")

        
    percorsiFile = glob.glob(os.path.join("Tesi_finale","Data_Paper_txt", '*.txt'))
    
    tabellaExcel =[]
    for file in percorsiFile:
        lista_tuple = leggi_file_e_trasforma_in_tuple(file)
        n =  math.floor(1/2*numero_nodi(file)) # La cardinalità massima di A e B
        
        tipo_funz_obiettivo, valore_funz_obiettivo, tempo_nec, lower_bound = vertex_separator(lista_tuple, n)
        
        
        tipo_funz_euristica, risultato_euristica,  miglior_bound_euristica, tempo_iterazione_utile, tempo_totale_euristica = euristica(lista_tuple, n, tempo_nec, lower_bound)
            
        precisione_euristica = (1-(risultato_euristica/valore_funz_obiettivo))*100

        tabellaExcel.append([str(os.path.basename(file)), valore_funz_obiettivo, lower_bound, str(tipo_funz_obiettivo), numero_nodi(file), tempo_nec, risultato_euristica, miglior_bound_euristica, tempo_iterazione_utile, tipo_funz_euristica, tempo_totale_euristica, precisione_euristica])
        with open("risultati_1su2_TL300.txt", "a") as documento:
            riga = [str(os.path.basename(file)), str(valore_funz_obiettivo), str(lower_bound), str(tipo_funz_obiettivo), str(numero_nodi(file)), str(tempo_nec), str( risultato_euristica), str(miglior_bound_euristica), str(tempo_iterazione_utile), str(tipo_funz_euristica), str(tempo_totale_euristica), str(precisione_euristica)+"%"]
            documento.write(schema(riga, tabella)+"\n")
    print(tabellaExcel)
    df = pd.DataFrame(tabellaExcel, columns = titoli)
    df.to_excel("trecentosecondiunmezzo.xlsx", index = False)
            
            

        

if __name__== "__main__":
    main()