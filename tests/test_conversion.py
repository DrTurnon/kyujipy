from unittest import TestCase
from kyujipy import KyujitaiConverter


class TestConverter(TestCase):
    def setUp(self):
        self.converter = KyujitaiConverter()

    def test_shinjitai_to_kyujitai(self):
        kyujitai_ref = "日本國の辯護士は本當に最高ですよ！"
        s = self.converter.shinjitai_to_kyujitai("日本国の弁護士は本当に最高ですよ！")
        self.assertEqual(s, kyujitai_ref)

    def test_kyujitai_to_shinjitai(self):
        shinjitai_ref = "この列は東亜連合の旅券のみである。"
        s = self.converter.kyujitai_to_shinjitai("この列は東亞聯合の旅券のみである。")
        self.assertEqual(s, shinjitai_ref)

    def test_basic_asymmetrical_conversion(self):
        kyujitai_ref = "亘、凛、晃、晋、萌"
        shinjitai = self.converter.kyujitai_to_shinjitai("亙、凜、晄、晉、萠")
        s = self.converter.shinjitai_to_kyujitai(shinjitai)
        self.assertEqual(s, kyujitai_ref)

    def test_kakikae_asymmetrical_conversion(self):
        kyujitai_ref = "飢餓の障礙は以上です。"
        shinjitai = self.converter.kyujitai_to_shinjitai("饑餓の障礙は已上です。")
        s = self.converter.shinjitai_to_kyujitai(shinjitai)
        self.assertEqual(s, kyujitai_ref)

    def test_shinijtai_to_kyujitai_exception(self):
        kyujitai_ref = "欠缺"
        s = self.converter.shinjitai_to_kyujitai("欠缺")
        self.assertEqual(s, kyujitai_ref)

    def test_kyujitai_to_shinijtai_exception(self):
        shinjitai_ref = "欠缺"
        s = self.converter.kyujitai_to_shinjitai("欠缺")
        self.assertEqual(s, shinjitai_ref)

    def test_partial_shinjitai_to_kyujitai(self):
        kyujitai_ref = "詭辯"
        s = self.converter.shinjitai_to_kyujitai("奇弁")
        self.assertEqual(s, kyujitai_ref)
        s = self.converter.shinjitai_to_kyujitai("詭弁")
        self.assertEqual(s, kyujitai_ref)
        s = self.converter.shinjitai_to_kyujitai("奇辯")
        self.assertEqual(s, kyujitai_ref)

    def test_multiple_kyujitai_to_shinjitai(self):
        shinjitai_ref = "奇弁"
        s = self.converter.kyujitai_to_shinjitai("奇辯")
        self.assertEqual(s, shinjitai_ref)
        s = self.converter.kyujitai_to_shinjitai("詭弁")
        self.assertEqual(s, shinjitai_ref)
        s = self.converter.kyujitai_to_shinjitai("詭辯")
        self.assertEqual(s, shinjitai_ref)

    def test_long_word_kyujitai_to_shinjitai(self):
        shinjitai_ref = "意固地"
        s = self.converter.kyujitai_to_shinjitai("意怙地")
        self.assertEqual(s, shinjitai_ref)
        s = self.converter.kyujitai_to_shinjitai("依固地")
        self.assertEqual(s, shinjitai_ref)
        s = self.converter.kyujitai_to_shinjitai("依怙地")
        self.assertEqual(s, shinjitai_ref)
