import numpy as np

def sum_date(start, add):
  return np.datetime64(start) + np.timedelta64(add)

def format_date(date):
  stringa = str(date)
  return stringa.replace("-", "")+'0000'