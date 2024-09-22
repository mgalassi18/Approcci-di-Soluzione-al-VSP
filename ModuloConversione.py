def leggi_file_e_trasforma_in_tuple(nome_file):
   
    try:
        # Aprire il file in modalità lettura
        with open(nome_file, 'r') as file:
            # Inizializzare una lista vuota per conservare le tuple
            lista_di_tuple = []
            
            
            # Leggere il file riga per riga
            for linea in file:
                # Rimuovere eventuali spazi bianchi e suddividere la riga per lo spazio
                dati = linea.strip().split()


                
                # Assicurarsi che ci siano almeno 2 colonne
                if len(dati) >= 2 and dati[0] =="e":
                    # Prendere i dati della colonna 1 e 2 e convertirli in una tupla
                    tupla = (dati[1].strip(), dati[2].strip())
                    # Aggiungere la tupla alla lista
                    lista_di_tuple.append(tupla)
        
        return lista_di_tuple
    except FileNotFoundError:
        print(f"Errore: Il file '{nome_file}' non è stato trovato.")
        return []