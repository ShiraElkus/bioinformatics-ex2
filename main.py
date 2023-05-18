import math
import random
import sys
from collections import Counter

# The cipher file.
CIPHERFILE = "enc.txt"

# The dictionary file.
DICTFILE = "dict.txt"

# The alphabet.
CHARS = "abcdefghijklmnopqrstuvwxyz"

# The frequency of letter.
LETTERFREQ_dict = {}

# The frequency of combinations.
LETTERFREQ2_dict = {}

# Word in english.
WORDS = []

# The population amount for the genetic algorithm.
POPULATION_AMOUNT = 100

# The amount of top solutions to keep.
CARRY_POPULATION = 5

# The mutations amount for each iteration.
MUTATIONS = 1

# The crossovers amount for each iteration.
CROSSOVERS = 4

# The amount of intervals for which the best score has to be stable before aborting the genetic algorithm.
STABILITY_INTERVALS = 20

# The amount of letters in the cipher text.
LETTERS_AMOUNT = 0

# The amount of combinations in the cipher text.
COMBINATIONS_AMOUNT = 0

# The amount of changes in the mapping.
CHANGES_AMOUNT = 10

# The method way
METHOD = sys.argv[1]


def amount_in_text(cipher_text, option=1):
    # Get the amount of abc characters.
    amount = 0
    if option == 1:
        # Get the amount of abc characters.
        global LETTERS_AMOUNT
        amount = len("".join([char for char in cipher_text if char.isalpha()]))
        LETTERS_AMOUNT = amount
        # Set the right file name and dict.
        file_name = "Letter_Freq.txt"
        file_dict = LETTERFREQ_dict
    else:
        # Get the amount of ab combinations.
        global COMBINATIONS_AMOUNT
        for i in range(len(cipher_text) - 1):
            if cipher_text[i].isalpha() and cipher_text[i + 1].isalpha():
                amount += 1
        COMBINATIONS_AMOUNT = amount
        # Set the right file name and dict.
        file_name = "Letter2_Freq.txt"
        file_dict = LETTERFREQ2_dict
    with open(file_name, "r") as f:
        # Get the frequency of each letter/combination.
        for line in f:
            if line == "\n":
                break
            freq, letter = line.rstrip('\n').split()
            letter = letter.lower()
            freq = float(freq)
            # Add the frequency to the dict.
            file_dict[letter] = int(freq * amount)


def init_population():
    # A set for all the characters.
    keys, values = set(CHARS), set(CHARS)
    mapping = {}
    for char in keys:
        # Get a random value from the values set.
        value = random.choice(list(values))
        # Add the key-value pair to the mapping.
        mapping[char] = value
        # Remove the value from the values set.
        values.remove(value)
    return mapping


def crossover(cross1, cross2):
    # Copy the first solution to the next iteration and cross it with the second solution.
    for i in range(CROSSOVERS):
        # Get a random key from the first solution.
        key = random.choice(list(cross1.keys()))
        # Swap the values of the key in the first solution and the second solution.
        cross1[key] = cross2[key]
    return cross1


def mutate(cross, value):
    # Copy the solution.
    for i in range(value):
        # Get a random key from the solution.
        key = random.choice(list(cross.keys()))
        # Get a random value from the solution.
        value = random.choice(list(cross.values()))
        # Swap the values of the key in the solution.
        cross[key], cross[value] = cross[value], cross[key]
    return cross


def fix_mapping(mapping):
    # If a letter appears twice in the mapping, swap the values.
    non_appearing_letters = list(set(mapping.values()) - set(mapping.keys()))
    if not non_appearing_letters:
        return mapping
    counting = Counter(mapping.values())
    for key in mapping:
        if counting[mapping[key]] >= 1:
            # Get a random key from the mapping.
            mapping[key] = random.choice(non_appearing_letters)
            non_appearing_letters.remove(mapping[key])
    return mapping


def generate_more_population(population):
    # Copy the population.
    new_population = population[:]
    while len(new_population) < POPULATION_AMOUNT:
        # Get two random solutions from the population.
        cross1, cross2 = random.choice(population), random.choice(population)
        # Copy the first solution to the next iteration and cross it with the second solution.
        new_cross1 = cross1.copy()
        new_cross1 = crossover(new_cross1, cross2)
        # Mutate the first solution.
        new_cross1 = mutate(new_cross1, MUTATIONS)
        new_cross1 = fix_mapping(new_cross1)
        new_population.append(new_cross1)
    return new_population


