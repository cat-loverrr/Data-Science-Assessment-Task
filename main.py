import pandas as pd
import matplotlib.pyplot as plt

# Defining my datasets
datasets = {
    "Housing Option 1": {
        "file": "mean_weekly_housing_costs_2019-20.csv",
        "description": "Mean housing costs in 2019-20."
    },
    "Housing Option 2": {
        "file": "mean_weekly_housing_costs1994-2020.csv",
        "description": "Mean housing costs in 1994-95 to 2019-20."
  }

# Global variables
current_dataset = None
df = None

# Load dataset based on name
def load_dataset(name):
    global current_dataset, df
    current_dataset = datasets[name]['file']
    print(f"\nLoaded dataset: {name} - {datasets[name]['description']}")
    try:
        df = pd.read_csv(current_dataset)
        print("Dataset loaded successfully.")
    except Exception as e:
        print(f"Error loading dataset: {e}")

# Guided exploration prompt
def guided_exploration():
    print("\nWhat would you like to explore? Either:")
    print("1. The average/mean housing costs from 1994-95 to 2019-20")
    print("2. The mean/average housing costs in 2019-20.")

    choice = input("Select an option (1-2): ").strip()

    if choice == 'a':
        load_dataset("Housing Option 1")
    elif choice == 'b':
        load_dataset("Housing Option 2")
    else:
        print("Invalid selection.")

# Manual dataset selection
def select_dataset():
    global current_dataset, df
    print("\nAvailable datasets:")
    for i, (name, info) in enumerate(datasets.items(), 1):
        print(f"{i}. {name} - {info['description']}")
    choice = input("Select a dataset: ").strip()
    try:
        index = int(choice) - 1
        key = list(datasets.keys())[index]
        current_dataset = datasets[key]['file']
        print(f"Selected dataset: {key}")
        df = pd.read_csv(current_dataset)
        print("Dataset loaded successfully.")
    except (ValueError, IndexError, Exception) as e:
        print(f"Error: {e}")

# Preview the dataset
def display_dataset_preview():
    if df is not None:
        print("\n=== Dataset Preview ===")
        print(df.head())
    else:
        print("No dataset loaded. Please select a dataset first.")

# Display a simple visualisation
def display_visualisation():
    if df is None:
        print("No dataset loaded. Please select a dataset first.")
        return

    print("\nAvailable columns:")
    for i, col in enumerate(df.columns, 1):
        print(f"{i}. {col}")

    x_col = input("Enter the column name for the X-axis (e.g., Year): ").strip()
    y_col = input("Enter the column name for the Y-axis (e.g., Income): ").strip()

    if x_col in df.columns and y_col in df.columns:
        plt.figure(figsize=(10, 5))
        plt.plot(df[x_col], df[y_col], marker='o')
        plt.title(f"{y_col} over {x_col}")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        print("Invalid column names. Please try again.")

# Run the guided flow directly
if __name__ == "__main__":
    guided_exploration()
    while True:
        print("\nWhat would you like to do next?")
        print("1. Preview dataset")
        print("2. Display visualisation")
        print("3. Exit")
        next_action = input("Choose an option (1-3): ").strip()

        if next_action == '1':
            display_dataset_preview()
        elif next_action == '2':
            display_visualisation()
        elif next_action == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid selection.")
