import pandas as pd
import re

data = pd.read_csv("data/scam_dataset.csv")


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


data["clean_message"] = data["message"].apply(clean_text)

print(data[["message", "clean_message"]].head())