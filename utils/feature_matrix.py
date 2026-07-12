import pandas as pd

from utils.feature_extractor import extract_features


def build_feature_dataframe(urls):

    features = []

    for url in urls:
        features.append(extract_features(url))

    return pd.DataFrame(features)