"""
House Price Prediction using Decision Tree Regressor.

This script:
- Loads housing data
- Preprocesses features (Handling missing values and ID removal)
- Encodes categorical variables using a Pipeline
- Trains a Decision Tree Regressor
- Evaluates performance using MAE, MSE, and R2 Score
"""

#Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

#Main MODEL CLASS
class HousePriceModel:
    def __init__(self,file_path,test_size=0.3,random_state=42):

      #Store basic configuration
      self.file_path = file_path
      self.test_size = test_size
      self.random_state = random_state
      #self.model = DecisionTreeRegressor(max_depth=10,random_state=42)

      #Data containers
      self.df = None
      self.X = None
      self.y = None

      #Train-Test Split
      self.X_train = None
      self.X_test = None
      self.y_train = None
      self.y_test = None

      #ML pipeline
      self.pipeline = None

      #LOAD DATA
    def load_data(self):
        self.df = pd.read_csv(self.file_path)
        print(f"\nData Loaded: {self.df.shape}")
        print("\nPrinting first five rows:\n",self.df.head())
        print("\nDescribing Dataset:\n",self.df.describe())
        print("\nDataSet Information:\n",self.df.info())
        print("\nChecking Null Values:\n",self.df.isnull().sum())
        print("\nChecking Duplicate Values\n",self.df.duplicated().sum())


    # PLOT OUTLIERS
    def plot_outliers(self):
        """
        Visualize outliers using boxplots for all numerical features.
        """
        print("[INFO] Generating boxplots to check for outliers...")

        # Select only numerical columns
        numeric_cols = self.df.select_dtypes(include=['number']).columns

        # Calculate number of plots needed
        num_cols = len(numeric_cols)

        # Create a figure with subplots (1 row, many columns)
        fig, axes = plt.subplots(1, num_cols, figsize=(4 * num_cols, 6))

        # Handle case where there is only 1 numeric column
        if num_cols == 1:
            axes = [axes]

        # Loop through columns and create boxplots
        for i, col in enumerate(numeric_cols):
            self.df.boxplot(column=col, ax=axes[i],widths=0.2, grid=False)
            axes[i].set_title(f"Outliers in {col}", fontsize=10)
            axes[i].set_ylabel("Value")

        plt.tight_layout()
        print("[INFO] Displaying boxplots. Close the window to continue...")
        plt.show()

     #PREPROCESS DATA
    def preprocess_data(self):
        self.y = self.df['price']
        self.X = self.df.drop(["price","ID"], axis=1, errors='ignore')

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=self.test_size, random_state=self.random_state)


     #Build Pipeline
    def build_pipeline(self):
        transformer = make_column_transformer(
            (SimpleImputer(strategy='mean'), make_column_selector(dtype_include='number')),
            (make_pipeline(
                SimpleImputer(strategy='constant', fill_value='na'),
                OneHotEncoder(handle_unknown='ignore')
            ), make_column_selector(dtype_include=object)),
            remainder='passthrough'
        )

        # 2. Define the model
        dt_model = DecisionTreeRegressor(
            max_depth=10,
            random_state=self.random_state
        )

        # 3. Combine into one pipeline
        self.pipeline = make_pipeline(
            transformer,
            dt_model
        )

        print("Pipeline created.")


      #Train Model
    def train_model(self):
        self.pipeline.fit(self.X_train,self.y_train)
        print(f"Model Training Done")


    #Evaluate Model
    def evaluate_model(self):
        y_pred = self.pipeline.predict(self.X_test)
        mse = mean_squared_error(self.y_test,y_pred)
        mae = mean_absolute_error(self.y_test,y_pred)
        r2 = r2_score(self.y_test,y_pred)

        #Print Results
        print("\n========== MODEL PERFORMANCE ==========")
        print(f"Mean Absolute Error (MAE) : {mae:.2f}")
        print(f"Mean Squared Error (MSE)  : {mse:.2f}")
        print(f"R-Squared (R2 Score)      : {r2:.4f}")
        print("=======================================\n")

        return y_pred

#Main Function
def main():

        #Dataset path
        DATA_PATH = "Cleaned_data_for_model.csv"

        #initialize model object
        model = HousePriceModel(DATA_PATH)

        #Execute pipeline steps
        model.load_data()
        model.plot_outliers()
        model.preprocess_data()
        model.build_pipeline()
        model.train_model()
        model.evaluate_model()


#Program Entry Point
if __name__ == "__main__":
        main()







