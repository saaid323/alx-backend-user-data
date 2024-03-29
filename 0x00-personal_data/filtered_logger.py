#!/usr/bin/env python3
'''filtered_logger module'''
import os
import re
from typing import List
import logging
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
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', "root")
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    name = os.getenv('PERSONAL_DATA_DB_NAME')
    print(username)
    print(type(PII_FIELDS))
    co = mysql.connector.connect(host=host, port=3306, user=username,
                                 password=password, database=name)
    return co


def main():
    '''function that takes no arguments and returns nothing'''
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    headers = [column[0] for column in cursor.description]
    all = cursor.fetchall()
    data = []
    for i in all:
        for j in range(len(headers)):
            data.append(f'{headers[j]}={i[j]}')
        msg = ';'. join(data)
        data = []
        log_record = logging.LogRecord("user_data", logging.INFO, None, None,
                                       msg, None, None)
        formatter = RedactingFormatter(fields=list(PII_FIELDS))
        print(formatter.format(log_record))


if __name__ == '__main__':
    main()
