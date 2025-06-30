import csv
import os

txt_path = "dicionarios/port_WFD.txt"
out_path = "dicionarios/pt-br.txt"

if not os.path.exists(txt_path):
    raise Exception("Arquivo port_200k.txt não baixado corretamente")

# latin1 evita erro de encoding do txt
with open(txt_path, encoding="latin1") as f_in, open(out_path, "w", encoding="utf-8") as f_out:
    lines = f_in.readlines()
    if len(lines) < 10 or "word" not in lines[2]:
        raise Exception("O arquivo baixado não parece ser o corpus esperado.")
    reader = csv.reader(lines[3:], delimiter="\t")
    for row in reader:
        if len(row) >= 3 and row[1].isalpha():
            f_out.write(f"{row[1]}\t{row[2]}\n")
