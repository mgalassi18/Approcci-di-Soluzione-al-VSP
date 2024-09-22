
# Funzione per formattare una riga
def schema(row, widths):
    return "".join(str(item).ljust(width) for item, width in zip(row, widths))

