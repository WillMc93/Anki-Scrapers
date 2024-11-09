# Deck model IDs
GEN_CHEM_ID = 1632546100
AMINO_ACIDS_ID = 1730700145751

# Card model IDs
DEFINITION_ID = 1347303602

# Generate an ID
if __name__ == '__main__':
    import random
    print(random.randrange(1 << 30, 1 << 31))