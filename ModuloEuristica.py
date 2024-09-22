import gurobipy as gp
from gurobipy import GRB
import numpy
import json
import math
import random

def euristica(spigoli, n, tempo_limite, miglior_risultato_raggiungibile):
    
    
    #RISULTATI:
    valore_euristica_finale = 10000
    tipo_euristica_finale=0
    tempo_euristica_finale = 0
    best_bound_euristica_finale = 0

    
    vertici = set()
    for u, v in spigoli:    
        vertici.add(u)
        vertici.add(v)
    vertici = list(vertici)
    #il codice seguente non è ancora inserito nella versione ufficiale, ma sewrve per il calcolo del grado,
    #imponendo il sort ottengo anche una lista ordinata in base al grado, questo mi permetterà di utilizzare solo i vertici di grado massimo
    
    tabella_grado_vertici=[]
    for elemento in vertici:
        tabella_grado_vertici.append([elemento, 0])
        
    for elemento in tabella_grado_vertici:
        conteggio = 0
        for coppia in spigoli:
            if elemento[0] in coppia:
                conteggio = conteggio +1
        elemento[1] = conteggio
    tabella_grado_vertici.sort(key=lambda x: x[1], reverse=True) #questa funzione da ChatGPT 
    #print(tabella_grado_vertici)
    #fine del codice per il conteggio del grado
    ##relativamente all'ordine creato in tabella vertici, posso o ciclare e trovarli in "vertici", o eliminare il conteggio del grado 
    # e andare a prendere i primi, suppongo che la migliore tecnica sia quella di usare una funzione
    #random sui primi xx% in modo da avere più casistiche
    lista_vertici_ordinata=[]
    for elemento in tabella_grado_vertici:
        lista_vertici_ordinata.append(elemento[0]) #qui ho creato una lista con i vertici in ordine di grado decrescente
    numero_vertici_estrazione=math.floor(0.4*len(lista_vertici_ordinata)) #indica la percentuale di vertici tra i quali voglio estrarre 
    vertici_fissi = set()
    numero_vertici_euristica = math.floor(0.15*len(lista_vertici_ordinata))
    somma_tempi = 0
    migliorabile = True
    while somma_tempi < tempo_limite and somma_tempi<300 and migliorabile == True:
        while len(vertici_fissi)< numero_vertici_euristica:
            vertici_fissi.add(random.choice(lista_vertici_ordinata[:numero_vertici_estrazione]))
        model = gp.Model("euristica")
        model.Params.TimeLimit=tempo_limite
    
    #Per ogni vertice, si creano due variabili binarie che indicano l'appartenza ad A e B
        y = model.addVars(vertici, vtype=GRB.BINARY, name="y")
        z = model.addVars(vertici, vtype=GRB.BINARY, name="z")

    # Massimizzare la cardinalità di A + B
        model.setObjective(gp.quicksum(y[i]+z[i] for i in vertici), GRB.MAXIMIZE)
    
    #euristica con appartenenza al sottoinsieme C
        for i in vertici_fissi:
            model.addConstr(y[i] == 0, name= "euristica_A")
            model.addConstr(z[i] == 0, name= "euristica_B")
                        
    # Appartenenza ad un solo sottoinsieme
        for i in vertici:
            model.addConstr(y[i] + z[i] <= 1, name=f"univocità_{i}")

    # Limite superiore per A e B
        model.addConstr(gp.quicksum(y[i] for i in vertici) <= n, name="cardinalità_A")
        model.addConstr(gp.quicksum(z[i] for i in vertici) <= n, name="cardinalità_B")

    # Nessuno spigolo tra A e B
        for u, v in spigoli:
            model.addConstr(y[u] + z[v] <= 1, name=f"no_collegamenti_A_B_{u}_{v}")
            model.addConstr(z[u] + y[v] <= 1, name=f"no_collegamenti_B_A_{u}_{v}")
        #model.write('prova.lp')
        #Ottimizzare il modello
        model.optimize()
        stato_del_risultato = model.status   
        valore_risultato = model.ObjVal
        valore_lowerbound= model.ObjBound
        tempo = model.Runtime
        somma_tempi=somma_tempi+tempo
        if valore_risultato < valore_euristica_finale:
            valore_euristica_finale = valore_risultato
            tipo_euristica_finale = stato_del_risultato
            best_bound_euristica_finale = valore_lowerbound
            tempo_euristica_finale = tempo
        if valore_risultato == miglior_risultato_raggiungibile:
            migliorabile = False
            
        #print("SOMMA TEMPI =" + str(somma_tempi))
        A = [i for i in vertici if y[i].x > 0.5]
        B = [i for i in vertici if z[i].x > 0.5]
        #print(A)
        #print(B)
        #print(vertici_fissi)
        #print(set(vertici)-set(A)-set(B))

    return tipo_euristica_finale, valore_euristica_finale, best_bound_euristica_finale, tempo_euristica_finale, somma_tempi



