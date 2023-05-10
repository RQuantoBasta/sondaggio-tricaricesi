import csv

colonna = "Com'è la Tricarico che vorresti?"

with open('Risultati Intervista ai Cittadini.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = [row[colonna] for row in reader]

with open(colonna + '.md', 'w') as f:
    parole = 0
    for item in data:
        if len(item.strip()) <= 1:
            continue
        line = f'- {item}\n'
        parole += len(line.split())
        if parole >= 2000:
            f.write("----- fine parte -----\n")
            parole = len(line.split())
        f.write(line)
