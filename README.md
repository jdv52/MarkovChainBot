# MarkovChainBot

This project is a Python application that uses Markov chains to generate sentences based on an input text file.

The application allows users to "train" the algorithm with the input text file, and the algorithm saves a database of words in a .csv file.

I built this project the summer after my senior year of high school to familiarize myself with Python. Originally I planned this project as a component of a larger application that was going to be a fully-fledged chatbot that took advantage of speech-to-text and text-to-speech to allow a user to actually speak to the bot through a microphone and hear a response. This larger project is currently on hold, but I hope to continue work on it in the near future.

# Project Status

Project is currently inactive. The algorithm is currently able to generate sentences, but sentences aren't fully coherent and the output requires some cleanup.

# Instructions

Clone this repository and run MarkovV2Driver.py

Input the order of the Markov chain when prompted.

Input the name of the database file you want to create (must be in .csv format! FOR EXAMPLE: db.csv).

A menu will appear giving you the option to:  
1. Train the bot
2. Display the Frequency Table
3. Display the Probability Table
4. Clear the database file
5. Generate a sentence

The database file is currently empty, so the program won't generate any sentences. You need to first train the algorithm using an input text. You can load multiple input texts into the same database file.

After populating the database file you can then begin to generate sentences.

If you want to erase all the data currently in the database file, you can choose to clear the database file.

When you want to exit enter 'q'.

# TODOs

The biggest issue with this application is coherence and output formatting. Generated sentences aren't always coherent, and sentences have extra spaces between punctuation. The program also uses a large amount of memory especially when multiple large texts are used to train the algorithm, which limits the size of the database. Therefore, I need to explore options to allow the program to keep a larger database.
