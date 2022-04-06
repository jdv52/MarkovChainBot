#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Jayson De La Vega
# Created Date: 4/6/22
# version = '1.0'
# ---------------------------------------------------------------------------
""" Driver class for the Markov Chain Text Generator application """
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from Loader import Loader


def main():
    """
    Main function loop. Includes a menu interface for user to interact with
    the Loader class.
    """
    print("Welcome to Markov Chain Text Generator")
    print("Enter the desired order: ")
    order = int(input())
    print("Enter database file name:")
    file_name = input()
    print("Created new bot")

    l = Loader(order, file_name)
    user_input = ''

    while user_input != 'q':
        print("What would you like to do (enter q to quit)?\n" +
              "\t1. Train Bot\n" +
              "\t2. Display Frequency Table\n" +
              "\t3. Display Probability Table\n" +
              "\t4. Clear Data\n" +
              "\t5. Generate text")
        user_input = input()

        l.update_frequency_table()
        l.update_prob_table()

        if user_input == '1':
            print("Enter name of input file:")
            train_file = input()
            l.train(train_file)
            l.update_frequency_table()
            l.update_prob_table()
        elif user_input == '2':
            print("You chose to display the Frequency Table")
            l.display_frequency_table()
        elif user_input == '3':
            print("You chose to display the Probability Table")
            l.display_prob_table()
        elif user_input == '4':
            print("Cleared Markov database")
            l.clear_data()
        elif user_input == '5':
            txt = l.generate_text()
            print(txt)
        elif user_input != 'q':
            print("Invalid input, please try again")
    print("Goodbye!")


if __name__ == '__main__':
    main()
