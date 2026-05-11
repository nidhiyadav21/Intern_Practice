import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.compose import make_column_selector, make_column_transformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import make_pipeline


class SocialNetworkADSModel:
    def __init__(self,file_path,test_size=0.3,random_state=42):
        self.file_path = file_path
        self.test_size = test_size
        self.random_state = random_state
        self.df = None

        self.X = None
        self.Y = None

        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

        self.pipeline = None


    def load_data(self):
        """
               Loads the dataset from the specified file path into a pandas DataFrame.


        """
        try:
            print("Loading data...")
            self.df = pd.read_csv(self.file_path)
            print("\nShape:",self.df.shape)
            print(self.df.head())
            print(f"Loaded Data: {self.df.shape}")
        except FileNotFoundError:
            print(f"Error: The file at {self.file_path} does not exist.")
        except Exception as e:
            print(f"Error: {e}")


    def plot_outliers(self):
        """
               Visualizes outliers using boxplots and caps them using the IQR (Interquartile Range) method.
        """

        self.load_data()
        try:
            print("Plotting outliers...")
            numeric_col = self.df.select_dtypes(include="number")

            for col in numeric_col:
                plt.figure(figsize = (6,4))
                plt.boxplot(self.df[col])
                plt.title(f"Boxplot of {col}")
                plt.xlabel(col)
                plt.grid(True)
                plt.show()

            for col in numeric_col:
                Q1 = self.df[col].quantile(0.25)

                Q3 = self.df[col].quantile(0.75)

                IQR = Q3 - Q1

                lower = Q1 - 1.5*IQR
                upper = Q3 + 1.5*IQR

                self.df[col] = np.where(self.df[col] < lower, upper,self.df[col])
                self.df[col] = np.where(self.df[col] > upper,upper,self.df[col])
        except Exception as e:
            print(f"Error: {e}")


    def preprocess_data(self):
        """
                Handles outlier removal and checks for missing or duplicated values in the dataset.
        """

        self.plot_outliers()

        try:
            print("Preprocessing data...")
            print("\nChecking null values...\n",self.df.isnull().sum())
            print("\nChecking duplicates values...\n",self.df.duplicated().sum())
            print("Preprocessing complete!")
        except Exception as e:
            print(f"Error: {e}")


    def split_data(self):
        """
                Separates features from the target and splits the data into training and testing sets.
        """
        self.preprocess_data()
        try:
            print("Splitting data...")
            self.X = self.df.drop(columns="Purchased")
            self.y = self.df["Purchased"]
            self.X_train,self.X_test,self.y_train,self.y_test = train_test_split(self.X,self.y,test_size=self.test_size,random_state=self.random_state)
            print("Splitting complete!")
        except KeyError:
            print(f"Error:Target column 'Purchase' not found in dataset.")
        except Exception as e:
            print(f"Error: {e}")


    def build_pipeline(self):
        """
                Creates a Scikit-Learn pipeline consisting of a ColumnTransformer
                (scaling/encoding).
        """

        self.split_data()
        try:
            cat_selector = make_column_selector(dtype_include= [object])
            num_selector = make_column_selector(dtype_include= [np.number])

            transformer = make_column_transformer(
                (OneHotEncoder(handle_unknown='ignore'),cat_selector),
                (StandardScaler(),num_selector),
            remainder = "passthrough"
            )

            rf_model = LogisticRegression()
            self.pipeline = make_pipeline(transformer, rf_model)
            print("Pipeline Created!")
        except Exception as e:
            print(f"Error: {e}")


    def train_data(self):
        """
               Fits the established pipeline onto the training data.
        """
        self.build_pipeline()
        try:
            print("Training data...")
            self.pipeline.fit(self.X_train,self.y_train)
            print("Training Completed")
        except Exception as e:
            print(f"Error: {e}")


    def evaluate_model(self):
        """
               Predicts test labels and outputs evaluation metrics, including accuracy
               scores and a confusion matrix heatmap.
        """
        self.train_data()
        try:
            print("Evaluating model...")

            train_pred = self.pipeline.predict(self.X_train)
            y_pred = self.pipeline.predict(self.X_test)

            test_probs = self.pipeline.predict_proba(self.X_test)
            accuracy = accuracy_score(self.y_test,y_pred)
            train_acc = accuracy_score(self.y_train,train_pred)
            print(f"Accuracy: {accuracy:.4f}")
            print(f"Train Accuracy: {train_acc:.4f}")
            cm = confusion_matrix(self.y_test,y_pred)
            plt.figure(figsize = (6,4))
            sns.heatmap(cm, annot=True, fmt="g",cmap="YlOrRd"
                       )

            plt.title("Confusion Matrix")
            plt.show()
        except Exception as e:
            print(f"Error: {e}")

def main():
    DATA_PATH = "Social_Network_Ads.csv"

    model = SocialNetworkADSModel(DATA_PATH)
    model.evaluate_model()

if __name__ == "__main__":
    main()
