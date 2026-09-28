''' It loads enterprise data from JSON and validate the CIF of each enterprise
Classes:
    Encode
    Decode
    Main
Author: Shuhan Ying and Hao Chen
Date: 2026-02-05'''

import string
from uc3m_consulting import EnterpriseManager


#GLOBAL VARIABLES
LETTERS = string.ascii_letters + string.punctuation + string.digits
SHIFT = 3



def encode(word):
    '''The function receive a word and encode it '''
    encoded = ""
    for letter in word:
        if letter == ' ':
            encoded = encoded + ' '
        else:

            x = (LETTERS.index(letter) + SHIFT) % len(LETTERS)
            encoded = encoded + LETTERS[x]
    return encoded

def decode(word):
    '''The function receive a word and encode it, obtaining an original string'''
    encoded = ""
    for letter in word:
        if letter == ' ':
            encoded = encoded + ' '
        else:
            x = (LETTERS.index(letter) - SHIFT) % len(LETTERS)
            encoded = encoded + LETTERS[x]
    return encoded


def main():
    '''This is the main function to execute the program'''
# Test with the correct CIF value
    mng = EnterpriseManager()
    res1 = mng.readProductCodeFromJson("test_correct.json")
    str_res1 = str(res1)
    print(str_res1)
    encode_res1 = encode(str_res1)
    print("Encoded Res "+ encode_res1)
    decode_res1 = decode(encode_res1)
    print("Decoded Res: " + decode_res1)
    print("cif: " + res1.enterprise_cif)
    print("enterprise_name: " + res1.enterprise_name)
    print("enterprise_phone: " + res1.phone_number)
    enterprise=EnterpriseManager()
    print(enterprise.validateCif(res1.enterprise_cif))

# Test with the wrong CIF value, since the CIF value is not valid it raises to error
    mng = EnterpriseManager()
    res2 = mng.readProductCodeFromJson("test_wrong.json")
    str_res2 = str(res2)
    print(str_res2)
    encode_res2 = encode(str_res2)
    print("Encoded Res " + encode_res2)
    decode_res2 = decode(encode_res2)
    print("Decoded Res: " + decode_res2)
    print("cif: " + res2.enterprise_cif)
    print("enterprise_name: " + res2.enterprise_name)
    print("enterprise_phone: " + res2.phone_number)

    enterprise = EnterpriseManager()
    print(enterprise.validateCif(res2.enterprise_cif))
if __name__ == "__main__":
    main()
