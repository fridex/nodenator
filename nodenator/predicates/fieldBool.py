#!/bin/env python


def fieldBool(message, key):
    try:
        val = reduce(lambda m, k: m[k], key if isinstance(key, list) else [key], message)
        return isinstance(val, bool)
    except:
        return False
