#!/usr/bin/env python3
'''
contains the filter_datum function
'''
import logging
import re
from os import getenv
import mysql.connector as m_c
from typing import List, Tuple

PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    '''
    function to filter out and obfuscate PII data
    '''
    for field in fields:
        message: str = re.sub(f'{field}=.*?{separator}',
                              f'{field}={redaction}{separator}',
                              message)
    return message


def get_logger() -> logging.Logger:
    '''
    returns a loger object
    '''
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> m_c.connection.MySQLConnection:
    '''
    returns a connector to a database
    '''
    host = getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    user = getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = getenv('PERSONAL_DATA_DB_PASSWORD', '')
    database = getenv('PERSONAL_DATA_DB_NAME')
    connection = m_c.connection.MySQLConnection(host=host,
                                                user=user,
                                                password=password,
                                                database=database)
    return connection


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
        '''
        filter values in incoming log records
        '''
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def main():
    '''
    display database querry result in desired format
    '''
    logger = get_logger()

    cnx = get_db()
    cur = cnx.cursor()
    cur.execute('SELECT * FROM users')
    f_names = [i[0] for i in cur.description]
    result = cur.fetchall()

    for row in result:
        formatted_row = ''.join(f'{f}={v}; ' for f, v in zip(f_names, row))
        logger.info(formatted_row.strip())

    cur.close()
    cnx.close()


if __name__ == '__main__':
    main()
