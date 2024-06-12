import random
import numpy as np
import matplotlib.pyplot as plt
from bitarray import bitarray
import time

###################################################################################################

def generate_signal(length, min_run_length, max_run_length):

    signal = []
    while len(signal) < length:
        random_length = random.randint(min_run_length, max_run_length)
        random_bit = random.choice([0, 1])
        signal.extend([random_bit] * random_length)
    return signal[:length]

###################################################################################################

def save_signal_to_file(signal, filename):

    with open(filename, 'w') as file:
        for bit in signal:              #signal nazwa listy
            file.write(str(bit))

###################################################################################################

def calculate_desynchronization_probability(signal_proabability):
    desynchronized_bits = 0
    desynchronization_flag = False
    probability = 0
    desynchronizations = 0
    previous_bit = signal_proabability[0]

    for bit in signal_proabability[1:]:
        if bit == previous_bit:
            if desynchronization_flag == True:
                desynchronized_bits += 1
            else:
                probability += 1
                random_value = random.randint(1, 100)
                if random_value <= probability:
                    desynchronizations += 1
                    desynchronized_bits += 1
                    desynchronization_flag = True
                    probability=0
        else:
            desynchronization_flag = False
            probability = 0

        previous_bit = bit
    print("liczba rozsychnronizowanych bitów to:",desynchronized_bits)
    return desynchronizations

###################################################################################################

def xor_scramble(data, key):

    scrambled_data = []
    for i in range(len(data)):
        scrambled_byte = data[i] ^ key[i % len(key)]
        scrambled_data.append(scrambled_byte)
    return scrambled_data

###################################################################################################

def xor_descramble(scrambled_data, key):
    descrambled_data= xor_scramble(scrambled_data, key)
    return descrambled_data

###################################################################################################

def mul_scrambler_w1(data, scramble_key):
    key = scramble_key[:]
    scrambled_data = bytearray()
    for i in range(len(data)):
        byteX = data[i]
        byte_from_key = key[18] ^ key[23]
        scrambled_byte = byteX ^ byte_from_key
        j = len(key)-1
        while j >= 0:
            key[j] = key[j-1]
            j -= 1
        key[0] = scrambled_byte
        scrambled_data.append(scrambled_byte)
    return scrambled_data

def mul_descrambler_w1(data, descramble_key):
    key = descramble_key[:]
    descrambled_data = bytearray()
    for i in range(len(data)):
        byteX = data[i]
        byte_from_key = key[18] ^ key[23]
        descrambled_byte = byteX ^ byte_from_key
        j = len(key) - 1
        while j >= 0:
            key[j] = key[j - 1]
            j -= 1
        key[0] = byteX
        descrambled_data.append(descrambled_byte)
    return descrambled_data

###################################################################################################

def mul_scrambler_w2(data, scramble_key):
    key = scramble_key[:]
    scrambled_data = bytearray()
    for i in range(len(data)):
        byteX = data[i]
        byte_from_key = key[4] ^ key[15]
        scrambled_byte = byteX ^ byte_from_key
        j = len(key)-1
        while j >= 0:
            key[j] = key[j-1]
            j -= 1
        key[0] = scrambled_byte
        scrambled_data.append(scrambled_byte)
    return scrambled_data

def mul_descrambler_w2(data, descramble_key):
    key = descramble_key[:]
    descrambled_data = bytearray()
    for i in range(len(data)):
        byteX = data[i]
        byte_from_key = key[4] ^ key[15]
        descrambled_byte = byteX ^ byte_from_key
        j = len(key) - 1
        while j >= 0:
            key[j] = key[j - 1]
            j -= 1
        key[0] = byteX
        descrambled_data.append(descrambled_byte)
    return descrambled_data

###################################################################################################

def mul_scrambler_w3(data, scramble_key):
    key = scramble_key[:]
    scrambled_data = bytearray()
    for i in range(len(data)):
        byteX = data[i]
        byte_from_key = key[4] ^ key[12] ^ key[17]
        scrambled_byte = byteX ^ byte_from_key
        j = len(key)-1
        while j >= 0:
            key[j] = key[j-1]
            j -= 1
        key[0] = scrambled_byte
        scrambled_data.append(scrambled_byte)
    return scrambled_data

def mul_descrambler_w3(data, descramble_key):
    key = descramble_key[:]
    descrambled_data = bytearray()
    for i in range(len(data)):
        byteX = data[i]
        byte_from_key = key[4] ^ key[12] ^ key[17]
        descrambled_byte = byteX ^ byte_from_key
        j = len(key) - 1
        while j >= 0:
            key[j] = key[j - 1]
            j -= 1
        key[0] = byteX
        descrambled_data.append(descrambled_byte)
    return descrambled_data

###################################################################################################

def count_sequence_lengths(data):
    sequence_lengths = []
    current_length = 0
    current_bit = None

    for bit in data:
        if bit == current_bit:
            current_length += 1
        else:
            if current_length >= 2:
                sequence_lengths.append(current_length)
            current_length = 1
            current_bit = bit

    if current_length >= 2:
        sequence_lengths.append(current_length)

    return sequence_lengths

