#!/bin/env python


def fieldContain(message, key, value):
    try:
        val = reduce(lambda m, k: m[k], key if isinstance(key, list) else [key], message)
        return value in val
    except:
        return False
