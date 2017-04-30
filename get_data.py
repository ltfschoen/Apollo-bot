import pandas as pd
import requests

class Data:
    """ Load DATA """
    def __init__(self, location, time):

        self.DATASET_REMOTE = "https://firms.modaps.eosdis.nasa.gov/active_fire/c6/text/MODIS_C6_{0}_{1}h.csv".format(location, time)
        self.dataset = self.get_data(None)

    def get_data(self, num_rows):
        """ Load from remote endpoint """
        try:
            def exists(path):
                r = requests.head(path)
                return r.status_code == requests.codes.ok
            if exists(self.DATASET_REMOTE):
                return pd.read_csv(self.DATASET_REMOTE, nrows=num_rows)
        except Exception as e:
            print(e.errno)

# data = Data("Global", "24")
# print(data.dataset)