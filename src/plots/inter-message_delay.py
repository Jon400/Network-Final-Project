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
    plot_inter_message_delay("data/test1.csv")
    plot_inter_message_delay("data/test2.csv")
    plot_inter_message_delay("data/test3.csv")
    plot_inter_message_delay("data/test5.csv")
    

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

def plot_inter_message_delay(filename: str):  
    # read csv file
    df = pd.read_csv(filename)

    # filter only incoming packets
    df = df.loc[df['Destination'] == '10.0.2.15']
    print(df.shape)

    # filter only relevant columns
    df = df[['Time', 'Length']]
    print(df)  

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
        i+=1

    # plot probability desnsity function of inter-message delay for this burst, x-axis is time, y-axis is PDF
    # for example if the busrst is 1, 10, 20, 30, 40, 100, 200, 500, 1000
    # then the inter-message delay is 9, 10, 10, 10, 60, 100, 300, 500
    # so the pdf is 1/9, 3/9, 3/9, 3/9, 1/9, 1/9, 1/9, 1/9, 1/9
    # so the x-axis is 9, 10, 60, 100, 300, 500, 1000

    burst_times = [row['Time'] for row in burst_data]
    burst_times.sort()
    inter_message_delay = [(burst_times[j+1] - burst_times[j]) for j in range(len(burst_times) - 1)]
    inter_message_delay = [delay for delay in inter_message_delay if delay <= 0.5]
    num_bins = 'auto'  # Use 'auto' to calculate the number of bins based on data distribution
    hist, bin_edges = np.histogram(inter_message_delay, bins=num_bins, density=True)

    # # Normalize the histogram
    bin_width = bin_edges[1] - bin_edges[0]
    pdf = hist * bin_width
    #pdf = pdf / pdf.sum()  # Normalize the histogram

    # plot the PDF in step function
    plt.step(bin_edges[:-1], pdf, where='post', label='Histogram of Inter-message Delay')
    plt.xlabel('Inter-message Delay (Seconds)')
    plt.ylabel('Probability Density Function (PDF)')
    plt.title('PDF of Inter-message Delay')
    # fit the exponential distribution according to the data pdf and bin
    
    fit_params = expon.fit(inter_message_delay)
    fitted_pdf = expon.pdf(bin_edges[:-1], loc=fit_params[0], scale=fit_params[1])
    fitted_pdf = fitted_pdf * bin_width
    # Calculate bin widths
    # bin_widths = np.diff(bin_edges)
    # # Normalize the fitted PDF to match the area of the histogram (area under the PDF = 1)
    # area_under_pdf = np.sum(bin_widths * fitted_pdf)
    # normalized_fitted_pdf = fitted_pdf / area_under_pdf
    #fitted_pdf = fitted_pdf / fitted_pdf.sum()
    # Plot the fitted exponential distribution as a line
    plt.plot(bin_edges[:-1], fitted_pdf, label='Fitted Exponential', color='red')
    plt.grid(True)
    plt.legend()
    plt.show()


            
            


if __name__ == '__main__':
    main()