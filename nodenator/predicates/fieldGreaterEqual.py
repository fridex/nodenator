#!/bin/env python


def fieldGreaterEqual(message, key, value):
    try:
        val = reduce(lambda m, k: m[k], key if isinstance(key, list) else [key], message)
        return val >= value
    except:
        return False
