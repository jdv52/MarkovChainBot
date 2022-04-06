#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Jayson De La Vega
# Created Date: 4/6/22
# version = '1.0'
# ---------------------------------------------------------------------------
""" Loader class that handles database and input text reading/processing """
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import csv
import copy
import numpy as np
from random import choice


class Loader:
    """
    Loader class that handles reading and processing of Markov chain database
    and input training text files.

    Uses concept of Markov chains to train the Loader with training texts.
    The Loader samples groups of words (the size of the group is dictated
    by the order attribute) and generates frequency and probability tables
    that describe how often a specific word will follow a certain grouping
    of words.
    The Loader stores its training data in a designated .csv file database.
    The Loader accesses this database to update a probability/frequency
    table, which it can utilize to generate random sentences.

    Attributes
    ----------
    __order : int
        The number of words that the Loader samples per group of words.
    __data_base_path : str
        The path of the database file that stores the frequency table.
    __frequency_table : dict
        Dictionary that stores how often a specific word appears after
        a certain grouping of words.
    __prob-table : dict
        Dictionary that stores the probability that a specific word
        appears after a certain grouping of words.

    Methods
    -------
    get_frequency_table()
        Returns this loader's frequency table
    get_prob_table()
        Returns this loader's probability table
    get_db_path()
        Returns this loader's database path
    train(input)
        Function to train loader and populate database file based on input from
        a specified training text.
    clean(text)
        Function to clean and reformat the input text
    clear_data()
        Function to empty the database file
    update_frequency_table()
        Function to load frequency table with data from the database file
    update_prob_table()
        Function to load probability table with data from the database file
    display_frequency_table()
        Function to display frequency table
    display_prob_table()
        Function to display probability table
    __display_nested_dict(d)
        Helper function to display nested dictionaries
    markov(ctx)
        Helper function for text-generation
    generate_text()
        Function to generate sentences
    """

    def __init__(self, order, data_base):
        """
        Constructs a Loader object and creates a database file

        Parameters
        ----------
        order : int
            The number of words the Loader samples from training texts
        data_base : str
            The path of the database file
        """
        self.__order = order
        self.__data_base_path = data_base
        open(data_base, 'w')
        self.__frequency_table = {}
        self.__prob_table = {}

    def get_frequency_table(self):
        """
        Getter function to return this Loader's frequency table (for
        debugging purposes)

        Returns
        -------
        dict
            This Loader's frequency table.
        """
        return self.__frequency_table

    def get_prob_table(self):
        """
        Getter function to return this Loader's probability table (for
        debugging purposes)

        Returns
        -------
        dict
            This Loader's probability table.
        """
        return self.__prob_table

    def get_db_path(self):
        """
        Getter function to return the database file path

        Returns
        -------
        str
            This database file's path.
        """
        return self.__data_base_path

    def train(self, input):
        """
        Function to train the Loader's database

        The function samples words from the input text file in groups of size
        order. This function then generates a frequency table and populates (or
        merges if there's existing data) the database file with frequency table
        information.

        Parameters
        ----------
        input : str
            Name of the training text file
        """
        # Open input file and split by the text into an array by spaces
        f = open(input, 'r')
        arr = self.clean(f.read()).split()
        f.close()

        # Begin populating frequency table by sampling words in groups of
        # size order, AKA 'engrams'
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

        # Merge new frequency table with existing frequency table
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

        # Update the database file to include the new data
        with open(self.__data_base_path, 'w', newline='') as dbfile:
            writer = csv.writer(dbfile, delimiter='\t')
            for gram in T:
                next_grams = T[gram]
                for item in next_grams:
                    writer.writerow([gram, item, next_grams[item]])

    def clean(self, text):
        """
        Method to clean and format the punctuation of the input text

        Parameters
        ----------
        text : str
            The text of the input file
        Returns
        ----------
        str
            The cleaned text
        """
        text = text.replace('.', ' .')
        text = text.replace(',', ' ,')
        text = text.replace(';', ' ;')
        text = text.replace('"', ' "')
        text = text.replace('  ', ' ')
        return text

    def clear_data(self):
        """
        Method to empty the database file
        """
        f = open(self.__data_base_path, 'w+')
        f.close()

    def update_frequency_table(self):
        """
        Method to retrieve the frequency table from the database file and update
        the frequency table.
        """
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

    def update_prob_table(self):
        """
        Method to recalculate the probability table from the frequency table.
        """
        T = copy.deepcopy(self.__frequency_table)
        for kx in T:
            s = float(sum(T[kx].values()))
            for k in T[kx].keys():
                T[kx][k] = T[kx][k] / s
        self.__prob_table = T

    def display_frequency_table(self):
        """
        Method to display the frequency table (for debugging)
        """
        self.__display_nested_dict(self.__frequency_table)

    def display_prob_table(self):
        """
        Method to display the probability table (for debugging)
        """
        self.__display_nested_dict(self.__prob_table)

    def __display_nested_dict(self, d):
        """
        Helper method to display nested dictionaries in a consistent format

        Parameters
        ----------
        d : dict
            The dictionary to be displayed
        """
        for i in d:
            print(i)
            for j in d[i]:
                print('\t' + j + ': ' + str(d[i][j]))

    def markov(self, ctx):
        """
        Helper method for text generation.

        Produces a random word from the probability table that follows the word
        combination given by the ctx parameter. Each word is given a weight based
        on its probability table value.

        Parameters
        ----------
        ctx : str
            The current engram (usually the engram at the end of the current sentence).
        Returns
        -------
        str
            A random word that is likely to follow the engram contained in ctx.
        """
        if ctx not in self.__prob_table:
            return ' '
        possible_chars = list(self.__prob_table[ctx].keys())
        possible_vals = list(self.__prob_table[ctx].values())
        return np.random.choice(possible_chars, p=possible_vals)

    def generate_text(self):
        """
        Method to generate random text.

        The method begins by selecting a random engram from the probability table and
        predicts a word that is likely to follow this engram. The method loops, predicting
        the next possible word until it predicts that the next 'word' is a period. The method
        then returns the sentence.

        Returns
        -------
        str
            The generated text
        """
        sentence = choice(list(self.__prob_table)).split(" ")
        ctx = " ".join(sentence[-self.__order:])
        next_prediction = self.markov(ctx)

        while next_prediction != '.':
            sentence.append(next_prediction)
            ctx = " ".join(sentence[-self.__order:])
            next_prediction = self.markov(ctx)
        sentence.append(next_prediction)
        return " ".join(sentence)
