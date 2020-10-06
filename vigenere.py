# CS 585-01 Programming Assignment 1
# File: vigenere.py
# Author: Will Thomason
# Desc: This program accepts user input to encrypt or decrypt a message using a Vigenere cipher with the specified key.
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


def encode(plaintext, caesars):
    """This function takes in the plaintext and list of caesar cipher lengths
    in order to calculate the appropriate ciphertext."""

    ciphertext = ""  # Create a blank string to hold the ciphertext

    for i in range(len(plaintext)):  # For every character in the plaintext...
        current = ord(plaintext[i])  # ...get its ASCII value

        if 96 < current < 123:  # If it is a lowercase character...
            current += caesars[i]
            while current > 122:  # ...shift it and make sure it is still a valid letter
                current -= 26
        elif 64 < current < 91:  # Do the same for uppercase letters
            current += caesars[i]
            while current > 90:
                current -= 26
        else:
            caesars.insert(i, " ")  # Keep other characters (numbers, spaces, etc) from affecting the cipher

        ciphertext += chr(current)  # Add the new character to the ciphertext string

    return ciphertext  # Return the encrypted message


def decode(ciphertext, caesars):
    """This function takes in the ciphertext and list of caesar cipher lengths
    in order to calculate the appropriate plaintext."""

    plaintext = ""  # Create a blank string to hold the plaintext

    for i in range(len(ciphertext)):  # For every character in the ciphertext...
        current = ord(ciphertext[i])  # ...get its ASCII value

        if 96 < current < 123:  # If it is a lowercase character...
            current -= caesars[i]
            while current < 97:  # ...shift it and make sure it is still a valid letter
                current += 26
        elif 64 < current < 91:  # Do the same for uppercase letters
            current -= caesars[i]
            while current < 65:
                current += 26
        else:
            caesars.insert(i, " ")  # Keep other characters (numbers, spaces, etc) from affecting the cipher

        plaintext += chr(current)  # Add the new character to the plaintext string

    return plaintext  # Return the decrypted message


vigenere = tk.Tk()  # Create main window for program
vigenere.title("Vigenere Cipher")
vigenere.geometry("650x400")
vigenere.resizable(0, 0)

titleLabel = tk.Label(vigenere, text="Vigenere Cipher", font=("Castellar", 36), anchor="center")
titleLabel.place(x=90, y=90)

plainLabel = tk.Label(vigenere, text="Plaintext")
plainLabel.place(x=125, y=210)
plainBox = tk.Entry(vigenere)  # This entry box accepts plaintext from the user/displays decryption results
plainBox.place(x=50, y=235, width=200)

cipherLabel = tk.Label(vigenere, text="Ciphertext")
cipherLabel.place(x=475, y=210)
cipherBox = tk.Entry(vigenere)  # This entry box accepts ciphertext from the user/displays encryption results
cipherBox.place(x=400, y=235, width=200)

programMessage = tk.Label(vigenere, text="This program will  ")
programMessage.place(x=60, y=300)

modeSelect = ttk.Combobox(vigenere, values=["encrypt", "decrypt"])  # Combobox to allow user to switch modes
modeSelect.place(x=160, y=300, width=100)
modeSelect.current(0)

messageOptions = ["the plaintext ", "the ciphertext"]
keyLabel = " using the following key:"
modeDescription = tk.StringVar()  # Message describing the program's current mode
modeDescription.set(messageOptions[modeSelect.current()] + keyLabel)

keyBox = tk.Entry(vigenere)  # This entry box accepts the key from the user
keyBox.place(x=475, y=300, width=100)


def adjustMessage(event):
    """This function updates the program description message whenever the user changes between modes"""

    current = modeSelect.current()
    if current != -1:
        modeDescription.set(messageOptions[current] + keyLabel)


modeMessage = tk.Label(vigenere, textvariable=modeDescription)  # Displays the message concerning the current mode
modeMessage.place(x=263, y=300)
modeSelect.bind('<<ComboboxSelected>>', adjustMessage)


def runVigenere():
    """This function confirms that the user has entered valid input for encryption/decryption, generates the list of
    necessary Caesar shift values, and then calls the appropriate function to perform either encryption or decryption
    as specified by the user"""

    if modeSelect.get() == "encrypt":  # if encryption is desired

        cipherBox.delete(0, "end")  # clear the ciphertext box

        if len(keyBox.get()) is 0:  # check for key
            cipherBox.insert(0, "No key entered")
        elif len(plainBox.get()) is 0:  # check for plaintext to encrypt
            cipherBox.insert(0, "No plaintext entered")
        else:
            caesars = setCaesars(keyBox.get(), len(plainBox.get()))  # calculate Caesar shift values

            if len(caesars) is 0:  # say if invalid key is used
                cipherBox.insert(0, "Invalid key. Please use only letters.")
            else:  # otherwise display the encrypted text
                cipherBox.insert(0, encode(plainBox.get(), caesars))

    elif modeSelect.get() == "decrypt":  # if decryption is desired

        plainBox.delete(0, "end")  # clear the plaintext box

        if len(keyBox.get()) is 0:  # check for key
            plainBox.insert(0, "No key entered")
        elif len(cipherBox.get()) is 0:  # check for ciphertext to decrypt
            plainBox.insert(0, "No ciphertext entered")
        else:
            caesars = setCaesars(keyBox.get(), len(cipherBox.get()))  # calculate Caesar shift values

            if len(caesars) is 0:  # say if invalid key is used
                plainBox.insert(0, "Invalid key. Please use only letters.")
            else:  # otherwise display the decrypted text
                plainBox.insert(0, decode(cipherBox.get(), caesars))


engage = tk.Button(vigenere, text="Go!", command=runVigenere)  # Button used to trigger encryption/decryption
engage.place(x=300, y=350, width=50)


vigenere.mainloop()  # Execute main GUI loop
