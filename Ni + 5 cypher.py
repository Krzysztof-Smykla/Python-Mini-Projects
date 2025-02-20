Alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']


def encrypt(mess):
    mess = mess.upper()
    words = mess.split()  # Split into words
    encrypted_words = []

    for word in words:
        encrypted_word = ""  # To store the encrypted word
        for i in range(len(word)):  # Ni is simply the position of each letter in the word
            letter = word[i]
            if letter in Alphabet:  # Only encrypt alphabet letters
                letter_index = Alphabet.index(letter)
                new_index = (letter_index + (i + 5)) % len(Alphabet)  # Circular shift
                encrypted_word += Alphabet[new_index]
            else:
                encrypted_word += letter  # Keep special characters unchanged

        encrypted_words.append(encrypted_word)

    return " ".join(encrypted_words)  # Join encrypted words back into a sentence


def decrypt(encrypted_mess):
    encrypted_mess = encrypted_mess.upper()
    words = encrypted_mess.split()  # Split into words
    decrypted_words = []

    for word in words:
        decrypted_word = ""  # To store the decrypted word
        for i in range(len(word)):  # Ni is simply the position of each letter in the word
            letter = word[i]
            if letter in Alphabet:  # Only decrypt alphabet letters
                letter_index = Alphabet.index(letter)
                new_index = (letter_index - (i + 5)) % len(Alphabet)  # Reverse shift
                decrypted_word += Alphabet[new_index]
            else:
                decrypted_word += letter  # Keep special characters unchanged

        decrypted_words.append(decrypted_word)

    return " ".join(decrypted_words)  # Join decrypted words back into a sentence


# Test encryption function
message = input("Enter message to encrypt: ")
encrypted_message = encrypt(message)
print("Encrypted message:", encrypted_message)

# Test decryption function
x = input("Input encrypted message: ")
print("Decrypted message:", decrypt(x))
