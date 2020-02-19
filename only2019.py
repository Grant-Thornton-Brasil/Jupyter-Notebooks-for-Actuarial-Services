from glob import glob
from tqdm import tqdm

files = glob("*.txt")
files

new_376 = open("376_2019.txt", "a+")
new_377 = open("377_2019.txt", "a+")
new_378 = open("378_2019.txt", "a+")
new_404 = open("404_2019.txt", "a+")
new_405 = open("405_2019.txt", "a+")
new_406 = open("406_2019.txt", "a+")
new_407 = open("407_2019.txt", "a+")
new_408 = open("408_2019.txt", "a+")
new_409 = open("409_2019.txt", "a+")
new_419 = open("419_2019.txt", "a+")
new_420 = open("420_2019.txt", "a+")
new_421 = open("421_2019.txt", "a+")
new_423 = open("423_2019.txt", "a+")



for file in files:
    with open(file) as old:
        print(f"Processing {file}")
        file = file.replace(".txt","_")
        for line in tqdm(old.readlines()):
            line = line.strip()
            if len(line) == 126:
                # 376
                if line[12:16] == "2019":
                    new_376.write(line+"\n")
            elif len(line) == 101:
                # 377
                if line[12:16] == "2019":
                    new_377.write(line+"\n")
            elif len(line) == 173 and line[20:23] == "378":
                # 378
                if line[12:16] == "2019":
                    new_378.write(line+"\n")
            elif len(line) == 133 and line[27] not in ["+", "-"]:
                # 404
                if line[12:16] == "2019":
                    new_404.write(line+"\n")
            elif len(line) == 132:
                # 405
                if line[12:16] == "2019":
                    new_405.write(line+"\n")
            elif len(line) == 130:
                # 406
                if line[12:16] == "2019":
                    new_406.write(line+"\n")
            elif len(line) == 129:
                # 407
                if line[12:16] == "2019":
                    new_407.write(line+"\n")
            elif len(line) == 173:
                # 408
                if line[12:16] == "2019":
                    new_408.write(line+"\n")
            elif len(line) == 172:
                # 409
                if line[12:16] == "2019":
                    new_409.write(line+"\n")
            elif len(line) == 133:
                # 419
                if line[11:15] == "2019" and line[27] in ["+", "-"]:
                    new_419.write(line+"\n")
            elif len(line) == 59:
                # 420
                if line[11:15] == "2019":
                    new_420.write(line+"\n")
            elif len(line) == 52:
                # 421
                if line[11:15] == "2019":
                    new_421.write(line+"\n")
            elif len(line) == 38:
                # 423
                if line[11:15] == "2019":
                    new_423.write(line+"\n")


new_376.close()
new_377.close()
new_378.close()
new_404.close()
new_405.close()
new_406.close()
new_407.close()
new_408.close()
new_409.close()
new_419.close()
new_420.close()
new_421.close()
new_423.close()