###################################################################################################

def plot_histogram(sequence_lengths):
    plt.hist(sequence_lengths, bins=np.arange(2, max(sequence_lengths) + 2), align='left', rwidth=0.8)
    plt.xlabel('Długość sekwencji')
    plt.ylabel('Ilość wystąpień')
    plt.title('Histogram ilości sekwencji dla danej długości sekwencji')
    plt.grid(True)
    plt.show()

###################################################################################################

def binary_iteration(length):
    results = []

    def generate_binary_combinations(n):
        if n == 0:
            return [[]]
        smaller_combinations = generate_binary_combinations(n - 1)
        return [[0] + combination for combination in smaller_combinations] + [[1] + combination for combination in smaller_combinations]

    binary_combinations = generate_binary_combinations(length)

    for combination in binary_combinations:
        results.append(combination)

    return results

###################################################################################################

def brute_force_attack(encrypted_data_to_crack, some_signal):
    start_time = time.time()
    key_length = len(encrypted_data_to_crack)  # Długość klucza równa długości szyfrogramu
    iterations = binary_iteration(key_length)  # Generowanie wszystkich możliwych kombinacji klucza

    for guess in iterations:
        new_key = []

        # Sprawdzanie, czy szyfrogram zgadza się z danymi oryginalnymi
        for i in range(len(guess)):
            if guess[i] == 0 and encrypted_data_to_crack[i] == 0:
                new_key.append(0)
            elif guess[i] == 1 and encrypted_data_to_crack[i] == 1:
                new_key.append(0)
            elif guess[i] == 1 and encrypted_data_to_crack[i] == 0:
                new_key.append(1)
            elif guess[i] == 0 and encrypted_data_to_crack[i] == 1:
                new_key.append(1)

            if new_key == some_signal:
                end_time = time.time()  # Czas zakończenia operacji łamania hasła
                elapsed_time = end_time - start_time  # Czas trwania operacji
                elapsed_time = round(elapsed_time, 2)
                print("Czas trwania operacji łamania klucza:", elapsed_time, "sekundy")
                return guess
            if i == len(some_signal)-1:
                new_key.clear()

###################################################################################################

