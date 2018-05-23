import cson
import os

EXCEPTIONS_KYUJITAI = {'缺缺': '欠缺'}
EXCEPTIONS_SHINJITAI = {'欠欠': '欠缺'}


class KyujitaiConverter(object):

    def __init__(self):

        # Determine databases path
        current_path = os.path.abspath(os.path.dirname(__file__))
        kakikae_db_path = os.path.join(current_path, 'kakikae.cson')
        kyujitai_db_path = os.path.join(current_path, 'kyujitai.cson')

        # Parse Kakikae database
        kakikae_db_file = open(kakikae_db_path, 'r', encoding="utf-8")
        self.kakikae_data = cson.load(kakikae_db_file)
        kakikae_db_file.close()

        # Parse Kyujitai database
        kyujitai_db_file = open(kyujitai_db_path, 'r', encoding="utf-8")
        self.kyujitai_data = cson.load(kyujitai_db_file)
        kyujitai_db_file.close()

        # Build Kakikae conversion databases
        self.kakikae_encode_database = {}
        self.kakikae_decode_database = {}

        # First step: index of all potential words (build database keys)
        for entry in self.kakikae_data:
            base_new_char = entry['new'][0]
            # Encode database keys
            for new_char in entry['new']:
                for word in entry.get('words'):
                    # replace base_new_char with current new_char
                    if new_char != base_new_char:
                        word = new_char.join(word.split(base_new_char))
                    # add word if not already in database
                    if word not in self.kakikae_encode_database:
                        self.kakikae_encode_database[word] = word
            # Decoding database keys
            for old_char in entry['old']:
                for word in entry.get('words'):
                    word = old_char.join(word.split(base_new_char))
                    if word not in self.kakikae_decode_database:
                        self.kakikae_decode_database[word] = word

        # Second step: replace Kakikae characters (build database values)
        for entry in self.kakikae_data:
            base_new_char = entry['new'][0]
            base_old_char = entry['old'][0]
            # Encoding database values
            for new_char in entry['new']:
                for word in entry.get('words'):
                    # replace base_new_char with current new_char
                    if new_char != base_new_char:
                        word = new_char.join(word.split(base_new_char))
                    self.kakikae_encode_database[word] = base_old_char.join(
                        self.kakikae_encode_database[word].split(new_char))
            # Decoding database values
            for old_char in entry['old']:
                for word in entry.get('words'):
                    word = old_char.join(word.split(base_new_char))
                    self.kakikae_decode_database[word] = base_new_char.join(
                        self.kakikae_decode_database[word].split(old_char))

        # Build Shinjitai to Kyujitai conversion databases
        self.shinjitai_to_kyujitai_database = {}
        self.kyujitai_to_shinjitai_database = {}

        # create Shinjitai/Kyujitai dictionaries
        for entry in self.kyujitai_data:
            shinjitai = entry[0]
            kyujitai = entry[1]
            self.shinjitai_to_kyujitai_database[shinjitai] = kyujitai
            self.kyujitai_to_shinjitai_database[kyujitai] = shinjitai

    def shinjitai_to_kyujitai(self, input_string):

        # revert douon no kanji ni yoru kakikae
        for word in self.kakikae_encode_database:
            input_string = self.kakikae_encode_database[word].join(input_string.split(word))

        # convert remaining individual characters
        for char in self.shinjitai_to_kyujitai_database:
            input_string = self.shinjitai_to_kyujitai_database[char].join(input_string.split(char))

        # process conversion exceptions
        for word in EXCEPTIONS_KYUJITAI:
            input_string = EXCEPTIONS_KYUJITAI[word].join(input_string.split(word))

        return input_string

    def kyujitai_to_shinjitai(self, input_string):

        # convert individual characters first
        for char in self.kyujitai_to_shinjitai_database:
            input_string = self.kyujitai_to_shinjitai_database[char].join(input_string.split(char))

        # apply douon no kanji ni yoru kakikae
        for word in self.kakikae_decode_database:
            input_string = self.kakikae_decode_database[word].join(input_string.split(word))

        # process conversion exceptions
        for word in EXCEPTIONS_SHINJITAI:
            input_string = EXCEPTIONS_SHINJITAI[word].join(input_string.split(word))

        return input_string
