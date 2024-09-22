import gurobipy as gp
from gurobipy import GRB
import numpy
import json
import math

def vertex_separator(spigoli, n):
    model = gp.Model("vertex_separator")
    model.Params.TimeLimit = 300
    

    
    vertici = set()
    for u, v in spigoli:    
        vertici.add(u)
        vertici.add(v)
    vertici = list(vertici)


    #Per ogni vertice, si creano due variabili binarie che indicano l'appartenza ad A e B
    y = model.addVars(vertici, vtype=GRB.BINARY, name="y")
    z = model.addVars(vertici, vtype=GRB.BINARY, name="z")

    # Massimizzare la cardinalità di A + B
    model.setObjective(gp.quicksum(y[i]+z[i] for i in vertici), GRB.MAXIMIZE)

    # Appartenenza ad un solo sottoinsieme
    for i in vertici:
        model.addConstr(y[i] + z[i] <= 1, name=f"one_set_{i}")

    # Limite superiore per A e B
    model.addConstr(gp.quicksum(y[i] for i in vertici) <= n, name="cardinalità_A")
    model.addConstr(gp.quicksum(z[i] for i in vertici) <= n, name="cardinalità_B")

    # Nessuno spigolo tra A e B
    for u, v in spigoli:
        model.addConstr(y[u] + z[v] <= 1, name=f"no_edge_A_B_{u}_{v}")
        model.addConstr(z[u] + y[v] <= 1, name=f"no_edge_B_A_{u}_{v}")
    
    # Ottimizzare il modello
    model.optimize()
    tipo_risultato = model.status
    valore_risultato = model.ObjVal
    valore_lowerbound= model.ObjBound
    tempo = model.Runtime

   
    A = [i for i in vertici if y[i].x > 0.5]
    B = [i for i in vertici if z[i].x > 0.5]
    

    return tipo_risultato, valore_risultato, tempo, valore_lowerbound

