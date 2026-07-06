from utils.feature_extractor import extract_features

url = input("Enter URL: ")

features = extract_features(url)

for key, value in features.items():
    print(f"{key}: {value}")