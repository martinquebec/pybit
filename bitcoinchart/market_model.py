import cPickle as pickle
import histo
from matplotlib import pyplot as plt

class MarketAnalytics(object):
    """A class that encapslulate all the analytics for one market:

    Attributes:
        name: Market name
        weekday adj: adjutment for day of the weee
        predicted volume curve for each day of the week
    """

    def __init__(self, name, weekday_adj, predicted_volume, weekday_intraday_curves):
        """Return a market analytics object with the proper calibration data"""
        self.name =name
        self.weekday_adj = weekday_adj
        self.predicted_volume = predicted_volume
        self.weekday_intraday_curves = weekday_intraday_curves

  #  def __init__(self,name,local_path=histo.local_histo_archive):
  #      self.load(name,local_path=local_path)

    def save(self,local_path=histo.local_histo_archive):
        """save class as self.name.txt"""
        file = open(local_path + 'market.analytics/' + self.name + '.pkl', 'w')
        pickle.dumps(self,file,protocol=2)
        file.close()

    def plot(self):
        plt.close()
        ax = plt.subplot(421)
        ax.set_title('all')
        ax.plot(self.weekday_intraday_curves.get('all'))

        for day in range(7):
            curve = self.weekday_intraday_curves.get(str(day))
            ax = plt.subplot(422 + day)
            ax.set_title(str(day))
            ax.plot(curve)

def load(name,local_path=histo.local_histo_archive):
    file = open(local_path + 'market.analytics/' + name + '.pkl', 'r')
 #   dataPickle = file.read()
    data = pickle.load(file)
    file.close()
 #   pickle.loads(dataPickle)
    return data