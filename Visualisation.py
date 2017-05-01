import requests
import pandas as pd
# import numpy as np
# import seaborn as sns
# import scipy.ndimage
# from scipy import stats
# import Tkinter as tk # Python 2
# import tkinter as tk # Python 3
# import matplotlib
# matplotlib.use('Agg') # Set Matplotlib backend to use Agg instead of Tk for use on Heroku
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

class Data:
    """ Load DATA """

    def __init__(self, location, time):

        self.DATASET_REMOTE = "https://firms.modaps.eosdis.nasa.gov/active_fire/c6/text/MODIS_C6_{0}_{1}h.csv".format(
            location, time)
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
            print("Exception retrieving data: ", e)

    # def graph(self, location = "Global", time = "24", filename = "output.png"):
    #     data = Data(location, time)
    #     feature_columns = ['latitude', 'longitude', 'brightness']
    #     X  = data.get_data(100)[feature_columns]
    #     # X.head()
    #     sns.set()
    #
    #     mu, sigma = 0, 0.1
    #     x = X['latitude']
    #     y = X['longitude']
    #     z = X['brightness']
    #
    #     xyz = np.vstack([x,y,z])
    #     density = stats.gaussian_kde(xyz)(xyz)
    #
    #     idx = density.argsort()
    #     x, y, z, density = x[idx], y[idx], z[idx], density[idx]
    #
    #     fig = plt.figure(frameon=False)
    #     ax = fig.add_subplot(111, projection='3d')
    #     ax.scatter(x, y, z, c=density)
    #     ax.set(xlabel='Latitude', ylabel='Longitude', zlabel='Brightness')
    #     ax.set_title("MODIS Satellite Global Fire Distribution [24 Hours]", fontsize=15)
    #     plt.show()
    #     fig.savefig(filename)

d = Data("Global", "24")
# print(d.dataset)
# d.graph()




