""" Helper functions """

import os


import unicodedata

from typing import List


def strip_accents(text):
    """ Transform latin text into utf-8 """
    text = unicodedata.normalize('NFD', text)\
        .encode('ascii', 'ignore')\
        .decode("utf-8")

    return str(text)


def group_results(results, group_by):
    """ Grou results by an specified key """
    keys = {el.get(group_by) for el in results}
    grouped_results = {}
    for key in keys:
        results_by_key = [el for el in results if el.get(group_by) == key]
        grouped_results[str(key)] = results_by_key

    return grouped_results


def month_number_to_text(month_number: int) -> str:
    """ get month text from number """
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
              'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    return months[month_number - 1]


def format_logros(logros: List[dict]) -> List[dict]:
    """ Format logros """
    logros_formatted = logros

    # Order by year
    for alumno_id, _logros in logros_formatted.items():
        logros_formatted[alumno_id] = sorted(
            _logros, key=lambda x: x['año'], reverse=True)

    return logros_formatted
