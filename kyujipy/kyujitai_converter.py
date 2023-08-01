import cson
import os

from kyujipy.basic_converter import BasicConverter


class KyujitaiConverter(object):
    """
    Full converter, converting Shinjitai to Kyujitai, and vice versa (WITH kakikae)
    """

    def _generate_conversion_tree(self, initial_word, conversions):
        converted_words = []
        for before, after in conversions:
            converted_word = initial_word.replace(before, after)
            if initial_word != converted_word:
                converted_words.append(converted_word)

        if not converted_words:
            # No more conversions possible, final word reached
            return initial_word

        conversion_tree = []
        for converted_word in converted_words:
            conversion_tree.append(
                self._generate_conversion_tree(converted_word, conversions)
            )
        return {initial_word: conversion_tree}

    def _shinjitai_to_kyujitai_dict_from_tree(self, conversion_tree, conversion_dict):
        for word, node in conversion_tree.items():
            conversion_dict[word] = word
            for conversion_subtree in node:
                if isinstance(conversion_subtree, str):
                    for key, value in conversion_dict.items():
                        if key == value:
                            conversion_dict[key] = conversion_subtree
                else:
                    self._shinjitai_to_kyujitai_dict_from_tree(
                        conversion_subtree, conversion_dict
                    )

    def _kyujitai_to_shinjitai_dict_from_tree(self, conversion_tree, initial_word):
        def _extract_words_from_subtree(conversion_node):
            converted_words = []
            for conversion_subtree in conversion_node:
                if isinstance(conversion_subtree, str):
                    converted_words.append(conversion_subtree)
                else:
                    for word, subnode in conversion_subtree.items():
                        converted_words.append(word)
                        converted_words += _extract_words_from_subtree(subnode)
            return converted_words

        node = conversion_tree[initial_word]
        converted_words = _extract_words_from_subtree(node)
        return {converted_word: initial_word for converted_word in converted_words}

    def __init__(self):
        # Use BasicConverter to convert individual Shinjitai/Kyujitai characters
        self.basic_converter = BasicConverter()

        # Determine Kakikae databases paths
        kakikae_simplified_db_path = os.path.join("data", "kakikae_simplified.cson")
        kakikae_variants_db_path = os.path.join("data", "kakikae_variants.cson")

        # Parse Kakikae database
        with open(
            kakikae_simplified_db_path, "r", encoding="utf-8"
        ) as kakikae_simplified_db_file:
            self.kakikae_database_simplified = cson.load(kakikae_simplified_db_file)
        with open(
            kakikae_variants_db_path, "r", encoding="utf-8"
        ) as kakikae_variants_db_file:
            self.kakikae_database_variants = cson.load(kakikae_variants_db_file)

        # Build Kakikae conversion databases
        self.word_dictionary = {}
        self.kakikae_encode_database = {}
        self.kakikae_decode_database = {}

        # First step, build word dictionary
        for entry in self.kakikae_database_simplified:
            for word in entry.get("words"):
                if word not in self.word_dictionary:
                    self.word_dictionary[word] = {}
                if "simplified" not in self.word_dictionary[word]:
                    self.word_dictionary[word]["simplified"] = []
                self.word_dictionary[word]["simplified"].append(
                    {
                        "new": entry["new"],
                        "old": entry["old"],
                    }
                )

        for entry in self.kakikae_database_variants:
            for word in entry.get("words"):
                if word not in self.word_dictionary:
                    self.word_dictionary[word] = {}
                if "variants" not in self.word_dictionary[word]:
                    self.word_dictionary[word]["variants"] = []
                self.word_dictionary[word]["variants"].append(
                    {
                        "new": entry["new"],
                        "old": entry["old"],
                    }
                )

        # Second step, build word dictionary
        for word, word_dict in self.word_dictionary.items():
            # Simplified database, both used for encoding and decoding
            simplified_chars = word_dict.get("simplified")

            # Variants database, only used for decoding (Kyujitai to Shinjitai conversion)
            variant_chars = word_dict.get("variants")

            if simplified_chars:
                # Encode database (Shinjitai to Kyujitai)
                conversions = [
                    (simplified_char_dict["new"], simplified_char_dict["old"][0])
                    for simplified_char_dict in simplified_chars
                ]
                conversion_tree = self._generate_conversion_tree(word, conversions)
                conversion_dict = {}
                self._shinjitai_to_kyujitai_dict_from_tree(
                    conversion_tree, conversion_dict
                )
                self.kakikae_encode_database.update(conversion_dict)

                # Decode database (Kyujitai to Shinjitai)
                conversions = [
                    (simplified_char_dict["new"], old_simplified_char_dict)
                    for simplified_char_dict in simplified_chars
                    for old_simplified_char_dict in simplified_char_dict["old"]
                ]
                conversion_tree = self._generate_conversion_tree(word, conversions)
                self.kakikae_decode_database.update(
                    self._kyujitai_to_shinjitai_dict_from_tree(conversion_tree, word)
                )

            if variant_chars:
                # Decode database (Kyujitai to Shinjitai)
                conversions = [
                    (variant_char_dict["new"], old_variant_char_dict)
                    for variant_char_dict in variant_chars
                    for old_variant_char_dict in variant_char_dict["old"]
                ]
                conversion_tree = self._generate_conversion_tree(word, conversions)
                self.kakikae_decode_database.update(
                    self._kyujitai_to_shinjitai_dict_from_tree(conversion_tree, word)
                )

    def shinjitai_to_kyujitai(self, input_string):
        # revert douon no kanji ni yoru kakikae
        for word in self.kakikae_encode_database:
            input_string = input_string.replace(
                word, self.kakikae_encode_database[word]
            )

        # convert remaining individual characters
        input_string = self.basic_converter.shinjitai_to_kyujitai(input_string)

        return input_string

    def kyujitai_to_shinjitai(self, input_string):
        # convert individual characters first
        input_string = self.basic_converter.kyujitai_to_shinjitai(input_string)

        # apply douon no kanji ni yoru kakikae
        for word in self.kakikae_decode_database:
            input_string = input_string.replace(
                word, self.kakikae_decode_database[word]
            )

        return input_string
