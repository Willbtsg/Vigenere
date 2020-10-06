# CS 585-01 Programming Assignment 1
# File: vigenereCracker.py
# Author: Will Thomason
# Desc: This program accepts encrypted ciphertexts and works with the user to discover the plaintext. It does so by
# analyzing the letter occurrences in each third of the ciphertext
# Date: 9/23/2020

import tkinter as tk
from tkinter import ttk


def setCaesars(key, messageLength):
    """This function takes the user submitted key and message. The key is used to generate the lengths of the
    necessary Caesar ciphers, and the message is used to make the key long enough (rather than performing the modulo
    operation during encryption/decryption to determine the appropriate Caesar key. This list is used in lieu of a
    tableau in this program."""

    caesars = []  # Create a list to hold Caesar cipher lengths

    key = key.lower()  # convert key to uniform case for simplicity

    for i in range(len(key)):  # Calculate the appropriate Caesar shift length for each key character...
        current = ord(key[i])  # Get ASCII value of current character...

        if not 96 < current < 123:  # ...if character is not a lowercase letter...
            return []  # ...return an empty list to indicate invalid input
        else:
            caesars.append(ord(key[i]) - 97)  # ...otherwise convert that letter to an offset and append it to the list

    while len(caesars) < messageLength:  # If the key is shorter than the plaintext...
        caesars.extend(caesars)  # ...repeat the key (i.e. list Caesar lengths) until it is long enough

    return caesars  # return calculated Caesar shift values


def decode(ciphertext, caesars):
    """This function takes in the ciphertext and list of caesar cipher lengths
    in order to calculate the appropriate plaintext."""

    plaintext = ""  # Create a blank string to hold the plaintext

    for i in range(len(ciphertext)):  # For every character in the ciphertext...
        current = ord(ciphertext[i])  # ...get its ASCII value

        if 96 < current < 123:  # If it is a lowercase character...
            current -= caesars[i]
            if current < 97:  # ...shift it and make sure it is still a valid letter
                current += 26
        elif 64 < current < 91:  # Do the same for uppercase letters
            current -= caesars[i]
            if current < 65:
                current += 26
        else:
            caesars.insert(i, " ")  # Keep other characters (numbers, spaces, etc) from affecting the cipher

        plaintext += chr(current)  # Add the new character to the plaintext string

    return plaintext  # Return the decrypted message


cracker = tk.Tk()  # Create main window for program
cracker.title("Vigenere / Cracked")
cracker.geometry("650x400")
cracker.resizable(0, 0)

titleLabel = tk.Label(cracker, text="Vigenere / Cracked", font=("Castellar", 36), anchor="center")
titleLabel.place(x=35, y=70)

cipherLabel = tk.Label(cracker, text="Ciphertext")
cipherLabel.place(x=125, y=175)
cipherBox = tk.Entry(cracker)  # This entry box accepts ciphertext from the user/displays encryption results
cipherBox.place(x=50, y=200, width=200)

firstLabel = tk.Label(cracker, text="First Shift")
firstLabel.place(x=192, y=250)
firstShift = ttk.Combobox(cracker)  # combobox used to change first letter of key
firstShift.place(x=200, y=275, width=40)

secondLabel = tk.Label(cracker, text="Second Shift")
secondLabel.place(x=287, y=250)
secondShift = ttk.Combobox(cracker)  # combobox used to change second letter of key
secondShift.place(x=305, y=275, width=40)

thirdLabel = tk.Label(cracker, text="Third Shift")
thirdLabel.place(x=400, y=250)
thirdShift = ttk.Combobox(cracker)  # combobox used to change third letter of key
thirdShift.place(x=410, y=275, width=40)

comboList = [firstShift, secondShift, thirdShift]  # list of comboboxes used to display tentative key

keyLabel = tk.Label(cracker, text="Key")
keyLabel.place(x=310, y=175)
keyBox = tk.Entry(cracker)  # displays current key guess
keyBox.place(x=300, y=200, width=50)

plainLabel = tk.Label(cracker, text="Plaintext")
plainLabel.place(x=475, y=175)
plainBox = tk.Entry(cracker)  # This entry box accepts plaintext from the user/displays decryption results
plainBox.place(x=400, y=200, width=200)


