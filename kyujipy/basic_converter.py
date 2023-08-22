import cson
import os

EXCEPTIONS_KYUJITAI = {
    "缺缺": "欠缺",
}

EXCEPTIONS_SHINJITAI = {
    "欠欠": "欠缺",
}


class BasicConverter(object):
    """
    Basic converter, only converting Shinjitai to Kyujitai, and vice versa (WITHOUT kakikae)
    """

    def __init__(self):
        # Determine Shinjitai/Kyujitai database path
        current_path = os.path.abspath(os.path.dirname(__file__))
        kyujitai_simplified_db_path = os.path.join(
            current_path, "data", "kyujitai_simplified.cson"
        )
        kyujitai_variants_db_path = os.path.join(
            current_path, "data", "kyujitai_variants.cson"
        )

        # Parse Kyujitai database
        with open(
            kyujitai_simplified_db_path, "r", encoding="utf-8"
        ) as kyujitai_simplified_db_file:
            self.kyujitai_data_simplified = cson.load(kyujitai_simplified_db_file)
        with open(
            kyujitai_variants_db_path, "r", encoding="utf-8"
        ) as kyujitai_variants_db_file:
            self.kyujitai_data_variants = cson.load(kyujitai_variants_db_file)

        # Build Shinjitai to Kyujitai conversion databases
        self.shinjitai_to_kyujitai_database = {}
        self.kyujitai_to_shinjitai_database = {}

        # create Shinjitai/Kyujitai dictionaries
        for entry in self.kyujitai_data_simplified:
            shinjitai = entry[0]
            kyujitai = entry[1]
            self.shinjitai_to_kyujitai_database[shinjitai] = kyujitai
            self.kyujitai_to_shinjitai_database[kyujitai] = shinjitai

        for entry in self.kyujitai_data_variants:
            shinjitai = entry[0]
            kyujitai = entry[1]
            self.kyujitai_to_shinjitai_database[kyujitai] = shinjitai

    def shinjitai_to_kyujitai(self, input_string):
        # convert individual characters
        for char in self.shinjitai_to_kyujitai_database:
            input_string = input_string.replace(
                char, self.shinjitai_to_kyujitai_database[char]
            )

        # process conversion exceptions
        for word in EXCEPTIONS_KYUJITAI:
            input_string = input_string.replace(word, EXCEPTIONS_KYUJITAI[word])

        return input_string

    def kyujitai_to_shinjitai(self, input_string):
        # convert individual characters
        for char in self.kyujitai_to_shinjitai_database:
            input_string = input_string.replace(
                char, self.kyujitai_to_shinjitai_database[char]
            )

        # process conversion exceptions
        for word in EXCEPTIONS_SHINJITAI:
            input_string = input_string.replace(word, EXCEPTIONS_SHINJITAI[word])

        return input_string
