#!/usr/bin/env python3
'''
contains the filter_datum function
'''
import re
from typing import List


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
