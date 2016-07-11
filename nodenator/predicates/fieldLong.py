#!/bin/env python


def fieldLong(message, key):
    try:
        val = reduce(lambda m, k: m[k], key if isinstance(key, list) else [key], message)
        return isinstance(val, long)
    except:
        return False
