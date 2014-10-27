# -*- coding:utf-8 -*-
import unicodedata


def encode_str(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