def decode_text(cipher_text, mapping):
    decoded_text = ""
    for char in cipher_text:
        if char.isalpha():
            decoded_text += mapping[char]
        else:
            decoded_text += char
    return decoded_text


def fitness(cipher_text, population):
    scores = []
    # Get the fitness score for each solution.
    for mapping in population:
        letter_appearances = {}
        pair_appearances = {}
        # Decode the text with the mapping.
        if METHOD != 0:
            new_mapping = mutate(mapping, CHANGES_AMOUNT)
        else:
            new_mapping = mapping
        decoded_text = decode_text(cipher_text, new_mapping)
        # Get the amount of appearances of each letter and pair.
        for letter in CHARS:
            if letter.isalpha():
                letter_appearances[letter] = decoded_text.count(letter)
        for i in range(len(decoded_text) - 1):
            if decoded_text[i].isalpha() and decoded_text[i + 1].isalpha():
                if decoded_text[i:i + 2] not in pair_appearances:
                    pair_appearances[decoded_text[i:i + 2]] = 0
                pair_appearances[decoded_text[i:i + 2]] += 1
        word_list = decoded_text.strip('\n').split(" ")
        word_amount = 0
        # Get the amount of words that are in the dictionary.
        for word in word_list:
            if word in WORDS:
                word_amount += 1
        score = len(word_list) - word_amount
        # Calculate the score.
        for letter in letter_appearances:
            if LETTERFREQ_dict[letter] != 0:
                score += abs(letter_appearances[letter] - LETTERFREQ_dict[letter])
        for pair in pair_appearances:
            if LETTERFREQ2_dict[pair] != 0:
                score += abs(pair_appearances[pair] - LETTERFREQ2_dict[pair])
        # Add the score to the scores list.
        if METHOD == 2:
            # If the method is 2, add the new mapping to the scores list. (Lamarckian)
            scores.append((score, new_mapping))
        else:
            # If the method is 0 or 1, add the old mapping to the scores list. (Darwinian)
            scores.append((score, mapping))
    # Sort the scores list by the score.
    sorted_population = sorted(scores, key=lambda x: x[0])
    return [m for _, m in sorted_population[:CARRY_POPULATION]], sorted_population[0][0]


def decrypt(cipher_text):
    population = [init_population() for _ in range(POPULATION_AMOUNT)]
    same_population = 0
    iterations = 0
    last_best_score = math.inf
    while same_population < STABILITY_INTERVALS:
        print("Last best score:", last_best_score)
        # Generate the new population with crossovers and mutations.
        population = generate_more_population(population)
        # Sort the population by fitness.
        population, best_score = fitness(cipher_text, population)
        iterations += 1
        if best_score < last_best_score:
            same_population = 0
            last_best_score = best_score
        else:
            same_population += 1
    with open('plain.txt', 'w') as f:
        f.write(decode_text(cipher_text, population[0]))
    with open('perm.txt', 'w') as f:
        f.write(str(population[0]))
    print(iterations)
    return population[0]


def check_accuracy(my_mapping):
    real_mapping = {'a': 'y', 'b': 'x', 'c': 'i', 'd': 'n', 'e': 't', 'f': 'o', 'g': 'z', 'h': 'j', 'i': 'c',
                    'j': 'e', 'k': 'b', 'l': 'l', 'm': 'd', 'n': 'u', 'o': 'k', 'p': 'm', 'q': 's', 'r': 'v',
                    's': 'p', 't': 'q', 'u': 'r', 'v': 'h', 'w': 'w', 'x': 'g', 'y': 'a', 'z': 'f'}
    missed_letters = 0
    for key in my_mapping:
        if my_mapping[key] != real_mapping[key]:
            missed_letters += 1
    print("Missed letters:", missed_letters)


if __name__ == "__main__":
    with open(CIPHERFILE, "r") as cipher_file:
        ciphertext = cipher_file.read().lower()
    amount_in_text(ciphertext)
    amount_in_text(ciphertext, option=2)
    with open(DICTFILE, "r") as dict_file:
        for line in dict_file:
            if line == "\n":
                break
            WORDS.append(line.rstrip('\n'))
    best_mapping = decrypt(ciphertext)
    check_accuracy(best_mapping)
