import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score,roc_curve
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
# from imblearn.over_smote import SMOTE

df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")
print("Shape:",df.shape)
print(df.head())
print(df.info())
print(df.describe())
print(df.isnull().sum())


#PERFORMING EDA

#Attrition distribution
sns.countplot(x ="Attrition",data=df)
plt.title("Distribution of Attrition")
plt.show()

#Age vs Attrition
sns.boxplot(x="Attrition",y="Age",data=df)
plt.title("Comparison of Age vs Attrition")
plt.show()

#Monthly Income vs Attrition
sns.boxplot(x="Attrition",y="MonthlyIncome",data=df)
plt.title("Comparison of Monthly Income vs Attrition")
plt.show()

df['MonthlyIncome'] = np.log(df['MonthlyIncome'])


#Correlation Heatmap
plt.figure(figsize=(15,10))
#sns.heatmap(df.corr(),annot=True,cmap="coolwarm")
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()


#Convert target
df["Attrition"] = df["Attrition"].map({"Yes": 1, "No": 0})

#PERFORMING PREPROCESSING

#Drop Unnecessary Columns
df = df.drop(['EmployeeCount','Over18','StandardHours','EmployeeNumber'],axis=1)

#Encode Categorical Columns
categorical_cols = df.select_dtypes(include=["object", "string"]).columns
le = LabelEncoder()
for col in categorical_cols:
    df[col] = le.fit_transform(df[col])


#Split data
X = df.drop('Attrition',axis=1)
y = df['Attrition']
print(y.value_counts())
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)


#Feature Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


#Logistic Regression model
model = LogisticRegression(max_iter=1000,class_weight='balanced')
model.fit(X_train,y_train)
y_pred = model.predict(X_test)
print(y_pred.shape)

print("Accuracy:",accuracy_score(y_test,y_pred))

#Confusion matrix
cm = confusion_matrix(y_test,y_pred)
sns.heatmap(cm, annot=True,fmt='d',cmap="Blues")
plt.title("Confusion Matrix")
plt.ylabel("Actual Value")
plt.xlabel("Predicted Value")
plt.show()



#Classification Report
print(classification_report(y_test,y_pred))


# Get the coefficients from your trained model
importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.coef_[0]
}).sort_values(by='Importance', ascending=False)

# Show the Top 5 reasons people LEAVE (Positive values)
print("Top Reasons for Attrition:")
print(importance.head(5))

# Show the Top 5 reasons people STAY (Negative values)
print("\nTop Reasons for Staying:")
print(importance.tail(5))


#ROC CURVE
y_prob = model.predict_proba(X_test)[:,1]
fpr,tpr,thresholds = roc_curve(y_test,y_prob)
plt.plot(fpr,tpr)
plt.plot([0,1],[0,1])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.show()
print("ROC-AUC Score:",roc_auc_score(y_test,y_prob))









