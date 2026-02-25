import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report

#Load Dataset
df = pd.read_csv("plant_disease_dataset.csv")
print(df.head())
print(df.describe())
print(df.info())

print(df.isnull().sum())
print("Duplicated Sum:",df.duplicated().sum())


#Check target Column
print(df['disease_present'].value_counts()) #Target Value already in 0/1 form

#



