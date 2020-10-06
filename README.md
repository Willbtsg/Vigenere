# Vigenere
This readme and the described programs were written by Will Thomason for Dr. Feng Zhu's CS 585-01 course in Fall 2020.

Both programs were written in Python and later converted into executables using Nuitka.

Vigenere- This program encrypts and decrypts messages using the Vigenere cipher. Users may input a key to use and choose
whether they wish to encrypt or decrypt a message. This may done as many times as desired until closing the program.

Vigenere Cracker- This programs accepts input in the form of ciphertext that has been encrypted using a Vigenere cipher with
a key length of 3 (as specified by assignment). When analyzing the ciphertext, the program determines the most likely Caesar key for each third of the
ciphertext. It then attempts decryption using the most likely key before displaying the options in order of likelihood to allow
the user to attempt decryption if the most likely answer was incorrect. Users may make as many guesses as they like, or change
the message that they wish to attempt to decrypt.
