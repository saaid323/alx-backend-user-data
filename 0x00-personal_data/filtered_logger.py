#!/usr/bin/env python3
'''filtered_logger module'''
import re
from typing import List


def filter_datum(fields: List, redaction: str, message: str,
                 separator: str) -> str:
    '''returns the log message obfuscated'''
    for i in fields:
        message = re.sub(f'{separator}{i}=.*?{separator}',
                         f'{separator}{i}={redaction}{separator}', message)
    return message
