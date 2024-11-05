# Deck model IDs
GEN_CHEM_ID_RANGE = [i for i in range(1632546100, 1632546122)]

# Card model IDs
DEFINITION_ID = 1347303602

# Generate an ID
if __name__ == '__main__':
    import random
    print(random.randrange(1 << 30, 1 << 31))