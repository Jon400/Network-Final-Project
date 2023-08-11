

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


is_in_burst = False
is_burst_detected = False
burst_size = 0
previous_time = 0

def main():
    plot_message_sizes("data/test1.csv")
    plot_message_sizes("data/test2.csv")
    plot_message_sizes("data/test3.csv")
    plot_message_sizes("data/test5.csv")
    

def if_burst(length, t):
    global is_in_burst
    global previous_time
    global burst_size
    if length > 1000:
        # if length == 1514:
        # 	burst_size += length
        if is_in_burst == False:
            # delay = abs(np.random.laplace(MU, SIGMA))
            # print ("delay is ",delay)
            # time.sleep(delay)
            is_in_burst = True
            previous_time = t
        elif is_in_burst == False:
            return    

def check_time(time):
    global is_in_burst
    global is_burst_detected
    global burst_size
    THR = 0.5
    if time - previous_time >= THR:
        is_in_burst = False
        is_burst_detected = True

def plot_message_sizes(filename: str):
    # read csv file
    df = pd.read_csv(filename)

    # filter only incoming packets
    df = df.loc[df['Destination'] == '10.0.2.15']

    # filter only relevant columns
    df = df[['Time', 'Length']]

    # Find the maximum packet length for normalization
    max_length = df['Length'].max()

    # Normalize the packet lengths
    df['Normalized Length'] = df['Length'] / max_length

    burst_data = []
    i = 0
    while i < len(df):
        if_burst(df.iloc[i]['Length'], df.iloc[i]['Time'])
        if is_in_burst:
            while is_in_burst:
                burst_data.append(df.iloc[i])
                i += 1
                if i >= len(df):
                    break
                check_time(df.iloc[i]['Time'])
        i += 1

    burst_data = pd.DataFrame(burst_data)

    # plot Complementary Cumulative Distribution Function (CDF) of message sizes
    counts, bin_edges = np.histogram(burst_data['Normalized Length'], bins=1000, density=True)
    ccdf = 1 - np.cumsum(counts) / np.sum(counts)
    # plot in log scale of y-axis
    #plt.yscale('log')
    plt.plot(bin_edges[1:], ccdf)
    plt.xlabel("Normalized Packet Length to their maximum value")
    plt.ylabel("CCDF")
    plt.title(filename)
    plt.grid(which='both', linestyle='-', linewidth=0.5)
    plt.show()


if __name__ == "__main__":
    main()
    