import csv
import copy
import numpy as np
from random import choice


class Loader:

    def __init__(self, order, data_base):
        self.__order = order
        self.__data_base_path = data_base
        open(data_base, 'w')
        self.__frequency_table = {}
        self.__prob_table = {}

    def get_frequency_table(self):
        return self.__frequency_table

    def get_prob_table(self):
        return self.__prob_table

    def get_db_path(self):
        return self.__data_base_path

    def train(self, input):
        # Open input file and split by the text into an array by spaces
        f = open(input, 'r')
        arr = self.clean(f.read()).split()
        f.close()

        # Begin creating frequency table
        T = {}
        for i in range(len(arr) - self.__order):
            gram = ' '.join(arr[i:i + self.__order])
            next_gram = arr[i + self.__order]
            if gram not in T:
                T[gram] = {}
                T[gram][next_gram] = 1
            elif next_gram not in T[gram]:
                T[gram][next_gram] = 1
            else:
                T[gram][next_gram] += 1

        # Merge new frequency table with existing data
        with open(self.__data_base_path, 'r') as dbfile:
            reader = csv.reader(dbfile, delimiter='\t')
            for row in reader:
                gram_header = row[0]
                next_gram = row[1]
                val = int(row[2])

                if gram_header not in T:
                    T[gram_header] = {}
                    T[gram_header][next_gram] = val
                elif next_gram not in T[gram_header]:
                    T[gram_header][next_gram] = val
                else:
                    T[gram_header][next_gram] += val

        # print(T)

        # Update the database file to include the new data
        with open(self.__data_base_path, 'w', newline='') as dbfile:
            writer = csv.writer(dbfile, delimiter='\t')
            for gram in T:
                next_grams = T[gram]
                for item in next_grams:
                    writer.writerow([gram, item, next_grams[item]])

    def clean(self, text):
        text = text.replace('.', ' .')
        text = text.replace(',', ' ,')
        text = text.replace(';', ' ;')
        text = text.replace('"', ' "')
        text = text.replace('  ', ' ')

        return text

    # Method to clear the Markov database
    def clear_data(self):
        f = open(self.__data_base_path, 'w+')
        f.close()

    # Method to retrieve data from Markov data base and load into frequency table
    def update_frequency_table(self):
        T = {}
        with open(self.__data_base_path, 'r') as dbfile:
            reader = csv.reader(dbfile, delimiter='\t')
            for row in reader:
                gram_header = row[0]
                next_gram = row[1]
                val = int(row[2])

                if gram_header not in T:
                    T[gram_header] = {}
                    T[gram_header][next_gram] = val
                else:
                    T[gram_header][next_gram] = val

        self.__frequency_table = T

    # Method to create probability table based on frequency table
    def update_prob_table(self):
        T = copy.deepcopy(self.__frequency_table)
        for kx in T:
            s = float(sum(T[kx].values()))
            for k in T[kx].keys():
                T[kx][k] = T[kx][k] / s
        self.__prob_table = T

    # Method to display frequency table
    def display_frequency_table(self):
        self.__display_nested_dict(self.__frequency_table)

    # Method to display probability table
    def display_prob_table(self):
        self.__display_nested_dict(self.__prob_table)

    # Helper method for display methods
    def __display_nested_dict(self, d):
        for i in d:
            print(i)
            for j in d[i]:
                print('\t' + j + ': ' + str(d[i][j]))

    # Helper method for text generation
    def markov(self, ctx):
        if ctx not in self.__prob_table:
            return ' '
        possible_chars = list(self.__prob_table[ctx].keys())
        possible_vals = list(self.__prob_table[ctx].values())
        return np.random.choice(possible_chars, p=possible_vals)

    # Method to generate text
    def generate_text(self):
        # Should input text be recycled into Markov data base?
        sentence = choice(list(self.__prob_table)).split(" ")
        ctx = " ".join(sentence[-self.__order:])
        next_prediction = self.markov(ctx)

        while next_prediction != '.':
            sentence.append(next_prediction)
            ctx = " ".join(sentence[-self.__order:])
            next_prediction = self.markov(ctx)
        sentence.append(next_prediction)
        return " ".join(sentence)
