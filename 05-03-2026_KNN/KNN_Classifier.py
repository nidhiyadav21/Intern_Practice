import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import pickle  #Used to save your trained model to a file.


class SocialNetworkAds:
    """
            Initializes the SocialNetworkAds class with dataset and model configurations.

            Args:
                file_path (str): Path to the CSV dataset.
                test_size (float): Proportion of the dataset to include in the test split.
                random_state (int): Controls the shuffling applied to the data before splitting.
                neighbors (int): Default number of neighbors for the KNN model.
    """
    def __init__(self, file_path, test_size=0.3, random_state=42, neighbors=10):
        self.file_path = file_path
        self.test_size = test_size
        self.random_state = random_state
        self.neighbors = neighbors

        self.df = None
        self.X_train, self.X_test, self.y_train, self.y_test = [None] * 4
        self.pipeline = None

    def load_data(self):
        """
                Loads the dataset from the CSV file and prints the dataframe shape.
        """
        print("Loading data...")
        self.df = pd.read_csv(self.file_path)
        print(f"Data loaded: {self.df.shape}")

    def plot_outliers(self):
        """
               Generates boxplots for numerical features to visualize potential outliers.
        """
        numeric_cols = ['Age', 'EstimatedSalary']
        plt.figure(figsize=(12, 5))
        for i, col in enumerate(numeric_cols, 1):  #enumerate gives us both the column name (col) and a counter (i) starting at 1.
            plt.subplot(1, 2, i)    #Divides the figure into a grid with 1 row and 2 columns. The i tells the code to draw the next plot in the position (either position 1 or 2).
            sns.boxplot(y=self.df[col], color='blue')
            plt.title(f'Outlier Detection: {col}')
        plt.tight_layout()        #Automatically adjusts the spacing between the two charts so the labels and titles don't overlap.
        plt.show()

    def preprocess_data(self):
        """
               Cleans the data by dropping unnecessary columns, handling duplicates,
               and splitting the data into training and testing sets.
        """
        print("Preprocessing data...")
        if 'User ID' in self.df.columns:
            self.df = self.df.drop(columns=['User ID'])

        print("\nChecking null values:\n", self.df.isnull().sum())
        print("\nChecking duplicates:", self.df.duplicated().sum())
        self.df = self.df.drop_duplicates(keep='first')

        self.X = self.df.drop(columns="Purchased")
        self.y = self.df["Purchased"]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=self.test_size, random_state=self.random_state
        )


    def build_pipeline(self):
        """
                Constructs a Scikit-Learn pipeline consisting of a ColumnTransformer
                (scaling/encoding) and a KNN Classifier.
        """
        print(f"\nBuilding pipeline with K={self.neighbors}...")
        cat_selector = make_column_selector(dtype_include=[object])
        # Note: Fixed dtype_include to np.number for proper scaling
        num_selector = make_column_selector(dtype_include=[np.number])

        transformer = make_column_transformer(
            (OneHotEncoder(handle_unknown='ignore'), cat_selector),
            (StandardScaler(), num_selector),
            remainder="passthrough"
        )

        knn_model = KNeighborsClassifier()
        self.pipeline = make_pipeline(transformer, knn_model)

    def run_grid_search(self):
        """
                Performs hyperparameter tuning using GridSearchCV to find the optimal KNN parameters.
                Updates self.pipeline with the best-performing estimator.
        """
        print("\n[INFO] Starting GridSearchCV to find the best model configuration...")

        # Re-use existing pipeline logic
        self.build_pipeline()

        # Define the parameter grid
        # Note: 'kneighborsclassifier' is the default name from make_pipeline
        param_grid = {
            'kneighborsclassifier__n_neighbors': range(1, 21),
            'kneighborsclassifier__weights': ['uniform', 'distance'],
            'kneighborsclassifier__metric': ['euclidean', 'manhattan'],
            'kneighborsclassifier__p': [1, 2]
        }

        # Run Grid Search
        grid = GridSearchCV(self.pipeline, param_grid, cv=5, scoring='accuracy', n_jobs=2)
        grid.fit(self.X_train, self.y_train)

        # Store results
        self.pipeline = grid.best_estimator_
        self.best_params = grid.best_params_

        print(f"Best Score (CV): {grid.best_score_:.4f}")
        print(f"Best Parameters: {self.best_params}")

    def train_pipeline(self):
        """
                Fits the current pipeline to the training data (X_train, y_train).
        """
        print("Training pipeline...")
        self.pipeline.fit(self.X_train, self.y_train)
        print("Training complete!")

    def evaluate_pipeline(self):
        """
                Evaluates the model on the test set. Prints accuracy and classification
                reports, and displays a confusion matrix heatmap.
        """
        print("\nEvaluating pipeline...")
        y_pred = self.pipeline.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)

        print(f"Final Accuracy: {accuracy:.4f}")
        print("\nClassification Report:\n", classification_report(self.y_test, y_pred))

        cm = confusion_matrix(self.y_test, y_pred)
        plt.figure(figsize=(6, 4))
        sns.heatmap(cm, annot=True, fmt="g", cmap="Blues",
                    xticklabels=['Not Purchased', 'Purchased'],
                    yticklabels=['Not Purchased', 'Purchased'])
        plt.title(f'Confusion Matrix (K={self.neighbors})')
        plt.show()

    def save_model(self, filename="knn_pipeline.pkl"):
        """
                Serializes and saves the trained pipeline to a file using pickle.

                Args:
                    filename (str): The name of the file to save the model to.
        """
        with open(filename, "wb") as f:  #wb stands for "Write Binary."
            pickle.dump(self.pipeline, f)
        print(f"Model saved to: {filename}")


def main():
    """
        Executes the full machine learning workflow for the Social Network Ads dataset.

        This function serves as the script's entry point, orchestrating the following steps:
        1. Initializing the model class with the data path.
        2. Loading and cleaning the data.
        3. Visualizing potential outliers.
        4. Building and tuning the KNN model via Grid Search.
        5. Training the optimized model on the training set.
        6. Evaluating performance on the test set and visualizing results.
        7. Saving the final pipeline for deployment.
        """
    DATA_PATH = "Social_Network_Ads.csv"
    model = SocialNetworkAds(DATA_PATH)

    model.load_data()
    model.plot_outliers()
    model.preprocess_data()
    model.build_pipeline()
    model.run_grid_search()
    model.train_pipeline()
    model.evaluate_pipeline()
    model.save_model()


if __name__ == "__main__":
    main()











