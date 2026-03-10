import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.compose import  make_column_selector, make_column_transformer
from sklearn.metrics import silhouette_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.decomposition import PCA

class CustomerSegmentation:
    """
       A class to perform end-to-end Customer Segmentation using K-Means clustering.
       Includes data loading, preprocessing, pipeline building, and visualization.
    """
    def __init__(self,file_path,test_size = 0.3,random_state=42):
        """
                Initializes the CustomerSegmentation class with file path and model parameters.

                Args:
                    file_path (str): Path to the CSV dataset.
                    test_size (float): Proportion of the dataset to include in the test split.
                    random_state (int): Seed used by the random number generator for reproducibility.
        """
        self.file_path = file_path
        self.test_size = test_size
        self.random_state = random_state

        self.df = None

        self.X = None
        self.y = None

        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

        self.pipeline = None

    def load_data(self):
        """
                Loads the dataset from the specified CSV file path and prints basic summary statistics.
        """
        try:
            print("Loading data...")
            self.df = pd.read_csv(self.file_path)
            print("\nPrinting first five rows:\n",self.df.head())
            print("\nDataset Information:\n")
            self.df.info()
            print("\nDescribing Dataset:\n",self.df.describe())
            print(f"Data loaded: {self.df.shape}")
        except FileNotFoundError:
            print(f"Error:The file at {self.file_path} was not found.")
        except Exception as e:
            print(f"An unexcepted error occured while loading data: {e} ")



    def plot_outliers(self):
        """
                Generates boxplots for all numeric columns in the dataset to identify potential outliers.
        """

        self.load_data()
        try:
            print("Plotting outliers...")
            # Select numeric columns
            numeric_col_list = self.df.select_dtypes(include=[np.number]).columns

            for col_name in numeric_col_list:
                # We use .copy().dropna() to ensure we have a clean Series of numbers
                clean_series = self.df[col_name].dropna()

                # Check if the series has any data points to plot
                if len(clean_series) > 0:
                    plt.figure(figsize=(6, 4))
                    plt.boxplot(clean_series)
                    plt.title(f"Boxplot of {col_name}")
                    plt.xlabel(col_name)
                    plt.grid(True)
                    plt.show()
                else:
                    print(f"Skipping {col_name}: No numeric data found.")
            print("Plotting Completed")
        except Exception as e:
            print(f"An unexcepted error occured while plotting data: {e} ")


    def preprocess_data(self):
            """
                Cleans the data by capping outliers, dropping irrelevant columns,
                mapping ordinal values, and filling missing values.
            """
            self.plot_outliers()
            try:
                print("Preprocessing data...")
                # Capping outliers to the 99th percentile
                for col in ['Work_Experience', 'Family_Size']:
                    upper_limit = self.df[col].quantile(0.99)
                    self.df[col] = np.where(self.df[col] > upper_limit, upper_limit, self.df[col])

                self.df.drop(columns=['ID', 'Profession', 'Var_1'], inplace=True, errors='ignore')

                # 1. Map Ordinal Features (CRITICAL for K-Means)
                res_map = {'Low': 1, 'Average': 2, 'High': 3}
                if 'Spending_Score' in self.df.columns:
                    self.df['Spending_Score'] = self.df['Spending_Score'].map(res_map)

                # 2. Handle missing values
                num_cols = self.df.select_dtypes(include=[np.number]).columns
                for col in num_cols:
                    self.df[col] = self.df[col].fillna(self.df[col].median())

                cat_cols = self.df.select_dtypes(include=[object,'string']).columns
                for col in cat_cols:
                    mode_val = self.df[col].mode()
                    if not mode_val.empty:
                        self.df[col] = self.df[col].fillna(mode_val[0])
                print("Preprocessing Completed")
            except Exception as e:
                print(f"An unexcepted error occured while preprocessing data: {e} ")



    def build_pipeline(self, k=4):
        """
                Constructs a Scikit-Learn pipeline consisting of a ColumnTransformer,
                PCA for dimensionality reduction, and the KMeans model.

                Args:
                    k (int): The number of clusters for the KMeans algorithm.
        """

        self.preprocess_data()
        try:
            cat_selector = make_column_selector(dtype_include=[object,'string'])
            num_selector = make_column_selector(dtype_include=[np.number])

            # We manually select columns to ensure 'Spending_Score' is treated as numeric now
            transformer = make_column_transformer(
                (OneHotEncoder(handle_unknown='ignore', drop='if_binary'),cat_selector),
                (StandardScaler(), num_selector),
            )

            self.pipeline = make_pipeline(transformer,PCA(n_components=0.95), KMeans(n_clusters=k, random_state=self.random_state, n_init=10))
            print(f"Pipeline built with PCA and k={k}")
        except Exception as e:
            print(f"An unexcepted error occured while building pipeline: {e} ")


    def find_optimal_k(self, max_k=10):
        """
                Executes the Elbow Method to help determine the optimal number of clusters (k).

                Args:
                    max_k (int): The maximum number of clusters to test.
        """

        self.build_pipeline()
        try:
            print("Calculating Elbow Method...")
            # Get processed data from transformer part of pipeline
            X_transformed = self.pipeline.named_steps['columntransformer'].fit_transform(self.df)

            inertia = []
            K = range(1, max_k + 1)
            for k in K:
                km = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
                km.fit(X_transformed)
                inertia.append(km.inertia_)

            plt.figure(figsize=(8, 4))
            plt.plot(K, inertia, 'bx-')
            plt.title('Elbow Method')
            plt.show()
        except Exception as e:
            print(f"An unexcepted error occured while finding optimal k: {e} ")


    def train_data(self):
        """
                Fits the entire pipeline to the current dataframe.
        """

        self.find_optimal_k()
        try:
            print("Training data...")
            self.pipeline.fit(self.df)
            print("Training Completed")
        except Exception as e:
            print(f"An unexcepted error occured while training data: {e} ")


    def evaluate_model(self):
        """
                Calculates the Silhouette Score and attaches cluster labels to the dataframe.
        """

        self.train_data()
        try:
            print("Evaluating model...")
            X_transformed = self.pipeline.named_steps['columntransformer'].transform(self.df)
            labels = self.pipeline.named_steps['kmeans'].labels_

            score = silhouette_score(X_transformed, labels)
            print(f"--- Optimized Silhouette Score: {score:.4f} ---")
            self.df['Cluster'] = labels
            print("Evaluation Completed")
        except Exception as e:
            print(f"An unexcepted error occured while evaluating model: {e} ")



    def describe_clusters(self):
        """
                Generates and prints cluster profiles based on the mean of numeric features.
        """

        self.evaluate_model()
        try:
            print("\n--- Generating Cluster Profiles ---")

            # 1. Filter for numeric types only (including the Cluster labels)
            # Using 'number' covers ints, floats, and  mapped Spending_Score
            numeric_df = self.df.select_dtypes(include=[np.number])

            # 2. Calculate averages
            analysis = numeric_df.groupby('Cluster').mean().reset_index()

            print("\n--- Cluster Averages ---")
            print(analysis)

            # 3. Visualization
            plt.figure(figsize=(8, 5))
            sns.barplot(x='Cluster', y='Age', data=analysis, palette='viridis', hue='Cluster', legend=False)
            plt.title("Average Age per Cluster")
            plt.show()
        except Exception as e:
            print(f"An unexcepted error occured while generating cluster profiles: {e} ")


    def visualize(self):
        """
             Visualizes clusters in a 2D space using the PCA components.
        """

        self.describe_clusters()
        try:
            print("Visualizing Clusters...")
            # Get the PCA coordinates
            preprocessor = self.pipeline.named_steps['columntransformer']
            pca = self.pipeline.named_steps['pca']
            X_transformed = preprocessor.transform(self.df)
            X_pca = pca.transform(X_transformed)

            labels = self.pipeline.named_steps['kmeans'].labels_
            centroids = self.pipeline.named_steps['kmeans'].cluster_centers_

            plt.figure(figsize=(10, 7))
            # Use alpha=0.5 to see overlapping points better
            scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap='viridis',
                                  s=40, alpha=0.5, edgecolors='white', linewidth=0.2)

            # Plot Centroids as large red stars
            plt.scatter(centroids[:, 0], centroids[:, 1], s=300, marker='*',
                        c='red', label='Centroids', edgecolor='black')

            plt.title('Customer Segments (PCA Projection)', fontsize=15)
            plt.xlabel('Principal Component 1')
            plt.ylabel('Principal Component 2')
            plt.colorbar(scatter, label='Cluster ID')
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.show()
        except Exception as e:
            print(f"An unexcepted error occured while visualizing clusters: {e} ")
        print("Visualization Completed..")

def main():
    DATA_PATH = "Test.csv"
    model = CustomerSegmentation(DATA_PATH)
    model.visualize()


if __name__ == "__main__":
    main()


