import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import numpy
import pandas as pd


def main():
    plot_using_csv("data/spotify.csv")
    plot_using_csv("data/test1.csv")
    plot_using_csv("data/test2.csv")
    plot_using_csv("data/test3.csv")
    plot_using_csv("data/correlated.csv")
    plot_using_csv("data/uncorrelated.csv")


def plot_using_csv(filename):
   # read csv file
    df = pd.read_csv(filename)

    # filter only incoming packets
    df = df.loc[(df['Destination'] == '10.0.2.15') | (df['Destination'] == '2001:67c:4e8:f004::9')]
    print(df.shape)

    # filter only relevant columns
    df = df[['Time', 'Length']]

    # print the 5 biggest packets
    df_sorted = df.sort_values("Length", ascending=False)
    print(df_sorted.head())

    print(numpy.unique(df["Time"]).size)
    bin_range = (df['Length'].min(), df['Length'].max()) 
    time_interval = 0.01

    # each bin is 5 packets

    plt.hist(df.Time, weights=df.Length, bins=df.shape[0])
    plt.xlabel("Time(Seconds)")
    plt.ylabel("Packet Length")
    plt.title("Traffic for " + filename.split("/")[-1].split(".")[0])
    #plt.show()

    # Save plot to res folder
    plt.savefig("../../res/traffic/" + filename.split("/")[-1].split(".")[0] + ".png")
    plt.close()



def plot_using_txt(filename):
    with open(filename, 'r') as file:
        data = file.readlines()

    data = data[1:]  # remove first line
    data = [row[11:-1] for row in data]  # filter out channel id and \n at end of each line
    data = [row.split()[1::2] for row in data]  # split each row into time and length
    data = [(row[0][:-6], row[1]) for row in data]  # remove time zone (+00:00)

    # convert datetime to int using the first record as start time
    start_time = datetime.strptime(data[0][0], '%H:%M:%S')
    data = [((datetime.strptime(row[0], '%H:%M:%S') - start_time).seconds, int(row[1])) for row in data]

    # convert list to pandas dataframe
    data = pd.DataFrame(data, columns=['Time (Seconds)', 'Packet Length (Bytes)'])
    print(data)

    # plot histogram
    plt.hist(data["Packet Length"])
    plt.show()


if __name__ == '__main__':
    main()
