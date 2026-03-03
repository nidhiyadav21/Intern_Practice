import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score
from sklearn.decomposition import PCA
from sklearn.inspection import DecisionBoundaryDisplay


class DiabetesClassifier:

    def __init__(self,file_path):
        self.file_path = file_path
        self.df = None
        self.X = None
        self.y = None

        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.best_model = None

    def load_and_clean_data(self):
        try:
            self.df = pd.read_csv(self.file_path)
            print(f"Data Loaded. Shape: {self.df.shape}")
        except FileNotFoundError:
            print("File not found.")
            exit()

    def prepare_data(self,test_size=0.3):
        self.df.dropna(inplace=True)

        X = self.df.drop("Outcome",axis=1)
        y = self.df["Outcome"]

        X_train_raw,X_test_raw,self.y_train ,self.y_test = train_test_split(X,y,test_size=test_size,random_state= 42,stratify=y)

        self.X_train = self.scaler.fit_transform(X_train_raw)
        self.X_test = self.scaler.transform(X_test_raw)

        if np.isnan(self.X_train).any() or np.isnan(self.X_test).any():
            print("Warning: NaNs detected after scaling! Imputing zeros.")
            self.X_train = np.nan_to_num(self.X_train)
            self.X_test = np.nan_to_num(self.X_test)

        print(f"Data prepared. Training shape: {self.X_train.shape}")

    def run_grid_search(self):
        parameters = [
            {'C': [0.1,1,10, 100], 'kernel': ['linear']},
            {'C': [0.5, 0.8, 1.0, 1.2,1.5], 'kernel': ['rbf'], 'gamma': ['scale',0.05, 0.1, 0.2]}
        ]
        grid = GridSearchCV(SVC(probability=True,class_weight='balanced'), parameters, scoring='accuracy', cv=5)
        grid.fit(self.X_train, self.y_train)

        self.best_model = grid.best_estimator_
        print(f"Best parameters: {grid.best_params_}")

    def evaluate(self):
        y_pred = self.best_model.predict(self.X_test)

        acc = accuracy_score(self.y_test, y_pred)

        print("\n" + "=" * 30 + "\nFINAL EVALUATION\n" + "=" * 30)
        print(f"Accuracy: {acc}")
        print("Classification Report:")
        print(classification_report(self.y_test, y_pred))

        cm = confusion_matrix(self.y_test, y_pred)
        plt.figure(figsize = (6,4))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False)
        plt.title("Confusion Matrix")
        plt.ylabel("Actual label")
        plt.xlabel("Predicted label")
        plt.show()

        from sklearn.decomposition import PCA
        from sklearn.inspection import DecisionBoundaryDisplay

    def plot_rbf_boundary(self, C=1.0, gamma=0.1):
        """Visualizes a curvy RBF decision boundary to better capture overlapping data."""
        if self.X_train is None:
                print("Prepare data first!")
                return

            # 1. Reduce to 2D for visualization
        pca = PCA(n_components=2)
        X_train_pca = pca.fit_transform(self.X_train)
        X_test_pca = pca.transform(self.X_test)

        # 2. Force an RBF model for this plot
        # Increasing gamma makes the boundary 'tighter' and more 'curvy'
        rbf_model = SVC(kernel='rbf', C=C, gamma=gamma, class_weight='balanced')
        rbf_model.fit(X_train_pca, self.y_train)

        # 3. Plotting
        plt.figure(figsize=(10, 8))

        # Draw the RBF decision regions
        DecisionBoundaryDisplay.from_estimator(
            rbf_model,
            X_train_pca,
            response_method="predict",
            cmap='RdYlGn',
            alpha=0.3,
            ax=plt.gca()
            )

        # Plot the actual data points
        scatter = plt.scatter(X_test_pca[:, 0], X_test_pca[:, 1], c=self.y_test,
                                edgecolors='k', cmap='RdYlGn', s=50)

        plt.title(f"SVM RBF Boundary (PCA Reduced)\nC={C}, Gamma={gamma}", fontsize=15)
        plt.xlabel("Principal Component 1")
        plt.ylabel("Principal Component 2")
        plt.legend(*scatter.legend_elements(), title="Actual Labels")
        plt.show()




if __name__ == "__main__":
    diabetes_pipeline = DiabetesClassifier("diabetes.csv")
    diabetes_pipeline.load_and_clean_data()
    # diabetes_pipeline.plot_diagnostics()
    diabetes_pipeline.prepare_data()
    diabetes_pipeline.run_grid_search()
    diabetes_pipeline.evaluate()
    diabetes_pipeline.plot_rbf_boundary()






