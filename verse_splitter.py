from pathlib import Path

# -------- Paden --------
base_dir = Path(r"D:\Christian")
bible_file = base_dir / "Bible.txt"
bijbel_dir = base_dir / "Bijbel"

# -------- Bestand lezen --------
lines = bible_file.read_text(encoding="utf-8").splitlines()

book_counts = {}  # {boek: {hoofdstuk: aantal verzen}}
total_verses = 0

for line in lines:
    line = line.strip()
    if not line:
        continue  # lege regels overslaan

    # Split op tab
    try:
        ref, text = line.split("\t", 1)
    except ValueError:
        continue  # geen tab gevonden, overslaan

    # Split boeknaam en hoofdstuk:vers vanaf rechts
    try:
        parts = ref.rsplit(" ", 1)
        book_name = parts[0]
        chap_verse = parts[1]
        chapter_str, verse_str = chap_verse.split(":", 1)
        chapter = int(chapter_str)
        verse = int(verse_str)
    except (ValueError, IndexError):
        print(f"Skipping malformed line: {line}")
        continue

    # Map per boek en hoofdstuk maken
    chapter_path = bijbel_dir / book_name / str(chapter)
    chapter_path.mkdir(parents=True, exist_ok=True)

    # Bestandsnaam: vers_<vers>.bf
    verse_file = chapter_path / f"vers_{verse}.bf"
    verse_file.write_text(ref + " " + text.strip(), encoding="utf-8")

    # Statistieken
    if book_name not in book_counts:
        book_counts[book_name] = {}
    book_counts[book_name][chapter] = book_counts[book_name].get(chapter, 0) + 1
    total_verses += 1

# -------- Output --------
print("\nAangemaakte verzen per boek en hoofdstuk:\n")
for book in sorted(book_counts):
    print(f"{book}:")
    for chap in sorted(book_counts[book]):
        print(f"  Hoofdstuk {chap:2}: {book_counts[book][chap]} verzen")
print(f"\nTotaal aangemaakte .bf-bestanden: {total_verses}")
