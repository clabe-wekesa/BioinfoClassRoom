# Read a FASTA file containing just one sequence.
with open("sequence.fasta", "r") as file:
    header = file.readline().strip()  # Read the first line (the header).
    sequence = ""                   # Start with an empty string.

    for line in file:
        sequence = sequence + line.strip()  # Join the sequence lines.

print(header)
print(sequence)
print("Sequence length:", len(sequence), "bases")