def analyzeVigenere():
    """This function analyzes the ciphertext to determine teh most likely letters that were used to shift each
    third of the original plaintext. It does this using the Caesar cipher statistical analysis method detailed
    on pages 293 and 294 of "Computer Security: Art and Science" by Matt Bishop (2nd Edition)"""

    frequencyList = [0.07984, 0.01511, 0.02504, 0.0426, 0.12452, 0.02262, 0.02013, 0.06384, 0.07, 0.00131, 0.00741,
                          0.03961, 0.02629, 0.06876, 0.07691, 0.01741, 0.00107, 0.05912, 0.06333, 0.09058, 0.02844,
                          0.01056, 0.02304, 0.00159, 0.02028, 0.00057]  # list of letter frequencies in English

    ciphertext = cipherBox.get()  # retrieve current ciphertext
    alphabetCounts = [[0 for j in range(26)] for i in range(3)]  # holds letter counts for each third of the ciphertext
    alphaSwitch = 0  # indicates which alphabetCounts list a letter belongs in
    shiftOdds = [{} for i in range(3)]  # stores likelihood of shift values for each third of ciphertext

    for i in range(len(ciphertext)):  # for every character in the ciphertext...

        current = ciphertext[i].lower()  # ...copy the current character...

        if 96 < ord(current) < 123:  # ...if that character is a letter...
            alphabetCounts[alphaSwitch][ord(current) - 97] += 1  # ...increase number of occurrences in the alphabet...
            alphaSwitch += 1  # ...then move to the next alphabet in the rotation
            alphaSwitch %= 3  # alphabets are numbered 0 through 2

    for i in range(len(alphabetCounts)):  # for each third of the ciphertext...
        length = sum(alphabetCounts[i])  # ...get the total number of letters...
        for shift in range(26):  # ...then for each possible shift value...
            likelihood = 0  # set initial likelihood to zero...
            for j in range(len(alphabetCounts[i])):  # then for each letter in the alphabet...
                letterCount = alphabetCounts[i][j]
                if letterCount > 0:  # ...if that letter appeared in this third of the ciphertext...
                    likelihood += letterCount/length*frequencyList[(j-shift) % 26]  # ...use it in the summation

            shiftOdds[i][chr(65+shift)] = likelihood  # add each shift to the dictionary with its likelihood

    key = ""  # variable to hold decryption key

    for i in range(len(shiftOdds)):  # for each third of the ciphertext...

        # ...sort the dictionary by likelihood values in descending order...
        currentShift = {letter: likelihood for letter, likelihood in sorted(shiftOdds[i].items(),
                                                                            key=lambda item: item[1], reverse=True)}

        comboList[i]['values'] = list(currentShift)  # ...display the sorted keys (i.e. letters) in a combobox...
        comboList[i].current(0)  # ...set the combobox to the most likely value...
        key += list(currentShift)[0]  # ...and add the most likely letter to the key

    keyBox.delete(0, "end")  # clear the key box
    keyBox.insert(0, key)  # display the tentative key
    plainBox.delete(0, "end")  # clear the plaintext box
    plainBox.insert(0, decode(ciphertext, setCaesars(key, len(ciphertext))))  # calculate and display the plaintext


analyze = tk.Button(cracker, text="Analyze!", command=analyzeVigenere)  # Button used to trigger alphabet analysis
analyze.place(x=240, y=330, width=60)


def testVigenere():
    """This function allows the user to test a new decryption key via the comboboxes"""

    key = firstShift.get() + secondShift.get() + thirdShift.get()  # get the new key from the comboboxes

    keyBox.delete(0, "end")  # clear the key box
    keyBox.insert(0, key)  # copy the new key to the entry box
    plainBox.delete(0, "end")  # clear the plaintext box
    plainBox.insert(0, decode(cipherBox.get(), setCaesars(key, len(cipherBox.get()))))  # calculate the new plaintext


test = tk.Button(cracker, text="Test!", command=testVigenere)  # button to test user-selected shift combinations
test.place(x=350, y=330, width=60)


cracker.mainloop()  # execute main GUI loop
