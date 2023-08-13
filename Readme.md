# Network-Final-Project

## 1. Introduction
### 1.1. About the project
The research paper [Practical Traffic Analysis Attacks on Secure Messaging Applications](https://www.researchgate.net/publication/221554707_Correlation_of_Instant_Messaging_Traffic_with_User_Behavior) reveals that it is possible to identify which groups the user belongs to, by analyzing the traffic of instant messaging applications.
It shows how easy it is to use simple statistical methods on the traffic data to identify the user, once achieving ground truth and succeeding to wiretap the user's traffic.

### 1.2. The experiment
The experiment is based on another experiments that were conducted in the research paper mentioned above.
In this experiment we will try to reproduce the results of the research paper and to see if we can get the same results.
The experiment process is based on the following steps:
1. Recording the traffic data in a pcap files of 4 different IM channels in Telegram. Each channel has a different attribute:
   - Images.pcap - Channel that is mainly used for sending images.
   - Video.pcap - Channel that is mainly used for sending videos.
   - Audio.pcap - Channel that is mainly used for sending audio messages.
   - Spotify.pcap - Channel that is mainly used for sending images, while playing spotify music in the background to generate noise in the traffic.
   * We've also another two pcap files that were recorded, one for a user that is a confirmed member in the IM group (correlated) and another for a user that is not a member in the IM group (uncorrelated).
2. Converting the pcap files to csv files, and filtering the data to get only TCP packets that their TCP destination port is 443 (HTTPS).
3. Plotting the data to three different types of graphs:
   - Raw data of the user traffic analysis (packet length in bytes by time in seconds).
   - PDF of delay between packets arrival time.
   - CCDF of message sizes normalized by the maximum message size.

## 2. How to use
### 2.1. Prerequisites
- Python 3.11 or higher
- Windows 10 or higher or Linux Ubuntu 20.04 or higher
- Git
- PIP (Python package manager)
- Wireshark (optional)

### 2.2. Installation
1. Clone the project from GitHub by using the following command:
```git clone https://github.com/Jon400/Network-Final-Project.git```
2. Upgrade pip by running the following command:
```python -m pip install --upgrade pip```
3. Navigate to the project folder and run the following command to install all required packages
```pip install -r requirements.txt```
4. Open jupyter notebook by running the following command:
```jupyter notebook```
5. Open your browser and navigate to your local Jupyter server (usually http://localhost:8888)
6. Open the file ```WetPart.ipynb```
7. Run the notebook by clicking on the ```Run``` button in the toolbar or by pressing ```Shift + Enter```. You can also run the whole notebook by clicking on  ```restart the kernel and run all cells```.

#### Issues during installation
* If you get an error, about jupyter configuration, while running the notebook, run the following command:
```jupyter notebook --generate-config```

### 2.3. Usage
#### Project structure:
- ```WetPart.ipynb``` - Jupiter notebook includes all the code and the results of the traffic analysis. The notebook includes the following main things:
  - Importing the required packages and reading the pcap file as CSV
  - Plotting the raw data of the user traffic analysis (packet length in bytes by time in seconds)
  - Plotting PDF of delay between packets arrival time.
  - Plotting CCDF of message sizes normalized by the maximum message size. There are 4 lines, each line represents a different IM group.
  - Comparing the traffic graphs of a confirmed member (correlated) and a non-member (uncorrelated) in the IM group.
- ```res``` - Folder contains the outcome graphs generated by the notebook.
- ```resources``` - Folder contains the pcap files and the csv files generated from the pcap files.

## 3. Results
### 3.1. The graph of the raw data of the user traffic analysis
If a user belongs to a specific IM group, it is possible to see the distinct pattern embedded in the traffic data.
High peaks in the graph represent the files that were sent in the IM group, and we can use them to identify the user.
It is important to note that the sizes of the peaks and the sizes of the files don't exhibit a strong correlation, because there are unstably factors that affect the network traffic, such as the network condition, the user's device, etc.
### 3.2. The PDF of delay between packets arrival time
The delay between packets arrival time is the time between the arrival of two consecutive packets.
It can be inferred that the delay is negligible, as it behaves similarly for all IM groups.
In addition, the graphs can be successfully fitted to an exponential distribution, as shown in the research paper.
### 3.3. The CCDF of message sizes normalized by the maximum message size
The CCDF of message sizes between images and videos is slightly the same, while the CCDF of audio messages is different.
We conclude that for each message type, we should fit the message sizes model to a different distribution.
### 3.4. Comparing the traffic graphs of a confirmed member (correlated) and a non-member (uncorrelated) in the IM group
It is easy to distinguish between the two users.

**Note:**
When background noise is added, it is more difficult to analyze the traffic data, because the peaks are less distinct and more steady.