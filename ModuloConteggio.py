def numero_nodi(file_name):
    try:
        with open(file_name, 'r') as doc:
            count =0
            for line in doc:
                data= line.strip().split()
                if data and data[0]=="v":
                    count = count+1
        return count
    except FileNotFoundError:
        print(f"Errore: Il file '{file_name}' non è stato trovato.")
        return exit #qui mi da un quitter