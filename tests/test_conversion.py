from unittest import TestCase
from kyujipy import KyujitaiConverter


class TestConverter(TestCase):

    def test_shinjitai_to_kyujitai(self):
        converter = KyujitaiConverter()
        kyujitai_ref = "日本國の辯護士は本當に最高ですよ！"
        s = converter.shinjitai_to_kyujitai("日本国の弁護士は本当に最高ですよ！")
        self.assertEqual(s, kyujitai_ref)

    def test_kyujitai_to_shinjitai(self):
        converter = KyujitaiConverter()
        shinjitai_ref = "この列は東亜連合の旅券のみである。"
        s = converter.kyujitai_to_shinjitai("この列は東亞聯合の旅券のみである。")
        self.assertEqual(s, shinjitai_ref)
