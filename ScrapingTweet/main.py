from function import manageJson, tweetRequest
from function.funzioni_date import *

end_date = np.datetime64('2019-07-25')
start_date = sum_date(end_date, -90)
try:
    while start_date >= np.datetime64('2018-01-01'):
        if start_date >= end_date:
            raise ValueError("start_time must be before end_time")
        end_date = sum_date(start_date, +90)
        n_files = tweetRequest.fun(format_date(start_date), format_date(end_date))
        for n_file in n_files:
            manageJson.manage(f'{n_file}')
        start_date = sum_date(start_date, -90)
except ValueError as e:
    print(e)
