import cson
import os

EXCEPTIONS_KYUJITAI = {
    '缺缺': '欠缺',
    '共倭國': '共和國',
}

EXCEPTIONS_SHINJITAI = {
    '欠欠': '欠缺',
}

class BasicConverter(object):
    """
    Basic converter, only converting Shinjitai to Kyujitai, and vice versa (WITHOUT kakikae)
    """

    def __init__(self):

        # Determine Shinjitai/Kyujitai database path
        current_path = os.path.abspath(os.path.dirname(__file__))
        kyujitai_db_path = os.path.join(current_path, 'kyujitai.cson')

        # Parse Kyujitai database
        kyujitai_db_file = open(kyujitai_db_path, 'r', encoding="utf-8")
        self.kyujitai_data = cson.load(kyujitai_db_file)
        kyujitai_db_file.close()

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

        # convert individual characters
        for char in self.shinjitai_to_kyujitai_database:
            input_string = self.shinjitai_to_kyujitai_database[char].join(input_string.split(char))

        # process conversion exceptions
        for word in EXCEPTIONS_KYUJITAI:
            input_string = EXCEPTIONS_KYUJITAI[word].join(input_string.split(word))

        return input_string

    def kyujitai_to_shinjitai(self, input_string):

        # convert individual characters
        for char in self.kyujitai_to_shinjitai_database:
            input_string = self.kyujitai_to_shinjitai_database[char].join(input_string.split(char))

        # process conversion exceptions
        for word in EXCEPTIONS_SHINJITAI:
            input_string = EXCEPTIONS_SHINJITAI[word].join(input_string.split(word))

        return input_string


class KyujitaiConverter(object):
    """
    Full converter, converting Shinjitai to Kyujitai, and vice versa (WITH kakikae)
    """

    def __init__(self):

        # Use BasicConverter to convert individual Shinjitai/Kyujitai characters
        self.basic_converter = BasicConverter()

        # Determine Kakikae databases paths
        current_path = os.path.abspath(os.path.dirname(__file__))
        kakikae_simplified_db_path = os.path.join(current_path, 'kakikae_simplified.cson')
        kakikae_variants_db_path = os.path.join(current_path, 'kakikae_variants.cson')

        # Parse Kakikae database
        kakikae_simplified_db_file = open(kakikae_simplified_db_path, 'r', encoding="utf-8")
        self.kakikae_database_simplified = cson.load(kakikae_simplified_db_file)
        kakikae_simplified_db_file.close()
        kakikae_variants_db_file = open(kakikae_variants_db_path, 'r', encoding="utf-8")
        self.kakikae_database_variants = cson.load(kakikae_variants_db_file)
        kakikae_variants_db_file.close()

        # Build Kakikae conversion databases
        self.kakikae_encode_database = {}
        self.kakikae_decode_database = {}

        # First step: index of all potential words (build database keys)
        for entry in self.kakikae_database_simplified:
            new_char = entry['new']
            # Encode (Shinjitai to Kyujitai) database keys
            for word in entry.get('words'):
                # add word if not already in database
                if word not in self.kakikae_encode_database:
                    self.kakikae_encode_database[word] = word
            # Decode (Kyujitai to Shinjitai) database keys
            for old_char in entry['old']:
                for word in entry.get('words'):
                    word = old_char.join(word.split(new_char))
                    if word not in self.kakikae_decode_database:
                        self.kakikae_decode_database[word] = word
        # Variants database only used for decoding (Kyujitai to Shinjitai conversion)
        for entry in self.kakikae_database_variants:
            new_char = entry['new']
            for old_char in entry['old']:
                for word in entry.get('words'):
                    word = old_char.join(word.split(new_char))
                    if word not in self.kakikae_decode_database:
                        self.kakikae_decode_database[word] = word

        # Second step: replace Kakikae characters (build database values)
        for entry in self.kakikae_database_simplified:
            new_char = entry['new']
            base_old_char = entry['old'][0]
            # Encode (Shinjitai to Kyujitai) database values
            for word in entry.get('words'):
                self.kakikae_encode_database[word] = base_old_char.join(
                    self.kakikae_encode_database[word].split(new_char))
            # Decode (Kyujitai to Shinjitai) database values
            for old_char in entry['old']:
                for word in entry.get('words'):
                    word = old_char.join(word.split(new_char))
                    self.kakikae_decode_database[word] = new_char.join(
                        self.kakikae_decode_database[word].split(old_char))
        # Variants database only used for decoding (Kyujitai to Shinjitai conversion)
        for entry in self.kakikae_database_variants:
            new_char = entry['new']
            for old_char in entry['old']:
                for word in entry.get('words'):
                    word = old_char.join(word.split(new_char))
                    self.kakikae_decode_database[word] = new_char.join(
                        self.kakikae_decode_database[word].split(old_char))

    def shinjitai_to_kyujitai(self, input_string):

        # revert douon no kanji ni yoru kakikae
        for word in self.kakikae_encode_database:
            input_string = self.kakikae_encode_database[word].join(input_string.split(word))

        # convert remaining individual characters
        input_string = self.basic_converter.shinjitai_to_kyujitai(input_string)

        return input_string

    def kyujitai_to_shinjitai(self, input_string):

        # convert individual characters first
        input_string = self.basic_converter.kyujitai_to_shinjitai(input_string)

        # apply douon no kanji ni yoru kakikae
        for word in self.kakikae_decode_database:
            input_string = self.kakikae_decode_database[word].join(input_string.split(word))

        return input_string
