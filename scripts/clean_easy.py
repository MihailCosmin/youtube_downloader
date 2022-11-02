from tqdm import tqdm

with open("easylist.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

youtube = ["youtube", "yt", "google"]

with open("easylist_clean.txt", "w", encoding="utf-8") as f:
    f.write("")
for line in tqdm(lines[17:]):
    if any(ytb in line for ytb in youtube):
        with open("easylist_clean.txt", "a", encoding="utf-8") as f:
            f.write(line)
