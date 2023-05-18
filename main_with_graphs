import math
import random
from collections import Counter
import matplotlib.pyplot as plt

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

# Words in english.
WORDS = []

# List of best scores for each iteration.
BEST_SCORES = []

# List of average score for each iteration.
AVERAGE_SCORES = []

# List of best mapping error percentage.
BEST_ERROR_PERCENTAGE = []
NUMBER_OF_ITERATIONS_RUN = []
NUMBER_OF_CHECKS = 5

# The population amount for the genetic algorithm.
POPULATION_AMOUNT = 120

# The amount of top solutions to keep.
CARRY_POPULATION = 5

# The mutations amount for each iteration.
MUTATIONS = 1

# The crossovers amount for each iteration.
CROSSOVERS = 1

# The amount of intervals for which the best score has to be stable before aborting the genetic algorithm.
STABILITY_INTERVALS = 20

# The amount of letters in the cipher text.
LETTERS_AMOUNT = 0

# The amount of combinations in the cipher text.
COMBINATIONS_AMOUNT = 0


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


def mutate(cross):
    # Copy the solution.
    for i in range(MUTATIONS):
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
        new_cross1 = mutate(new_cross1)
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
    for mapping in population:
        letter_appearances = {}
        pair_appearances = {}
        decoded_text = decode_text(cipher_text, mapping)
        # delete all non-letters
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
        for word in word_list:
            if word in WORDS:
                word_amount += 1
        score = len(word_list) - word_amount
        for letter in letter_appearances:
            if LETTERFREQ_dict[letter] != 0:
                score += abs(letter_appearances[letter] - LETTERFREQ_dict[letter])
        for pair in pair_appearances:
            if LETTERFREQ2_dict[pair] != 0:
                score += abs(pair_appearances[pair] - LETTERFREQ2_dict[pair])
        scores.append((score, mapping))
    sorted_population = sorted(scores, key=lambda x: x[0])
    total_score = sum(score for score, _ in scores)
    average_score = total_score / len(scores)
    AVERAGE_SCORES.append(average_score)
    return [m for _, m in sorted_population[:CARRY_POPULATION]], sorted_population[0][0]


def decrypt(cipher_text):
    population = [init_population() for _ in range(POPULATION_AMOUNT)]
    same_population = 0
    iterations = 0
    last_best_score = math.inf
    while same_population < STABILITY_INTERVALS:
        # print("Last best score:", last_best_score)
        BEST_SCORES.append(last_best_score)
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
    # with open('plain.txt', 'w') as f:
    #     f.write(decode_text(cipher_text, population[0]))
    # with open('perm.txt', 'w') as f:
    #     f.write(str(population[0]))
    # print(iterations)
    # draw_plot(iterations)
    return population[0], iterations


def draw_plot(iterations):
    iters = list(range(1, iterations + 1))
    plt.plot(iters, AVERAGE_SCORES, label="Average Score")
    plt.plot(iters, BEST_SCORES, label="Best Score")
    plt.xlabel('Iteration')
    plt.ylabel('Score')
    plt.title('Fitness Progress')
    plt.legend()
    plt.show()


def check_accuracy(my_mapping):
    real_mapping = {'a': 'y', 'b': 'x', 'c': 'i', 'd': 'n', 'e': 't', 'f': 'o', 'g': 'z', 'h': 'j', 'i': 'c',
                    'j': 'e', 'k': 'b', 'l': 'l', 'm': 'd', 'n': 'u', 'o': 'k', 'p': 'm', 'q': 's', 'r': 'v',
                    's': 'p', 't': 'q', 'u': 'r', 'v': 'h', 'w': 'w', 'x': 'g', 'y': 'a', 'z': 'f'}
    missed_letters = 0
    for key in my_mapping:
        if my_mapping[key] != real_mapping[key]:
            missed_letters += 1
    percentage_missed_letters = (missed_letters / len(CHARS) * 100)
    return percentage_missed_letters


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
    # for p in POPULATION_SIZES:
        # POPULATION_AMOUNT = p
    for i in range(1, NUMBER_OF_CHECKS):
        best_mapping, iterations = decrypt(ciphertext)
        percentage = check_accuracy(best_mapping)
        BEST_ERROR_PERCENTAGE.append(percentage)
        NUMBER_OF_ITERATIONS_RUN.append(iterations)
        print(f"finished run number {i}")
    average_error = sum(i for i in BEST_ERROR_PERCENTAGE) / len(BEST_ERROR_PERCENTAGE)
    average_iterations = sum(j for j in NUMBER_OF_ITERATIONS_RUN) / len(NUMBER_OF_ITERATIONS_RUN)
    print(f"population size: {POPULATION_AMOUNT}, average error %: {average_error}, average iterations: {average_iterations}\n\n")

