import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score


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

        X_train_raw,X_test_raw,self.y_train ,self.y_test = train_test_split(X,y,test_size=test_size,random_state= 42)

        self.X_train = self.scaler.fit_transform(X_train_raw)
        self.X_test = self.scaler.transform(X_test_raw)

        if np.isnan(self.X_train).any() or np.isnan(self.X_test).any():
            print("Warning: NaNs detected after scaling! Imputing zeros.")
            self.X_train = np.nan_to_num(self.X_train)
            self.X_test = np.nan_to_num(self.X_test)

        print(f"Data prepared. Training shape: {self.X_train.shape}")

    def run_grid_search(self):
        parameters = [
            {'C': [0.1, 1, 10, 100], 'kernel': ['linear']},
            {'C': [0.1, 1, 10, 100], 'kernel': ['rbf'], 'gamma': ['scale', 'auto', 0.01, 0.1]}
        ]
        grid = GridSearchCV(SVC(probability=True), parameters, scoring='accuracy', cv=5)
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

if __name__ == "__main__":
    diabetes_pipeline = DiabetesClassifier("diabetes.csv")
    diabetes_pipeline.load_and_clean_data()
    # diabetes_pipeline.plot_diagnostics()
    diabetes_pipeline.prepare_data()
    diabetes_pipeline.run_grid_search()
    diabetes_pipeline.evaluate()






