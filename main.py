import random
from collections import Counter

# The cipher file.
CIPHERFILE = "enc.txt"

# The dictionary file.
DICTFILE = "dict.txt"

# The alphabet.
CHARS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
         'u', 'v', 'w', 'x', 'y', 'z']

# The frequency of letter.
LETTERFREQ_dict = {}

# The frequency of combinations.
LETTERFREQ2_dict = {}

# Word in english.
WORDS = []

# The population amount for the genetic algorithm.
POPULATION_AMOUNT = 120

# The amount of top solutions to keep.
CARRY_POPULATION = 20

# The mutations amount for each iteration.
MUTATIONS = 1

# The tournament size for the genetic algorithm.
TOURNAMENT_SIZE = 30

# The factor for the score of the words.
WORD_FACTOR = 2

# The factor for the score of the letters.
LETTER_FACTOR = 3

# The factor for the score of the combinations.
COMBINATION_FACTOR = 4

# The amount of intervals for which the best score has to be stable before aborting the genetic algorithm.
STABILITY_INTERVALS = 25

# The amount of letters in the cipher text.
LETTERS_AMOUNT = 0

# The amount of combinations in the cipher text.
COMBINATIONS_AMOUNT = 0

# The amount of changes in the mapping.
CHANGES_AMOUNT = 3


def amount_in_text(cipher_text, option=1):
    # Get the amount of abc characters.
    amount = 0
    if option == 1:
        # Get the amount of abc characters.
        global LETTERS_AMOUNT
        LETTERS_AMOUNT = len("".join([char for char in cipher_text if char.isalpha()]))
        # Set the right file name and dict.
        file_name = "Letter_Freq.txt"
        file_dict = LETTERFREQ_dict
    else:
        # Get the amount of ab combinations.
        global COMBINATIONS_AMOUNT
        for i in range(len(cipher_text) - 1):
            if cipher_text[i].isalpha() and cipher_text[i + 1].isalpha():
                COMBINATIONS_AMOUNT += 1
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
            file_dict[letter] = freq


def init_population():
    # A set for all the characters.
    values = set(CHARS)
    mapping = {}
    for char in CHARS:
        # Get a random value from the values set.
        value = random.choice(list(values))
        # Add the key-value pair to the mapping.
        mapping[char] = value
        # Remove the value from the values set.
        values.remove(value)
    return mapping


def crossover(parent1, parent2):
    size = len(parent1)
    # Choose crossover points
    point1, point2 = sorted(random.sample(range(size), 2))

    # Convert parents to lists to allow index operations
    keys = list(parent1.keys())
    parent1_values = list(parent1.values())
    parent2_values = list(parent2.values())

    # Create child
    child_values = parent1_values.copy()

    # For each position in the selected segment from parent2
    for i in range(point1, point2):
        if parent2_values[i] not in parent1_values[point1:point2]:
            # If the value from parent2 is not in the selected segment from parent1, swap it
            index_in_child = parent1_values.index(parent2_values[i])
            child_values[i], child_values[index_in_child] = child_values[index_in_child], child_values[i]

    # Create new mapping
    child_mapping = dict(zip(keys, child_values))

    return child_mapping


def mutate(cross, value):
    # Copy the solution.
    for i in range(value):
        # Get a random key from the solution.
        key1, key2 = random.sample(CHARS, 2)
        # Swap the values of the key in the solution.
        cross[key1], cross[key2] = cross[key2], cross[key1]
    return cross


def tournament_selection(scores):
    # Randomly select `tournament_size` individuals from the population
    tournament = random.sample(scores, TOURNAMENT_SIZE)

    # Return the best individual from the tournament
    return max(tournament, key=lambda x: x[0])[1]


def generate_more_population(scores):
    # Copy the population.
    new_population = []
    sorted_scores = sorted(scores, key=lambda x: x[0], reverse=True)
    for i in range(CARRY_POPULATION):
        new_population.append(sorted_scores[i][1])
    while len(new_population) < POPULATION_AMOUNT:
        # Get two random solutions from the population.
        parent1 = tournament_selection(scores)
        parent2 = tournament_selection(scores)
        # Copy the first solution to the next iteration and cross it with the second solution.
        child = crossover(parent1, parent2)
        # Mutate the first solution.
        child = mutate(child, MUTATIONS)
        new_population.append(child)
    return new_population, sorted_scores[0][0]


def decode_text(cipher_text, mapping):
    i = 0
    decoded_text = [''] * len(cipher_text)
    for char in cipher_text:
        if char.isalpha():
            decoded_text[i] += mapping[char]
        else:
            decoded_text[i] += char
        i += 1
    return ''.join(decoded_text)


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
        counting = Counter(decoded_text)
        # Get the frequency of each letter.
        for letter in CHARS:
            if letter.isalpha():
                letter_appearances[letter] = counting[letter] / LETTERS_AMOUNT
        # Get the frequency of each pair.
        for i in range(len(decoded_text) - 1):
            if decoded_text[i].isalpha() and decoded_text[i + 1].isalpha():
                if decoded_text[i:i + 2] not in pair_appearances:
                    pair_appearances[decoded_text[i:i + 2]] = 0
                pair_appearances[decoded_text[i:i + 2]] += 1 / COMBINATIONS_AMOUNT
        word_list = decoded_text.strip('\n').split(" ")
        # Get the amount of words that are in the dictionary.
        score = WORD_FACTOR * sum(word in WORDS for word in word_list) / len(word_list)
        # Get the absolute difference between the frequencies of the decoded text and the frequencies of the
        # English language letters.
        for letter in letter_appearances:
            score += LETTER_FACTOR * (1 - abs(letter_appearances[letter] - LETTERFREQ_dict[letter]))
        # Get the absolute difference between the frequencies of the decoded text and the frequencies of the
        # English language pairs.
        for pair in pair_appearances:
            if LETTERFREQ2_dict[pair] != 0:
                score += COMBINATION_FACTOR * (1 - abs(pair_appearances[pair] - LETTERFREQ2_dict[pair]))
        # Add the score to the scores list.
        if METHOD == 2:
            # If the method is 2, add the new mapping to the scores list. (Lamarckian)
            scores.append((score, new_mapping))
        else:
            # If the method is 0 or 1, add the old mapping to the scores list. (Darwinian)
            scores.append((score, mapping))
    # Sort the scores list by the score.
    return scores


def decrypt(cipher_text):
    population = [init_population() for _ in range(POPULATION_AMOUNT)]
    same_population = 0
    iterations = 0
    last_best_score = 0
    while same_population < STABILITY_INTERVALS:
        # Sort the population by fitness.
        population = fitness(cipher_text, population)
        # Generate the new population with crossovers and mutations.
        population, best_score = generate_more_population(population)
        iterations += 1
        if best_score > last_best_score:
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


if __name__ == "__main__":
    METHOD = input("What method do you want to use? (0 - Classic, 1 - Darwinian, 2 - Lamarckian)\n")
    while METHOD > 2 or METHOD < 0:
        METHOD = input("Please enter a valid method.\n")
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
