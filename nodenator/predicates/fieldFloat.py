#!/bin/env python


def fieldFloat(message, key):
    try:
        val = reduce(lambda m, k: m[k], key if isinstance(key, list) else [key], message)
        return isinstance(val, float)
    except:
        return False

