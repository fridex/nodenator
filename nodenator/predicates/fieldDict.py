#!/bin/env python


def fieldDict(message, key):
    try:
        val = reduce(lambda m, k: m[k], key if isinstance(key, list) else [key], message)
        return isinstance(val, dict)
    except:
        return False
