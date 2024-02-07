#!/usr/bin/env python3
'''filtered_logger module'''
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    '''returns the log message obfuscated'''
    for i in fields:
        pattern = f'{separator}{i}=.*?{separator}'
        message = re.sub(pattern, f'{separator}{i}={redaction}{separator}',
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        '''method to filter values in incoming log records using
        filter_datum'''
        formater = super(RedactingFormatter, self).format(record)
        m = filter_datum(self.fields, self.REDACTION, formater, self.SEPARATOR)
        return m
