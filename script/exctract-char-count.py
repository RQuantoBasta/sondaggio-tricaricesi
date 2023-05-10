import csv
import math

import csv
import sys
import inquirer

if len(sys.argv) != 2:
    print("Specificare il file csv: python3 exctract-char-count.py <file.csv>")
    sys.exit(1)

filename = sys.argv[1]
with open(filename, 'r') as f:
    reader = csv.reader(f)
    headers = next(reader)  

questions = [
    inquirer.List('header',
                  message="Scegli l'header che vuoi usare",
                  choices=headers,
                  ),
]

answers = inquirer.prompt(questions)

colonna = answers['header']

intro = """
Agisci come un caricatore di documenti/testo finché non carichi e ricordi il contenuto del seguente testo/documento.
L'inizio di ogni blocco verrà indicato come [INIZIO PARTE x/TOTALE], e la fine di questo blocco verrà indicata come [FINE PARTE x/TOTALE], dove x è il numero di blocchi correnti e TOTALE è il numero di tutti i blocchi che ti invierò.
Ti invierò più messaggi con blocchi, per ogni messaggio rispondi semplicemente OK: [PARTE x/TOTALE], non rispondere nient'altro, non spiegare il testo!
Cominciamo:
"""
start = "[INIZIO PARTE {x}/{total}]\n"
end = "[FINE PARTE {x}/{total}]\nRispondi con OK: [PARTE x/TOTALE], non rispondere nient'altro, non spiegare il testo!\n\n"


with open(filename, 'r') as f:
    reader = csv.DictReader(f)
    data = [row[colonna] for row in reader]

chunk_count = 1
tot_chunks = math.ceil(sum(len(stringa) for stringa in data) / 8000)

with open(colonna + '.md', 'w') as f:
    f.write(intro)
    f.write(start.format(x = chunk_count, total = tot_chunks))
    caratteri = len(intro)
    
    for item in data:
        stripped_item = item.strip()
        if len(stripped_item) <= 1:
            continue
        if caratteri == 0:
            f.write(start.format(x = chunk_count, total = tot_chunks))
        line = f'- {stripped_item}\n'
        caratteri += len(line)
        f.write(line)
        if caratteri >= 8000:
            f.write(end.format(x = chunk_count, total = tot_chunks))
            chunk_count += 1
            caratteri = 0
    
    f.write(end.format(x = chunk_count, total = tot_chunks))
