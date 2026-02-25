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

#Checking Outliers
features = ['temperature', 'humidity', 'rainfall', 'soil_pH']
plt.figure(figsize=(12, 6))
sns.boxplot(data=df[features])
plt.title("Box Plot for Feature Outliers")
plt.show()

#Capping for Handling Outliers

# Capping Rainfall at 95th percentile
upper_limit = df['rainfall'].quantile(0.95)
df['rainfall'] = df['rainfall'].clip(upper=upper_limit)

#Cap Temperature at 1% and 99%
temp_lower = df['temperature'].quantile(0.01)
temp_upper = df['temperature'].quantile(0.99)
df['temperature'] = df['temperature'].clip(lower=temp_lower, upper=temp_upper)



#Check target Column
print(df['disease_present'].value_counts()) #Target Value already in 0/1 form so no need to Encode.

#Separate Features and Target
X = df.drop('disease_present',axis=1)
y = df['disease_present']

#Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=42)

#Train Decision Tree
model = DecisionTreeClassifier(max_depth=5,random_state=42,class_weight='balanced')
model.fit(X_train,y_train)

#Predictions
y_pred = model.predict(X_test)

#Accuracy Evaluation
print("Accuracy:",accuracy_score(y_test,y_pred)*100)

#Confusion Matrix
cm = confusion_matrix(y_test,y_pred)
sns.heatmap(cm,annot=True,fmt='d')
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

#Classification_Report
print(classification_report(y_test,y_pred))

#Feature importance
importance = model.feature_importances_

feature_imp = pd.Series(importance,index=X.columns)
feature_imp.sort_values().plot(kind='barh')
plt.title("Feature Importance")
plt.show()










