from chardet import UniversalDetector
import pandas as pd
import os


def check_encoding(file_path):
    detector = UniversalDetector()
    for line in file_path:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result['encoding']

def open_file_as_df(file):
    extension = os.path.splitext(file)[1]

    if extension == ".csv":
        df = pd.read_csv(file, header=None, dtype=str, na_filter=False)
    else:
        df = pd.read_table(file, header=None, dtype=str, na_filter=False)

    return df