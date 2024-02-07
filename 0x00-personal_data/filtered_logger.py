#!/usr/bin/env python3
'''filtered_logger module'''
import re


def filter_datum(fields, redaction, message, separator):
    '''returns the log message obfuscated'''
    for i in fields:
        pattern = f'{separator}{i}=.*?{separator}'
        message = re.sub(pattern, f'{separator}{i}={redaction}{separator}', message)
    return message
