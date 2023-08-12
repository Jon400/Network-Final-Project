import datetime
import time

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import expon



is_in_burst = False
is_burst_detected = False
burst_size = 0
previous_time = 0

def main():
    # generate plot graph with 4 subplots in 2 rows and 2 columns
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('PDF of Inter-message Delay for Different Network Traffic')
    plot_inter_message_delay("data/test1.csv", axs[0, 0])
    plot_inter_message_delay("data/test2.csv", axs[0, 1])
    plot_inter_message_delay("data/test3.csv", axs[1, 0])
    plot_inter_message_delay("data/spotify.csv", axs[1, 1])
    plt.savefig('../../res/inter-message-delays.png')
    

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
        elif is_in_burst == True:
            previous_time = t
            return    

def check_time(time):
    global is_in_burst
    global is_burst_detected
    global burst_size
    THR = 0.5
    if time - previous_time >= THR:
        is_in_burst = False

def plot_inter_message_delay(filename: str, ax: plt.Axes = None):  
    # read csv file
    df = pd.read_csv(filename)

    # filter only incoming packets
    df = df.loc[df['Destination'] == '10.0.2.15']
    print(df.shape)

    # filter only relevant columns
    df = df[['Time', 'Length']]
    print(df)  

    burst_data = [] 

    time = sorted(df['Time'].tolist())
    inter_message_delays = [float(time[i+1] - time[i]) for i in range(len(time)-1)]
    # i = 0
    # while i < len(df):
    #     if_burst(df.iloc[i]['Length'], df.iloc[i]['Time'])
    #     if is_in_burst:
    #         while is_in_burst:
    #             burst_data.append(df.iloc[i])
    #             i += 1
    #             if i >= len(df):
    #                 break
    #             if_burst(df.iloc[i]['Length'], df.iloc[i]['Time'])
    #             check_time(df.iloc[i]['Time'])
    #             if is_in_burst:
    #                 inter_message_delay.append(df.iloc[i]['Time'] - df.iloc[i-1]['Time'])
    #     i+=1

    # plot probability desnsity function of inter-message delay for this burst, x-axis is time, y-axis is PDF
    num_bins = 'auto'  # Use 'auto' to calculate the number of bins based on data distribution
    hist, bin_edges = np.histogram(inter_message_delays, bins=num_bins, density=True)

    # # Normalize the histogram
    bin_width = bin_edges[1] - bin_edges[0]
    pdf = hist * bin_width

    # plot the PDF in step function
    ax.step(bin_edges[:-1], pdf, where='mid', label='Histogram of Inter-message Delay')
    ax.set_xlabel('Inter-message Delay (Seconds)')
    ax.set_ylabel('Probability Density Function (PDF)')
    ax.set_title("PDF of Inter-message Delay for " + filename)
    # fit the exponential distribution according to the data pdf and bin
    fit_params = expon.fit(inter_message_delays)
    fitted_pdf = expon.pdf(bin_edges[:-1], loc=fit_params[0], scale=fit_params[1])
    fitted_pdf = fitted_pdf * bin_width
    # Plot the fitted exponential distribution as a line
    ax.plot(bin_edges[:-1], fitted_pdf, label='Fitted Exponential', color='red')
    ax.grid(True)
    ax.legend()
    # save the plot in res folder
    #plt.savefig('../../res/inter-message-delays/' + filename.split('/')[-1].split('.')[0] + '.png')


            
            


if __name__ == '__main__':
    main()