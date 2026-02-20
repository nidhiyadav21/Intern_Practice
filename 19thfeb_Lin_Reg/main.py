#Importing the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,r2_score,mean_absolute_error


#Load the Dataset and Printing first five rows
df = pd.read_csv("insurance.csv")
print(df.head())


#Printing Number of Rows and Columns
print(df.shape)


#Describing the dataset
print(df.describe())


#Datasets Information
print(df.info())


#Checking the null values.
print(df.isnull().sum())


#Checking Duplicate Values
print("Duplicate rows:",df.duplicated().sum())
df = df.drop_duplicates()
print("Duplicate rows:",df.duplicated().sum())


#Checking Outliers
sns.boxplot(x=df["charges"])
plt.title("Boxplot of charges")
plt.show()


# Based on the boxplot above, charges exceeding $50,000 are rare and act as outliers.
df = df[df['charges'] < 50000]


#Showing boxplot of BMI
sns.boxplot(x=df["bmi"])
plt.show()


#Showing Distribution Charges
sns.histplot(df["charges"],kde=True) #Kde = Kernal Density Estimation
plt.title("Distribution of charges")
plt.show()


#Showing Relationship between age and charges
sns.scatterplot(x="age", y="charges",data=df)
plt.show()


#Showing Relationship between bmi and charges
sns.scatterplot(x="bmi", y="charges",data=df)
plt.show()


#Convert Categorical Variable into Numerical Variables
df = pd.get_dummies(df,drop_first=True)


#Feature Engineering
df['bmi_smoker'] = df['bmi'] * df['smoker_yes']


#Split the target Variable from features
X = df.drop("charges",axis=1)
Y = df["charges"]


#Splitting the dataset
X_train,X_test,y_train,y_test = train_test_split(X,Y,test_size=0.3,random_state=42)
# X_train.shape,y_train.shape,X_test.shape,y_test.shape


# Initializes the linear Regression Model
model = LinearRegression()
model.fit(X_train,y_train)


#shows how much each feature(Age,BMI,etc) affects the price.
coef_df = pd.DataFrame(model.coef_,X.columns,columns=["Coefficient"])
print(coef_df)


#Showing Predicted y
y_pred = model.predict(X_test)
print(y_pred)


#Error Metrics
print("Mean Squared Error:",mean_squared_error(y_test,y_pred))
print("Mean Absolute Error:",mean_absolute_error(y_test,y_pred))
print("Root Mean Squared Error:",np.sqrt(mean_squared_error(y_test,y_pred)))
print("R2 Score:",r2_score(y_test,y_pred))
r2 = r2_score(y_test, y_pred)
# Display as Percentage
print(f"Model Accuracy (R2 Score): {r2 * 100:.2f}%")


#Plotting the graph
plt.scatter(y_test,y_pred)
plt.xlabel("Actual Charges")
plt.ylabel("Predicted Charges")
plt.title("Actual vs Predicted ")
plt.plot([y_test.min(),y_test.max()],[y_test.min(),y_test.max()],color="red")
plt.show()


#Showing the first 10 comparison between Actual vs Prediction
results = pd.DataFrame({
    "Actual": y_test.values,
    "Predicted": y_pred
})
results.head(10)
