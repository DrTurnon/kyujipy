# kyujipy

[![PyPI version](https://badge.fury.io/py/kyujipy.svg)](https://badge.fury.io/py/kyujipy)

[kyujipy](https://github.com/DrTurnon/kyujipy) is a  Python library to convert Japanese texts from
[Shinjitai](https://en.wikipedia.org/wiki/Shinjitai) (新字体) to
[Kyūjitai](https://en.wikipedia.org/wiki/Ky%C5%ABjitai), (舊字體) and vice versa.

[kyujipy](https://github.com/DrTurnon/kyujipy) is based on the
[kyujitai.js](https://github.com/hakatashi/kyujitai.js) project, originally authored by
[Koki Takahashi](https://github.com/hakatashi).


## Installation (via [Pip](http://www.pip-installer.org/))

    $ pip install kyujipy


## Usage

In Python shell (or inside Python script):

    
    # Import main class
    >>> from kyujipy import KyujitaiConverter
    
    # Instantiate Shinjitai <-> Kyujitai converter
    >>> converter = KyujitaiConverter()
    
    # Convert a text from Shinjitai to Kyujitai
    >>> print(converter.shinjitai_to_kyujitai("新字体"))
    新字體
    
    # Convert a text from Kyujitai to Shinjitai
    >>> print(converter.kyujitai_to_shinjitai("舊字體"))
    旧字体


## API Reference

* __shinjitai_to_kyujitai(string)__

Convert a text from Shinjitai (新字体) to Kyūjitai (舊字體)

* __kyujitai_to_shinjitai(string)__

Convert a text from Kyūjitai (舊字體) to Shinjitai (新字体)


## License

[kyujipy](https://github.com/DrTurnon/kyujipy) is licensed under the MIT license.

© 2017-2025 [Emmanuel Ternon](https://github.com/DrTurnon)
