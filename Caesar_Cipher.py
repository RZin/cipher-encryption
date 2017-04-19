import string

def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings 
    of lowercase letters.
    '''
    print('Loading words...')
    # inFile: file
    in_file = open(file_name, 'r')
    # line: string
    line = in_file.readline()
    # word_list: list of strings
    word_list = line.split()
    print('  ', len(word_list), 'words loaded.')
    in_file.close()
    return word_list
    
WORDLIST_FILENAME = 'words.txt'
wordlist = load_words(WORDLIST_FILENAME)

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    >>> is_word(word_list, 'bat') -> True
    >>> is_word(word_list, 'asdf') -> False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def read_story_string(fileName_from): 
    """
    fileName_from - string
    
    Returns: string
    """
    with open(fileName_from, 'r') as origin:
        origin_str = origin.read()
    return origin_str

def write_story_string(fileName_to, story):
    """
    fileName_to - name of file (string)
    stroy - string
    
    writes story to fileName_to
    """
    with open(fileName_to, 'w') as to_write:
        to_write.write(story)

class Message(object):
    def __init__(self, text):
        '''
        text (string): the message's text

        self.message_text (string, determined by input text)
        self.valid_words (list, determined using function load_words
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME) 

    def get_message_text(self):
        return self.message_text

    def get_valid_words(self):
        return self.valid_words[:]
        
    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a Caesar cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        contains 52 keys of all the uppercase letters and all the lowercase
        letters.        

        shift (integer): the amount by which to shift 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        al = tuple(string.ascii_lowercase)
        AL = tuple(string.ascii_uppercase)
        newal = []
        newAL = []
        for i in range(len(al) - shift):
            newal.append(al[i + shift])
            newAL.append(AL[i + shift])
        for j in range(shift):
            newal.append(al[j])
            newAL.append(AL[j])
        newal = tuple(newal)
        newAL = tuple(newAL)
        res = dict(zip(al,newal))
        res.update(dict(zip(AL,newAL)))
        return res

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26
        
        Returns: the message text (string) in which every character is shifted
        down the alphabet by the input shift
        '''
        allletters = {}
        digits = dict(zip(string.digits,string.digits))
        punctuation = dict(zip(string.punctuation,string.punctuation))
        whitespace = dict(zip(string.whitespace,string.whitespace))
        allletters.update(self.build_shift_dict(shift))
        allletters.update(digits)
        allletters.update(punctuation)
        allletters.update(whitespace)
        L = []
        for i in self.message_text:
            L.append(allletters[i])
        return ''.join(L)

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''  
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)
        '''
        Message.__init__(self, text)
        self.shift = shift
        self.enctypting_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        return self.shift
        
    def get_encrypting_dict(self):
        return self.enctypting_dict.copy()
        
    def get_message_text_encrypted(self):
        return self.message_text_encrypted
        
    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and 
        updates all attributes determined by shift

        shift (integer): the new shift 0 <= shift < 26
        '''
        self.shift = shift
        self.enctypting_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        text (string): the cipher text

        self.message_text (string, determined by input text)
        self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)
        
        
    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. 
        
        finds best shift 
            (which creates max of real words after apply_shift(shift))
            if bests shits are many - chooses any of them 
            
        decrypts message

        Returns: a tuple of the best shift 
        and the decrypted message text using that shift value 
        (10, 'Hope walks through the fire, faith leaps over it')
        '''
        def PunctDelete(text):
            '''
            text - string
            returns - string without  punctuation and so on
            '''
            l = []
            for i in text:
                l.append(i)
            l_copy = l[:]
            for i in l:
                if i in string.punctuation:
                    l_copy.remove(i)
            return ''.join(l_copy)

        maxnum = 0
        for i in range(26):
            apply = self.apply_shift(i)
            PunctDel = PunctDelete(apply)
            L = PunctDel.split(" ")
            num = 0           
            for j in L:
                if is_word(wordlist, j) == True:
                    num += 1
            if num > maxnum:
                maxnum = num
                maxi = i
        original = self.apply_shift(maxi)
        return (maxi ,original)

#Example test case (PlaintextMessage)
def test_encrypt_message():
    plaintext = PlaintextMessage('Jack', 10)
    print('Expected Output: Tkmu ')
    print('Actual Output:', plaintext.get_message_text_encrypted())

#Example test case (CiphertextMessage)
def test_decrypt_message():
    ciphertext = CiphertextMessage('Tkmu ')
    print('Expected Output:', (16, 'Jack '))
    print('Actual Output:', ciphertext.decrypt_message())

def decrypt_story(fileName_from, fileName_to):
    ''' takes encrypted text from fileName_from 
        writes original text to fileName_to
        
        returns original text str
    '''
    encrypted_str = read_story_string(fileName_from)
    to_decrypt = CiphertextMessage(encrypted_str)# use gen
    write_story_string(fileName_to, to_decrypt.decrypt_message()[1])
    return to_decrypt.decrypt_message()[1]

def encrypt_story(fileName_from, fileName_to,):
    ''' takes original text from 'fileName_from'
        writes encrypted to file 'fileName_to'
        
        returns encrypted text str
    '''    
    origin_str = read_story_string(fileName_from)
    to_encrypt = PlaintextMessage(origin_str, 10)
    write_story_string(fileName_to, to_encrypt.message_text_encrypted)
    return to_encrypt.message_text_encrypted

print(encrypt_story('message.txt' ,'encrypted.txt'))
print(decrypt_story('encrypted.txt', 'original.txt'))
