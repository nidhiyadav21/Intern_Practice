import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer,make_column_selector
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn import tree


#Main Class
class InsuranceSQLModel:
    def __init__(self,server,database,table_name,test_size=0.3,random_state=42):

        self.server = server
        self.database = database
        self.table_name = table_name
        self.test_size = test_size
        self.random_state = random_state
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.X = None
        self.y = None

        self.conn = None
        self.engine = None
        self.df = None
        self.pipeline = None

    def connect_sql(self):
        """
                Establish a connection to the local SQL Server using SQLAlchemy.
                Uses Windows Authentication (Trusted Connection).
        """
        print("Connecting to SQL Server...")
        self.engine = create_engine("mssql+pyodbc://@localhost/InsuranceDB"
                               "?driver=ODBC+Driver+17+for+SQL+Server"
                               "&trusted_connection=yes")
        print("Connected to SQL Server")

    def load_data(self):
        """
               Execute a SQL query to pull all records from the specified table
               into a Pandas DataFrame.
        """
        print("Loading data...")
        query = f"SELECT * FROM {self.table_name}"
        self.df = pd.read_sql(query,self.engine)
        print(f"Data loaded: {self.df.shape}")
        print("Data Loaded Successfully")

    def preprocess(self):
        """
               Perform exploratory data analysis (EDA) and data cleaning.
               This includes:
               - Separating target (charges) from features.
               - Removing duplicate rows.
               - Splitting data into training and testing sets.
        """

        print("Preprocessing data...")
        self.y = self.df["charges"]
        self.X = self.df.drop("charges",axis=1)

        print("\nPrinting Dataset Information:\n")
        self.df.info()
        print("\nPrinting Dataset Description:\n", self.df.describe())
        print("\nPrinting first 5 rows:\n", self.df.head())
        print("\n Checking null values:\n", self.df.isnull().sum())
        print("\n Checking Duplicate values:\n", self.df.duplicated().sum())
        df = self.df.drop_duplicates()
        print("\nDuplicate rows:", df.duplicated().sum())

        print("Preprocessing completed.")

        #Train-test-Split
        print("Splitting Data...")
        self.X_train,self.X_test,self.y_train,self.y_test = train_test_split(self.X,self.y,test_size=self.test_size,  random_state=self.random_state)
        print("Data Split completed")

    def plot_outliers(self):
        """
               Generate boxplots for all numerical columns in the dataset.
               Helps visualize distribution and identify potential outliers
               in columns like Age, BMI, and Charges.
        """
        print("Generating boxplots for outlier detection...")
        # Select only numeric columns (age, bmi, children, charges)
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns

        # Set up the matplotlib figure
        plt.figure(figsize=(12, 6))

        # Loop through each numeric column and create a subplot
        for i, col in enumerate(numeric_cols, 1):
            plt.subplot(1, len(numeric_cols), i)
            sns.boxplot(y=self.df[col], color='skyblue')
            plt.title(f'Boxplot of {col}')

        plt.tight_layout()
        plt.show()

    def build_pipeline(self):
        """
               Construct a Scikit-Learn pipeline that automates:
               1. One-Hot Encoding for categorical string variables.
               2. Passing through numerical variables.
               3. Initializing the Random Forest Regressor.
        """
        print("Building pipeline...")
        categorical_selector = make_column_selector(dtype_include=[object])
        transformer = make_column_transformer((OneHotEncoder(handle_unknown="ignore"),categorical_selector),remainder="passthrough")
        model = RandomForestRegressor(n_estimators=100,max_depth = 8,min_samples_split=15,min_samples_leaf=5, random_state=self.random_state)
        self.pipeline = make_pipeline(transformer, model)
        print("Pipeline completed")

    def train(self):
        """
                Fit the entire machine learning pipeline on the training data.
                This includes applying the column transformations (encoding)
                and training the Random Forest Regressor.
        """
        print("Training pipeline...")
        self.pipeline.fit(self.X_train,self.y_train)
        print("Training completed")

    def evaluate(self):
        """
                Assess model performance by calculating R2 scores for both
                training and testing sets. Generates a 'Best Fit' scatter plot
                comparing actual vs. predicted values.
        """
        print("Evaluating pipeline...")
        y_train_pred = self.pipeline.predict(self.X_train)
        y_test_pred = self.pipeline.predict(self.X_test)

        train_r2 = r2_score(self.y_train,y_train_pred)
        test_r2 = r2_score(self.y_test,y_test_pred)
        print("\n === MODEL PERFORMANCE ===")
        print(f"Training R2 Score: {train_r2:.4f}")
        print(f"Test R2 Score: {test_r2:.4f}")

        #Plotting Best fit
        plt.figure(figsize=(10, 6))

        # Plotting Actual vs Predicted
        sns.scatterplot(x=self.y_test, y=y_test_pred, alpha=0.6, label="Predicted vs Actual")

        # Plotting the 'Perfect Fit' line
        max_val = max(max(self.y_test), max(y_test_pred))
        min_val = min(min(self.y_test), min(y_test_pred))
        plt.plot([min_val, max_val], [min_val, max_val], color='red', lw=2, linestyle='--', label="Perfect Fit (y=x)")

        plt.title(f"Random Forest Best Fit: Actual vs Predicted Charges\n(Test R2: {test_r2:.4f})")
        plt.xlabel("Actual Charges")
        plt.ylabel("Predicted Charges")
        plt.legend()
        plt.grid(True)
        plt.show()

        #Overfitting Check
        gap = train_r2 - test_r2
        print("Gap score:", gap)
        print("Evaluation completed")
        # return y_test_pred

    def save_to_existing_table(self):
        """
               Clean up the local DataFrame by removing redundant prediction columns,
               calculating final predictions for the entire dataset, and overwriting
               the original SQL table with the updated results.
        """
        print(f"Cleaning columns and updating {self.table_name}...")

        # 1. Generate new predictions
        y_pred_all = self.pipeline.predict(self.X)

        # 2. Identify and REMOVE all unwanted columns from the DataFrame
        # This list includes every variation you've created by mistake
        unwanted_cols = ['y_pred','Predicted_charges']

        # We drop them from the current DataFrame if they exist
        self.df = self.df.drop(columns=[c for c in unwanted_cols if c in self.df.columns])

        # 3. Add back only the ONE column with your final preferred name
        self.df['Predicted_Charges'] = y_pred_all

        # 4. Overwrite the table in SSMS
        # This replaces the old 10-column table with a clean 8-column version
        self.df.to_sql(self.table_name, self.engine, if_exists='replace', index=False)

        print(f"Successfully updated '{self.table_name}'. Extra columns have been removed.")

    def plot_individual_tree(self, tree_index=0, max_depth=3):
        """
               Extract and visualize a single decision tree from the Random Forest.

               Args:
                   tree_index (int): The index of the tree to visualize.
                   max_depth (int): Limit the depth of the plot for better readability.
        """
        print(f"Visualizing Tree #{tree_index} from the Forest...")

        # 1. Get the feature names after OneHotEncoding
        # This ensures the tree labels show 'sex_male' instead of just 'x1_male'
        preprocessor = self.pipeline.named_steps['columntransformer']
        feature_names = preprocessor.get_feature_names_out()

        # 2. Get the specific tree from the RandomForest
        rf_model = self.pipeline.named_steps['randomforestregressor']
        single_tree = rf_model.estimators_[tree_index]

        # 3. Plot
        plt.figure(figsize=(25, 12))
        tree.plot_tree(single_tree,
                       feature_names=feature_names,
                       filled=True,
                       rounded=True,
                       fontsize=10,
                       max_depth=max_depth)

        plt.title(f"Decision Tree #{tree_index} (Max Depth: {max_depth})")
        plt.show()


def main():
    """
        Step-by-step workflow to run the Insurance Prediction Model.
    """
    model = InsuranceSQLModel(server="localhost",database="InsuranceDB",table_name="InsuranceTable")
    model.connect_sql()
    model.load_data()
    model.preprocess()
    model.plot_outliers()
    model.build_pipeline()
    model.train()
    model.evaluate()
    model.save_to_existing_table()
    model.plot_individual_tree()



if __name__ == "__main__":
    main()


