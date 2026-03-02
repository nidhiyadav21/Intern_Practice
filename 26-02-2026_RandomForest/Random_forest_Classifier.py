import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve

class LoanApprovalModel:

    def __init__(self,file_path,test_size=0.3,random_state=42):
        self.file_path = file_path
        self.test_size = test_size
        self.random_state = random_state
        self.df = None
        self.X  = None
        self.y = None
        self.pipeline = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def load_data(self):
        print("[INFO] Loading Loan Dataset...")
        self.df = pd.read_csv(self.file_path)
        print(f"Data Loaded Successfully:{self.df.shape}")


    def preprocess_data(self):

        self.df = self.df.dropna(subset=['loan_status'])
        self.y = self.df.pop('loan_status').astype(int)

        # Drop ID column (Commonly 'Loan_ID' in these datasets)
        if 'Loan_ID' in self.df.columns:
            self.X = self.df.drop('Loan_ID', axis=1)
        else:
            self.X = self.df

        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=self.test_size, random_state=self.random_state
        )

        # Handling missing values for the pipeline
        self.X_train = self.X_train.fillna(self.X_train.mode().iloc[0])
        self.X_test = self.X_test.fillna(self.X_train.mode().iloc[0])
        print("[INFO] Preprocessing completed.")

    import seaborn as sns
    import matplotlib.pyplot as plt

    def check_outliers(self):
        print("[INFO] Generating boxplots for numerical features...")

        # Automatically select only numeric columns to avoid errors with text columns
        num_cols = self.df.select_dtypes(include=['number']).columns.tolist()

        # Exclude columns that are binary (0/1) or targets
        # (Checking outliers for 'loan_status' doesn't make sense)
        exclude = ['loan_status', 'previous_loan_defaults_on_file']
        cols_to_plot = [c for c in num_cols if c not in exclude]

        # Create subplots to see each feature clearly
        plt.figure(figsize=(16, 12))
        for i, col in enumerate(cols_to_plot):
            plt.subplot(3, 3, i + 1)
            sns.boxplot(y=self.df[col], color='lightgreen')
            plt.title(f'Outliers in {col}')
            plt.grid(axis='y', linestyle='--', alpha=0.5)

        plt.tight_layout()
        plt.show()

    def build_pipeline(self):
        print("[INFO] Building Random Forest Pipeline...")

        cat_selector = make_column_selector(dtype_include=object)

        # Transformer for categorical data
        transformer = make_column_transformer(
            (OneHotEncoder(handle_unknown="ignore"), cat_selector),
            remainder="passthrough"
        )

        # Random Forest Model
        rf_model = RandomForestClassifier(
            n_estimators=100,
            random_state=self.random_state,
            class_weight='balanced'  # Good for loan datasets which are often imbalanced
        )

        self.pipeline = make_pipeline(transformer, rf_model)
        print("[INFO] Pipeline created.")


    def train(self):
        print("[INFO] Training model...")
        self.pipeline.fit(self.X_train, self.y_train)


    def evaluate(self):
        print("[INFO] Evaluating model...")
        y_pred = self.pipeline.predict(self.X_test)
        test_probs = self.pipeline.predict_proba(self.X_test)[:, 1]

        accuracy = accuracy_score(self.y_test, y_pred)
        auc_score = roc_auc_score(self.y_test, test_probs)

        print("\n========== LOAN MODEL PERFORMANCE ==========")
        print(f"Accuracy : {accuracy:.4f}")
        print(f"ROC-AUC  : {auc_score:.4f}")
        print("============================================\n")
        return test_probs


    def plot_roc(self, test_probs):
        fpr, tpr, _ = roc_curve(self.y_test, test_probs)
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, label=f"Random Forest (AUC = {roc_auc_score(self.y_test, test_probs):.2f})")
        plt.plot([0, 1], [0, 1], 'k--', label="Random Guess")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("Loan Approval ROC Curve")
        plt.legend()
        plt.grid(True)
        plt.show()


def main():
    # Ensure your filename matches: "loan_data.csv"
    DATA_PATH = "loan_data.csv"

    model = LoanApprovalModel(DATA_PATH)
    model.load_data()
    model.preprocess_data()
    model.build_pipeline()
    model.train()
    probs = model.evaluate()
    model.plot_roc(probs)
    model.check_outliers()


if __name__ == "__main__":
    main()