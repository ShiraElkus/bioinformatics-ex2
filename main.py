import random

# The cipher file.
CIPHERFILE = "enc.txt"

# The frequency of letters.
LETTERFREQ = "Letter_Freq.txt"

# The frequency of letter pairs.
LETTERFREQ2 = "Letter2_Freq.txt"

# The frequency of letter.
LETTERFREQ_dict = {}

# The frequency of combinations.
LETTERFREQ2_dict = {}

# The dictionary file.
DICTFILE = "dict.txt"

# The population amount for the genetic algorithm.
POPULATION_AMOUNT = 0

# The amount of top solutions to keep.
CARRY_POPULATION = 0

# The mutations amount for each iteration.
MUTATIONS = 0

CROSSOVERS = 0


def amount_in_text(cipher_text, option=1):
    # Get the amount of abc characters.
    amount = 0
    file_name = ""
    file_dict = {}
    if option == 1:
        amount = len("".join([char for char in cipher_text if char.isalpha()]))
        file_name = LETTERFREQ
        file_dict = LETTERFREQ_dict
    else:
        for i in range(len(cipher_text) - 1):
            if cipher_text[i].isalpha() and cipher_text[i + 1].isalpha():
                amount += 1
        file_name = LETTERFREQ2
        file_dict = LETTERFREQ2_dict
    with open(file_name, "r") as f:
        for line in f:
            if line == "\n":
                break
            freq, letter = line.rstrip('\n').split()
            freq = float(freq)
            file_dict[letter] = int(freq * amount)


def decode(cipher_text):
    pass


if __name__ == "__main__":
    with open(CIPHERFILE, "r") as f:
        ciphertext = f.read().upper()
    amount_in_text(ciphertext)
    amount_in_text(ciphertext, option=2)
    decode(ciphertext)
