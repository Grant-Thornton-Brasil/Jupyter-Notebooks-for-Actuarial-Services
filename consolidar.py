from glob import glob

arquivos = glob("*.txt")

with open("consolidado.txt", "a+") as new:
    for arquivo in arquivos:
        with open(arquivo) as old:
            for line in old.readlines():
                if line not in [None, ""]:
                    new.write(line.strip()+"\n")
