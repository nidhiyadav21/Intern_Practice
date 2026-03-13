import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori,association_rules
from mlxtend.preprocessing import TransactionEncoder

class AprioriModel():
    """
            Initializes the AprioriModel with file settings and algorithm parameters.

            Args:
                file_path (str): The path to the CSV dataset.
                min_support (float): The minimum support threshold for Apriori.
                min_threshold (float): The minimum lift threshold for generating rules.
    """
    def __init__(self,file_path,min_support=0.01,min_threshold = 1.0):
         self.file_path = file_path
         self.min_support = min_support
         self.min_threshold = min_threshold
         self.df  = None

         self.basket_df = None
         self.frequent_itemsets = None
         self.rules = None

    def load_data(self):
        """
               Reads the CSV file from the file_path into a pandas DataFrame and
               prints basic summary statistics and information.
        """
        print("Loading data...")
        try:
            self.df = pd.read_csv(self.file_path)
            print("\nPrinting first 5 rows:\n",self.df.head())
            print("\nData Information:\n")
            self.df.info()
            print("\nData Description:\n", self.df.describe())
            print(f"Data Loaded:\n {self.df.shape}")
        except Exception as e:
            print(e)

    def preprocess_data(self):
        """
               Triggers data loading and checks for missing (null) values and
               duplicate rows within the dataset.
        """

        self.load_data()
        try:
            print("Preprocessing data...")
            print("\n Checking Null values:\n",self.df.isnull().sum())
            print("\nChecking Duplicate values:\n",self.df.duplicated().sum())
            print("Preprocessing Completed")
        except Exception as e:
            print(e)

    def check_data_quality(self):
        """
               Cleans the 'Date' column by converting it to datetime objects and
               visualizes the top 20 most frequently purchased items.
        """

        self.preprocess_data()
        try:
        # Convert Date to datetime object (important for grouping)
            self.df['Date'] = pd.to_datetime(self.df['Date'], dayfirst=True)


            # Instead of Boxplots, visualize the Top 10 Most Frequent Items
            print("\nPlotting Item Frequency...")
            plt.figure(figsize=(10, 6))
            self.df['itemDescription'].value_counts().head(20).plot(kind='bar', color='skyblue')
            plt.title("Top 10 Most Frequent Items")
            plt.ylabel("Frequency")
            plt.xticks(rotation=45)
            plt.show()
            print("\nPlotting Done")
        except Exception as e:
            print(e)


    def create_basket(self):
        """
               Groups the data by Member and Date to create shopping 'baskets'.
               Uses TransactionEncoder to transform lists of items into a True/False matrix.
        """

        self.check_data_quality()
        try:
            print("\nGrouping Transactions\n")
            transactions = self.df.groupby(['Member_number','Date'])['itemDescription'].apply(list).values.tolist()
            print(f"No. of Unique Transactions: {len(transactions)}")

            #TransactionEncoder as a translator.
            # It translates a list of items into a mathematical table (Matrix) that the Apriori algorithm can understand.
            te = TransactionEncoder()
            te.matrix = te.fit(transactions).transform(transactions)
            self.basket_df = pd.DataFrame(te.matrix,columns = te.columns_)
            print("\nBasket Matrix Created\n")
            print(self.basket_df.iloc[:10,:10].to_string())

            print("\nTop Items in Basket:\n")
            print(self.basket_df.sum().sort_values(ascending=False).head(10))
            print("Grouping Done")
        except Exception as e:
            print(e)



    def generate_rules(self):
        """
                Runs the Apriori algorithm to find frequent itemsets and then
                generates association rules based on the 'lift' metric.
        """

        self.create_basket()
        try:
            print(f"\nRunning Apriori (Support {self.min_support})")
            self.frequent_itemsets = apriori(self.basket_df,min_support=self.min_support,use_colnames=True)

            if self.frequent_itemsets.empty:
                print("No frequent itemsets found")
                self.rules = pd.DataFrame()
                return
            print(f"Generating Rules(Lift_Threshold {self.min_threshold})")
            self.rules = association_rules(self.frequent_itemsets,metric="lift",min_threshold=self.min_threshold)
            self.rules = self.rules.sort_values(by="lift",ascending=False)
            print("\nRules Generation Completed\n")
            print(self.rules.head())
        except Exception as e:
            print(e)



    def visualize_results(self):
        """Plots Support vs Confidence of the rules."""
        self.generate_rules()
        try:
            if self.rules.empty:
                print("No rules found. Try lowering min_support.")
                return

            print("\nTop 5 Rules:")
            print(self.rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
                              .head(20).round(4).to_string())

            # Visualization
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x="support", y="confidence", size="lift", data=self.rules, hue="lift", palette="YlOrRd")
            plt.title("Rules: Support vs Confidence (Sized by Lift)")
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(e)


def main():
    DATA_PATH = "Groceries_dataset.csv"
    model = AprioriModel(DATA_PATH,min_support=0.001, min_threshold=1.0)

    model.visualize_results()

if __name__ == "__main__":
    main()











