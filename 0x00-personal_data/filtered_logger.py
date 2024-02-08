#!/usr/bin/env python3
'''filtered_logger module'''
import re
from typing import List
import logging
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


def get_logger() -> logging.Logger:
    '''get_logger method'''
    logger = logging.getLogger('user_data')
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''get_db function'''
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    name = os.getenv('PERSONAL_DATA_DB_NAME')
    co = mysql.connector.connect(host=host, user=username,
                                 password=password, database=name)
    return co


def main() -> None:
    '''main function'''
    db = get_db()
    cursor = db.cursor()
    formatter = RedactingFormatter(fields=("email", "ssn", "password"))
    cursor.execute("SELECT name, email, phone, ssn, password, ip, last_login, user_agent
                   FROM users
                   ")
    for i in cursor:
        RedactingFormatter(fields=(PII_FIELDS))
        print(formatter.format(i))


if __name__ == '__main__':
    main()
