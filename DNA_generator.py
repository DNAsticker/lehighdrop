import random

def is_reverse_complement(seq1, seq2):
    """Check if seq2 is the reverse complement of seq1."""
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    rev_comp = ''.join(complement[base] for base in reversed(seq1))
    return rev_comp == seq2

def has_self_complementarity(seq, window_size=4):
    """
    Checks for self-complementary regions in the sequence.
    Scans the sequence for any region whose reverse complement appears elsewhere.
    """
    for i in range(len(seq) - window_size + 1):
        window = seq[i:i+window_size]
        rev_comp = ''.join({'A':'T', 'T':'A', 'C':'G', 'G':'C'}[b] for b in reversed(window))
        if rev_comp in seq[i+1:]:  # Avoid overlap with the same region
            return True
    return False

def gc_content(seq):
    """Returns the GC content percentage of the sequence."""
    gc_count = seq.count('G') + seq.count('C')
    return 100 * gc_count / len(seq)

def generate_dna_sequence(length=90, gc_min=30, gc_max=60, max_attempts=10000):
    """Generates a non-self-hybridizing DNA sequence."""
    bases = ['A', 'T', 'C', 'G']
    attempts = 0
    while attempts < max_attempts:
        seq = ''.join(random.choice(bases) for _ in range(length))
        gc = gc_content(seq)
        if gc_min <= gc <= gc_max and not has_self_complementarity(seq):
            return seq
        attempts += 1
    raise ValueError("Failed to generate a suitable sequence after many attempts.")

# Example usage
if __name__ == "__main__":
    seq = generate_dna_sequence(length=90)
    print("Non-self-hybridizing DNA sequence:")
    print(seq)
