import cPickle as pickle
import bitcoinchart
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

    def save(self, local_path=bitcoinchart.local_histo_archive):
        """save class as self.name.txt"""
        file = open(local_path + 'market.analytics/' + self.name + '.pkl', 'w')
        pickle.dumps(self,file,protocol=2)
        file.close()

    def plot(self):
        left = 0.125  # the left side of the subplots of the figure
        right = 0.9  # the right side of the subplots of the figure
        bottom = 0.1  # the bottom of the subplots of the figure
        top = 0.9  # the top of the subplots of the figure
        wspace = 0.3  # 0.2the amount of width reserved for blank space between subplots
        hspace = 0.6  # 0.5the amount of height reserved for white space between subplots

        plt.close()
        ax = plt.subplot(421)
        ax.set_title('all')
        ax.plot(self.weekday_intraday_curves.get('all'))

        for day in range(7):
            curve = self.weekday_intraday_curves.get(str(day))
            ax = plt.subplot(422 + day)
            ax.set_title(str(day))
            ax.plot(curve)

def load(name, local_path=bitcoinchart.local_histo_archive):
    file = open(local_path + 'market.analytics/' + name + '.pkl', 'r')
 #   dataPickle = file.read()
    data = pickle.load(file)
    file.close()
 #   pickle.loads(dataPickle)
    return data