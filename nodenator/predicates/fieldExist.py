#!/bin/env python


def fieldExist(message, key):
    try:
        reduce(lambda m, k: m[k], key if isinstance(key, list) else [key], message)
        return True
    except:
        return False
