dna = "ATGCGTAA"
length = len(dna)
gc_count = dna.count("G") + dna.count("C")
gc_percentage = (gc_count / length) * 100

print(f"Sequence: {dna}")
print(f"Length: {length}")
print(f"GC percentage: {gc_percentage:.2f}%")