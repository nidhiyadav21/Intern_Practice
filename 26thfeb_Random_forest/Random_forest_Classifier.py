import pandas as pd
import numpy as np
from multipart import file_path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report

class LoanApprovalModel:

    def __init__(self,file_path,test_size=0.2,random_state=42):
        self.file_path = file_path
        self.test_size = test_size
        self.random_state = random_state
        self.df = None
        self.X  = None
        self.y = None
        self.pipeline = None

def load_data(self):
    print("[INFO] Loading Loan Dataset...")
    self.df = pd.read_csv(self.file_path)
    print(f"Data Loaded Successfully:{self.df.shape}")

def preprocess_data(self):
    if "Loan_ID" in self.df.columns:
        self.df.drop("Loan_ID",axis=1,inplace=True)