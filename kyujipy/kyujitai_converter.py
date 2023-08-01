import cson
import os

from kyujipy.basic_converter import BasicConverter
from kyujipy.conversion_node import ConversionNode


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
        with open(kakikae_simplified_db_path, 'r', encoding="utf-8") as kakikae_simplified_db_file:
            self.kakikae_database_simplified = cson.load(kakikae_simplified_db_file)
        with open(kakikae_variants_db_path, 'r', encoding="utf-8") as kakikae_variants_db_file:
            self.kakikae_database_variants = cson.load(kakikae_variants_db_file)

        # Build Kakikae conversion databases
        self.kakikae_encode_database = {}
        self.kakikae_decode_database = {}

        # Simplified database, both used for encoding and decoding
        for entry in self.kakikae_database_simplified:
            new_char = entry['new']
            base_old_char = entry['old'][0]
            # Encode (Shinjitai to Kyujitai) database keys
            for word in entry.get('words'):
                self.kakikae_encode_database[word] = self.kakikae_encode_database.get(word, word).replace(new_char, base_old_char)
            # Decode (Kyujitai to Shinjitai) database keys
            for old_char in entry['old']:
                for word in entry.get('words'):
                    word = word.replace(new_char, old_char)
                    self.kakikae_decode_database[word] = self.kakikae_decode_database.get(word, word).replace(old_char, new_char)

        # Variants database, only used for decoding (Kyujitai to Shinjitai conversion)
        for entry in self.kakikae_database_variants:
            new_char = entry['new']
            for old_char in entry['old']:
                for word in entry.get('words'):
                    word = word.replace(new_char, old_char)
                    self.kakikae_decode_database[word] = self.kakikae_decode_database(word, word).replace(old_char, new_char)

    def shinjitai_to_kyujitai(self, input_string):

        # revert douon no kanji ni yoru kakikae
        for word in self.kakikae_encode_database:
            input_string = input_string.replace(word, self.kakikae_encode_database[word])

        # convert remaining individual characters
        input_string = self.basic_converter.shinjitai_to_kyujitai(input_string)

        return input_string

    def kyujitai_to_shinjitai(self, input_string):

        # convert individual characters first
        input_string = self.basic_converter.kyujitai_to_shinjitai(input_string)

        # apply douon no kanji ni yoru kakikae
        for word in self.kakikae_decode_database:
            input_string = input_string.replace(word, self.kakikae_decode_database[word])

        return input_string