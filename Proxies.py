import pandas as pd
import numpy as np
def Proxy_splitter(n):
    ser = pd.read_csv("proxies.csv", header=None)
    Proxy_list = np.array_split(ser,n)
    return Proxy_list
