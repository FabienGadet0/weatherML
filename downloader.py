from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
import requests
import csv
import sys
import io
URL = "https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/Archive/synop.{}.csv.gz"


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def to_csv(name, df, append=False):
    if append:
        with open('output.csv', 'a') as f:
            df.to_csv(f, header=False)
    else:
        cr.to_csv("output.csv", sep=',')


if __name__ == "__main__":
    date = datetime(1996, 1, 1)
    goal = datetime(2006, 1, 1)
    cr = pd.DataFrame()
    nb_iterate = diff_month(goal, date)
    dates = [datetime.strftime(date + relativedelta(months=+x), "%Y%m")
             for x in range(0, nb_iterate)]
    print("downloading {} months".format(nb_iterate))
    with open('output.csv', 'a') as f:
        for i, d in enumerate(dates):
            try:
                r = requests.get(URL.format(d)).content.decode('utf-8')
            except requests.exceptions.RequestException as e:
                print(e)
                sys.exit(1)
            cr = cr.append(pd.read_csv(io.StringIO(r), delimiter=';'))
    print("Total length {}".format(len(cr)))
    print("Writing to csv")