def menu():
    signal = []
    scrambled_signal=[]
    descrambled_signalXOR=[]
    scrambled_signal_mul=[]
    descrambled_signal_mul=[]
    sequence_lengths=[]
    while True:
        print("\nMenu:")
        print("1. Generuj sygnał")
        print("2. Zapisz sygnał do pliku")
        print("3. Oblicz prawdopodobieństwo rozsynchronizowania")
        print("4. Zaszyfruj sygnał za pomocą XOR")
        print("5. Odszyfruj sygnał za pomocą XOR")
        print("6. Zaszyfruj sygnał za pomocą scramblera multiplikatywnego")
        print("7. Odszyfruj sygnał za pomocą descramblera multiplikatywnego")
        print("8. Zmierz długość sekwencji")
        print("9. Wyświetl histogram ilości danych sekwencji")
        print("10. Wyjście")
        print("11. Sprawdz po jakim czasie udalo sie zlamac klucz")

        choice = input("Wybierz opcję (1-10): ")

        if choice == '1':
            length = int(input("Podaj długość sygnału: "))
            min_run_length = int(input("Podaj minimalną długość sekwencji: "))
            max_run_length = int(input("Podaj maksymalną długość sekwencji: "))
            signal = generate_signal(length, min_run_length, max_run_length)
            print(f"Wygenerowany sygnał: {signal}")

        elif choice == '2':
            if signal:
                filename = input("Podaj nazwę pliku: ")
                save_signal_to_file(signal, filename)
            else:
                print("Najpierw wygeneruj sygnał!")


        elif choice == '3':
            signal_probability=[]
            choice3 = input(" 1. signal, 2. scrambler_data_xor, 3. descrambled_data_xor, 4. scrambled_data_mul, 5.descrambled_data_mul ")
            choice3 = int(choice3)  # Konwersja wyboru na integer
            if choice3 == 1:
                signal_probability=signal
            elif choice3 ==2:
                signal_probability=scrambled_signal
            elif choice3 ==3:
                signal_probability=descrambled_signalXOR
            elif choice3 ==4:
                signal_probability=scrambled_signal_mul
            elif choice3 ==5:
                signal_probability=descrambled_signal_mul
            desync_count = calculate_desynchronization_probability(signal_probability)
            print(f"Liczba rozsynchronizowań: {desync_count}")

        elif choice == '4':
            if signal:
                key_length = int(input("Podaj długość klucza: "))
                key = [random.choice([0, 1]) for _ in range(key_length)]
                scrambled_signal = xor_scramble(signal, key)
                print(f"Klucz: {key}")
                print(f"Zaszyfrowany sygnał: {scrambled_signal}")
            else:
                print("Najpierw wygeneruj sygnał!")

        elif choice == '5':
            if scrambled_signal:
                descrambled_signalXOR = xor_scramble(scrambled_signal, key)

                print(f"Odszyfrowany sygnał: {descrambled_signalXOR}")
            else:
                print("Najpierw scrambluj sygnał!")


        elif choice == '6':

            if signal:

                '''

                key_length = int(input("Podaj długość klucza: "))

                #key = [random.choice([0, 1]) for _ in range(key_length)]

                key = bitarray(key_length)

                for i in range(key_length):

                    key[i] = random.choice([0, 1])

                #1print(key)

                '''

                print("Wybierz wersję scramblera multiplikatywnego: ")

                print("1. W1 -- 1 + z^18 + z^23")

                print("2. W2 -- 1 + z^39 + z^58")

                print("3. W3 -- 1 + z^18 + z^23 + z^39 + z^58")

                scrambler_choice = 0

                '''

                while scrambler_choice < 1 or scrambler_choice > 3:

                    scrambler_choice = int(input())


                    if scrambler_choice == 1:

                        scrambled_signal_mul = mul_scrambler_w1(signal, key)

                    elif scrambler_choice == 2:

                        scrambled_signal_mul = mul_scrambler_w2(signal, key)

                    elif scrambler_choice == 3:

                        scrambled_signal_mul = mul_scrambler_w3(signal, key)

                    else:

                        print("Nieprawidłowy wybór.")

                '''

                while scrambler_choice < 1 or scrambler_choice > 3:

                    scrambler_choice = int(input())

                    if scrambler_choice < 1 or scrambler_choice > 3:
                        print("Nieprawidłowy wybór.")

                min_key_length = [24, 59, 59]

                print(
                    f"Podaj długość klucza. Klucz musi mieć długość co najmniej {min_key_length[scrambler_choice - 1]} bitów: ")

                key_length = 0

                while key_length < min_key_length[scrambler_choice - 1]:

                    key_length = int(input())

                    if key_length < min_key_length[scrambler_choice - 1]:
                        print("Niepoprawny wybór")

                key = bitarray(key_length)

                for i in range(key_length):
                    key[i] = random.choice([0, 1])

                if scrambler_choice == 1:

                    scrambled_signal_mul = mul_scrambler_w1(signal, key)

                elif scrambler_choice == 2:

                    scrambled_signal_mul = mul_scrambler_w2(signal, key)

                elif scrambler_choice == 3:

                    scrambled_signal_mul = mul_scrambler_w3(signal, key)

                print(f"Zaszyfrowany sygnał:", ''.join(map(str, scrambled_signal_mul)))

            else:

                print("Najpierw wygeneruj sygnał!")



        elif choice == '7':

            if scrambled_signal_mul:

                print("Wybierz wersję scramblera multiplikatywnego: ")

                print("1. W1 -- 1 + z^18 + z^23")

                print("2. W2 -- 1 + z^39 + z^58")

                print("3. W3 -- 1 + z^18 + z^23 + z^39 + z^58")

                scrambler_choice = 0

                # print(key)

                # print(signal)

                while scrambler_choice < 1 or scrambler_choice > 3:

                    scrambler_choice = int(input())

                    if scrambler_choice == 1:

                        descrambled_signal_mul = mul_descrambler_w1(scrambled_signal_mul, key)

                    elif scrambler_choice == 2:

                        descrambled_signal_mul = mul_descrambler_w2(scrambled_signal_mul, key)

                    elif scrambler_choice == 3:

                        descrambled_signal_mul = mul_descrambler_w3(scrambled_signal_mul, key)

                    else:

                        print("Nieprawidłowy wybór.")

                # print(signal)

                print(f"Odszyfrowany sygnał:", ''.join(map(str, descrambled_signal_mul)))


            else:

                print("Najpierw scrambluj sygnał!")

        elif choice == '8':
            data_seq_length=[]
            choice2 = input(" 1. signal, 2. scrambler_data_xor, 3. descrambled_data_xor, 4. scrambled_data_mul, 5.descrambled_data_mul ")
            choice2 = int(choice2)  # Konwersja wyboru na integer
            if choice2 == 1:
                data_seq_length=signal
            elif choice2 ==2:
                data_seq_length=scrambled_signal
            elif choice2 ==3:
                data_seq_length=descrambled_signalXOR
            elif choice2 ==4:
                data_seq_length=scrambled_signal_mul
            elif choice2 ==5:
                data_seq_length=descrambled_signal_mul

            sequence_lengths=count_sequence_lengths(data_seq_length)

        elif choice == '9':
            plot_histogram(sequence_lengths)

        elif choice == '10':
            print("Wyjście z programu.")
            break

        elif choice == '11':
            choice5 = input(" 1. scrambler_data_xor, 2. ")

            choice5 = int(choice5)  # Konwersja wyboru na integer
            if choice5 == 1:
                print(f"Klucz: {key}")
                print(f"Zaszyfrowany sygnał: {scrambled_signal}")
                print("Odszyfrowany klucz",brute_force_attack(scrambled_signal, signal))
            break
            # if choice5 == 2:

        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

if __name__ == '__main__':
    menu()
###################################################################################################

