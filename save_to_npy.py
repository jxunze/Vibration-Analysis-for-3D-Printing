import re
import io
import numpy as np
import pandas as pd

def cache_processed_data(filename):
    with open(filename, 'r') as f:
        contents = f.readlines()
    data_format = "^[+-]?([0-9]+\.?[0-9]*),[+-]?([0-9]+\.?[0-9]*),[+-]?([0-9]+\.?[0-9]*),[+-]?([0-9]+\.?[0-9]*)$"

    start_line = -1

    for i, line in enumerate(contents):
        x = re.match(data_format,line)
        print(x)
        if x:
            start_line = i
            break

    if start_line == -1:
        print("No start line. Ending process.")
        return

    joined_contents = "".join(contents[start_line:])
    data = io.StringIO(joined_contents)
    df = pd.read_csv(data, header = None,delimiter = ',')
    df_acc = df.rename(columns={0: 'Timestamp', 1: 'X', 2: 'Y', 3: 'Z'})
    # df_acc.drop(columns=['_drop'], inplace=True)
    np.save("df.npy", df_acc)