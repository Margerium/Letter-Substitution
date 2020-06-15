import time
import argparse
import json


def is_key_file_valid(cipher_type, file_type, rotation, alphabet):
    """Function that checks the validity of the '.key' json file

    :param cipher_type: Checks the json object 'ciphertype' for 'lettersubstitution' as this is the only valid input
    :type cipher_type: str

    :param file_type: Checks the json object 'filetype' for 'key' as this is the only valid input
    :type file_type: str

    :param rotation: Checks the json object 'rotate' for a valid integer between 0 and 25
    :type rotation: int

    :param alphabet: Checks the json object 'key' for 26 alphabet entries
    :type alphabet: dict

    """
    if cipher_type != "lettersubstitution":
        print("\nInvalid cipher type, expecting 'lettersubstitution', please check your .key file!")
        exit(0)

    elif file_type != "key":
        print("\nInvalid file type, expecting 'key', please check your .key file!")
        exit(0)

    elif 0 > rotation > 25:
        print("\nInvalid rotation, expecting an integer value between 0 and 25, please check your .key file!")
        exit(0)

    elif len(alphabet) != 26:
        print("\nInvalid alphabet, expecting 26 entries for A - Z, please check your .key file!")
        exit(0)

    elif len(alphabet) == 26:
        try:
            key_alphabet = {}
            # starting with an empty dictionary, the function will check for entries A - Z in the 'key' and the
            # paired value for A - Z to ensure the key is valid.
            for letter in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                           "S", "T", "U", "V", "W", "X", "Y", "Z"]:
                if alphabet[letter] in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
                                        "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]:
                    key_alphabet[letter] = alphabet[letter]

                else:
                    print("\nYour 'key' does not contain valid pairs for entries A - Z. Please check your .key file!")

                # example, if key contains {"A":"Z" , ...} then alphabet["A"] will return "Z" and as Z is a letter in
                # the alphabet it will be added to the dictionary key_alphabet (key_alphabet["A"] = "Z" in this
                # case). if all 26 key entries and their assigned pair are in A - Z, key_alphabet will contain 26
                # entries and the .key file will pass its validity check!

            if len(key_alphabet) == 26:
                print("\nKey is valid!")
                return True

        except LookupError:
            # if an invalid character is in the alphabet, a lookup error occurs
            print("\nYour 'key' does not contain entries A - Z. Please check your .key file!")
            exit(0)


def letter_substitution(code_type, text, rotation, key):
    """Function that implements the letter substitution to the provided text, uses parameters from the .key file

    :param code_type: 'Encoding' or 'Decoding', controlled with argparse commands (-e or -d) (see below)
    :type code_type: str

    :param text: The text the function will 'code', provided via a .txt file controlled with argparse commands
    (-i "my_file.txt")
    :type text: file / str

    :param rotation: The rotation sets what a letter will be set to after its first instance, for example with a
    rotation of 1, assuming a key where "A":"Z", the first "A" will become "Z", the second will become "Y" and the
    third will become "X" and so on, provided via the .key file, set by argparse command (-k "my_file.key")
    :type rotation: int

    :param key: The key is the A - Z alphabet provided in the .key file, it should be in the form of a paired value
    dictionary, for example {"A":"Z", "B":"Y", "C":"X", ... , "Z":"A"). This controls what a letter will be subbed to
    :type key: dict

    """
    print("\nPlease wait, operation in progress")
    start_time = time.time()
    # gets the time at which this function is started

    iteration = 0
    # this tracks the total shift for a letter, its value is determined by adding or subtracting the rotation value
    # in the .key file each time a letter is substituted
    translated = ""
    # your translated text, starts as an empty string

    for character in text:

        num = ord(character)
        # converts the current character in your text to an ASCII value

        if character.upper() in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q",
                                 "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]:
            # checks whether the current character is in the A - Z alphabet, allows the function to ignore spaces and
            # punctuation

            if character.isupper():
                # checks whether the character is upper or lower as they have different ASCII values (ord(A) != ord(a)

                if code_type == "e":
                    # "e" for encoding

                    num = ord(key[character]) - iteration
                    # when encoding the current character is swapped with its paired value in the key minus the
                    # iteration value
                    if num > ord("Z"):
                        # prevents the character from being coded to a character outside the A - Z alphabet
                        num = num - 26

                    elif num < ord("A"):
                        num = num + 26

                    translated = translated + chr(num)
                    # adds the coded character (now translated) to the output
                    iteration = iteration + rotation
                    # rotation is added to iteration when encoding
                    iteration = iteration % 26
                    # ensures the iteration remains within the A - Z alphabet

                elif code_type == "d":
                    # "d" for decoding

                    num = ord(key[character]) + iteration
                    # opposite to the above comments applies when decoding for the mathematics regarding iteration
                    # and rotation

                    if num > ord("Z"):
                        num = num - 26

                    elif num < ord("A"):
                        num = num + 26

                    translated = translated + chr(num)
                    iteration = iteration - rotation
                    iteration = iteration % 26

            elif character.islower():

                if code_type == "e":

                    num = ord(key[character.upper()].lower()) - iteration

                    if num > ord("z"):
                        num = num - 26

                    elif num < ord("a"):
                        num = num + 26

                    translated = translated + chr(num)
                    iteration = iteration + rotation
                    iteration = iteration % 26

                elif code_type == "d":

                    num = ord(key[character.upper()].lower()) + iteration

                    if num > ord("z"):
                        num = num - 26

                    elif num < ord("a"):
                        num = num + 26

                    translated = translated + chr(num)
                    iteration = iteration - rotation
                    iteration = iteration % 26

        else:
            translated = translated + chr(num)
            # if the character is a space or other punctuation it is not coded and so is immediately added to the output

    print("\nThe operation took %s seconds to perform" % (time.time() - start_time))
    # gets the time when the function finishes, subtracts the start time from this value to ascertain the total time
    # taken to run the function
    return translated
    # function returns the whole translated output


parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group()
group.add_argument("-e", "--encode", action="store_true", help="Tells the program to encode your text")
group.add_argument("-d", "--decode", action="store_true", help="Tells the program to decode your text")
group.add_argument("-l", "--text_length", action="store_true", help="Shows the total length of your text")

parser.add_argument("-k", type=str, required=True, help="Provide your key file - example 'sub_cipher_test_1.key'")
parser.add_argument("-i", type=str, required=True, help="Provide a name for your input file")
parser.add_argument("-o", type=str, required=True, help="Provide a name for your output file")
parser.add_argument("-s", type=int, required=False, help="Tells the program to start from a certain character in the "
                                                         "text")
parser.add_argument("-n", type=int, required=False, help="Tells the program to output a certain number of characters "
                                                         "from the text")
parser.add_argument("-p", "--print_to_screen", action="store_true", required=False, help="Tells the program to print "
                                                                                         "the output to the console")
args = parser.parse_args()

input_file_name = args.i
# assigns the -i argument to the input file name: -i "my_input.txt" will assign "my_input.txt" as the input file name
output_file_name = args.o
# same as above, -o argument assigns the output file name ("my_output.txt)
key_file_name = args.k
# same as above, -k argument assigns the key file name ("my_key.key")
starting_character_in_file = args.s
# the -s argument assigns the starting character in the input file: -s 1000 would run the function from the 1000th
# character in the input text
number_of_characters_to_output = args.n
# same as above, the -n command assigns the number of characters to output

key_file = open(key_file_name, "r", encoding="utf8")
# opens the .key file, loads the json objects inside and then closes the .key file
json_object = json.load(key_file)
key_file.close()

input_file = open(input_file_name, "r", encoding="utf8")
# opens the input file, assigns it to a variable and then closes the input file
input_text = input_file.read()
input_file.close()

if isinstance(starting_character_in_file, int):
    if starting_character_in_file > len(input_text):
        # prevents the user trying to use a start point outside the scope of the file
        print("\nYou have chosen a starting point that is larger than the number of characters in your file! Use the "
              "-l command to check the number of characters in your file!")
        exit(0)
    input_text = input_text[starting_character_in_file:]

# if the -s command was used, sets the starting character

if isinstance(number_of_characters_to_output, int):
    input_text = input_text[:number_of_characters_to_output]
# if the -n command was used, sets the number of characters to output

if is_key_file_valid(json_object["ciphertype"], json_object["filetype"], json_object["rotate"], json_object["key"]):
    # runs the .key file check, if the key is valid, the program calls the substitution function, otherwise exits

    if args.encode:
        # if encoding, opens or creates the output file and runs your input text through the substitution function
        # configured for encoding, the output from the function is written to the output file
        output_file = open(output_file_name, "w", encoding="utf8")
        output_file.write(letter_substitution("e", input_text, json_object["rotate"], json_object["key"]))
        output_file.close()

        if args.print_to_screen:
            # if the -p command was used, re-opens output file and assigns its contents to a variable before closing
            # the file again, the output is then printed to the screen, with an additional check for large outputs
            output_file = open(output_file_name, "r", encoding="utf8")
            output_text = output_file.read()
            output_file.close()

            if len(output_text) > 5000:
                # check to prevent the user from inadvertently outputting a large text dump to the console
                print("\nRemember, when running this program you can use the -s and -n commands to set a start point "
                      "and max number of characters to output respectively")
                print_text = input("\nYour text is more than 5000 characters, are you sure you want to print to "
                                   "console? (Y/N): ")

                while print_text.upper() != "Y" and print_text.upper() != "N":
                    print_text = input("\nPlease enter 'Y' or 'N': ")

                if print_text.upper() == "Y":
                    print("\n", output_text)

                elif print_text.upper() == "N":
                    exit(0)

            else:
                print("\n", output_text)
                exit(0)

        else:
            exit(0)

    elif args.decode:
        # same as the comments for encoding, only the substitution function is set to decode mode
        output_file = open(output_file_name, "w", encoding="utf8")
        output_file.write(letter_substitution("d", input_text, json_object["rotate"], json_object["key"]))
        output_file.close()

        if args.print_to_screen:
            output_file = open(output_file_name, "r", encoding="utf8")
            output_text = output_file.read()
            output_file.close()

            if len(output_text) > 5000:
                print(
                    "\nRemember, when running this program you can use the -s and -n commands to set a start point and "
                    "max number of characters to output respectively")
                print_text = input("\nYour text is more than 5000 characters, are you sure you want to print to "
                                   "console? (Y/N): ")

                while print_text.upper() != "Y" and print_text.upper() != "N":
                    print_text = input("\nPlease enter 'Y' or 'N': ")

                if print_text.upper() == "Y":
                    print("\n", output_text)
                    exit(0)

                elif print_text.upper() == "N":
                    exit(0)

            else:
                print("\n", output_text)
                exit(0)

        else:
            exit(0)

    elif args.text_length:
        # if the -l command is used instead of -e or -d, the number of characters in the input text file is simply
        # printed to the screen before terminating
        print("\nyour text file contains", len(input_text), "characters")
        exit(0)

    else:
        print("\nPlease provide one of the following arguments:")
        print("\n '-e' to encode your text ")
        print("\n '-d' to decode your text")
        print("\n '-l' to show the length of your text")
        print("\nTo see a list of all available commands, use the -h command")
        exit(0)
