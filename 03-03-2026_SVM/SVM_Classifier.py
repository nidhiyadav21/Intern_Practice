import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.decomposition import PCA
from sklearn.inspection import DecisionBoundaryDisplay

class HeartDiseaseModel:
    def __init__(self, filepath, test_size=0.3, random_state=42):
        self.filepath = filepath
        self.test_size = test_size
        self.random_state = random_state
        self.df = None
        self.X = None
        self.y = None
        self.X_train, self.X_test, self.y_train, self.y_test = [None] * 4
        self.pipeline = None

    def load_data(self):
        print("Loading data...")
        self.df = pd.read_csv(self.filepath)
        print(f"Data loaded: {self.df.shape}")

    def plot_diagnostics(self):
        """Generates boxplots to visualize outliers in the features."""
        # Focus only on truly numerical columns
        numeric_cols = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']

        plt.figure(figsize=(15, 10))
        for i, col in enumerate(numeric_cols, 1):
            plt.subplot(2, 3, i)
            sns.boxplot(y=self.df[col], color='skyblue')
            plt.title(f'Outlier Detection: {col}')

        plt.tight_layout()
        plt.show()

    def preprocess_data(self):
        print("Preprocessing data...")
        print("\nPrinting Dataset Information:\n")
        self.df.info()
        print("\nPrinting Dataset Description:\n", self.df.describe())
        print("\nPrinting first 5 rows:\n", self.df.head())
        print("\n Checking null values:\n", self.df.isnull().sum())
        print("\n Checking Duplicate values:\n", self.df.duplicated().sum())
        print("After dropping duplicate values:\n", self.df.drop_duplicates(keep='first'))
        self.df = self.df.drop_duplicates(keep='first')
        print(f"Duplicates removed. New shape: {self.df.shape}")
        self.y = self.df["target"]
        self.X = self.df.drop(columns="target")
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=self.test_size, random_state=self.random_state
        )

    def build_pipeline(self):
        print("Building pipeline...")
        cat_selector = make_column_selector(dtype_include=[object])
        # FIX: Changed dtype_include from object to np.number
        num_selector = make_column_selector(dtype_include=[np.number])

        transformer = make_column_transformer(
            (OneHotEncoder(handle_unknown='ignore'), cat_selector),
            (StandardScaler(), num_selector),
            remainder="passthrough"
        )

        svm_model = SVC(kernel='rbf', probability=True, random_state=self.random_state)
        self.pipeline = make_pipeline(transformer, svm_model)
        print("Pipeline Created")

    def train_pipeline(self):
        print("Training pipeline...")
        self.pipeline.fit(self.X_train, self.y_train)
        print("Training Completed")

    def evaluate(self):
            print("[INFO] Evaluating model...")
            y_pred = self.pipeline.predict(self.X_test)
            test_probs = self.pipeline.predict_proba(self.X_test)[:, 1]

            # Metrics
            accuracy = accuracy_score(self.y_test, y_pred)
            # roc_auc = roc_auc_score(self.y_test, test_probs)  # Added ROC-AUC

            print(f"\nAccuracy: {accuracy:.4f}")
            # print(f"ROC-AUC Score: {roc_auc:.4f}\n")
            print("Classification Report:")
            print(classification_report(self.y_test, y_pred))

            # Visualization
            cm = confusion_matrix(self.y_test, y_pred)
            plt.figure(figsize=(6, 4))
            # Added labels for clarity
            sns.heatmap(cm, annot=True, fmt='d', cmap='YlGnBu',
                        xticklabels=['No Disease', 'Disease'],
                        yticklabels=['No Disease', 'Disease'])
            plt.title('Confusion Matrix')
            plt.ylabel('Actual Label')
            plt.xlabel('Predicted Label')
            plt.show()

            return y_pred, test_probs

    def plot_decision_boundaries(self):
        print("[INFO] Plotting decision boundaries...")
        # Scale and reduce dimensions to 2D for plotting
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(self.X_train)

        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)

        # Fit a 2D model just for visualization
        svm_2d = SVC(kernel='rbf', C=1.0)
        svm_2d.fit(X_pca, self.y_train)

        plt.figure(figsize=(10, 6))
        DecisionBoundaryDisplay.from_estimator(
            svm_2d, X_pca, response_method="predict",
            cmap=plt.cm.Spectral, alpha=0.8, ax=plt.gca()
        )

        # Scatter points: look for points in the 'wrong' color zone to see misclassification
        plt.scatter(X_pca[:, 0], X_pca[:, 1], c=self.y_train, edgecolors='k', cmap=plt.cm.Spectral)
        plt.title("SVM Decision Boundary (PCA Reduced)")
        plt.show()



def main():
    DATA_PATH = "heart.csv"

    model = HeartDiseaseModel(DATA_PATH)
    try:
        model.load_data()
        model.plot_diagnostics()
        model.preprocess_data()
        model.build_pipeline()
        model.train_pipeline()
        # y_pred, test_probs = model.evaluate()

        # Calling code
        result = model.evaluate()
        if result is not None:
            y_pred, test_probs = result
        else:
            print("Evaluation failed to return values.")

        # CALLING THE PLOTS HERE:

        model.plot_decision_boundaries()

    except FileNotFoundError:
        print(f"[ERROR] Could not find {DATA_PATH}.")
    except Exception as e:
        print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()








