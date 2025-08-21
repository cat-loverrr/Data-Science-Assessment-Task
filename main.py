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
        "description": "Mean housing costs from 1994-95 to 2019-20."
    }
}

# Global variables
current_dataset = None
df = None

# Load dataset based on name
def load_dataset(name):
    global current_dataset, df
    if name in datasets:
        current_dataset = datasets[name]['file']
        print(f"\nLoaded dataset: {name} - {datasets[name]['description']}")
        try:
            df = pd.read_csv(current_dataset, skipinitialspace=True, engine='python')
            df = df.dropna(axis=1, how='all')
            df = df.map(lambda x: x.strip() if isinstance(x, str) else x)  # Clean spaces
            # --- Add this block below ---
            # Remove the 'Type' column if present
            df = df.drop(columns=['Type'], errors='ignore')

            # Remove asterisks and convert to numeric where possible
            for col in df.columns[1:]:  # Skip the first column (category/label)
                df[col] = (
                    df[col]
                    .replace(r'[*]+', '', regex=True)  # Remove asterisks
                    .replace('', pd.NA)                # Replace empty strings with NA
                )

            df = df.rename(columns={df.columns[0]: "Category"})
            df.columns = ["Category"] + [f"Column {i+1}" for i in range(1, len(df.columns))]
            print("Dataset loaded successfully.")
        except Exception as e:
            print(f"Error loading dataset: {e}")
    else:
        print("Dataset name not found.")

# Guided exploration prompt
def guided_exploration():
    print("\nWhat would you like to explore?")
    print("1. The mean housing costs in 2019-20")
    print("2. The average housing costs from 1994-95 to 2019-20")

    choice = input("Select an option (1-2): ").strip()

    if choice == '1':
        load_dataset("Housing Option 1")
    elif choice == '2':
        load_dataset("Housing Option 2")
    else:
        print("Invalid selection.")

# Manual dataset selection
def select_dataset():
    global current_dataset, df
    print("\nAvailable datasets:")
    for i, (name, info) in enumerate(datasets.items(), 1):
        print(f"{i}. {name} - {info['description']}")
    choice = input("Select a dataset by number: ").strip()
    try:
        index = int(choice) - 1
        key = list(datasets.keys())[index]
        load_dataset(key)
    except (ValueError, IndexError) as e:
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
        # Drop rows where X or Y is missing
        plot_df = df[[x_col, y_col]].dropna()
        # Convert X to string for categorical plotting
        plot_df[x_col] = plot_df[x_col].astype(str)
        plt.figure(figsize=(10, 5))
        plt.plot(plot_df[x_col], plot_df[y_col], marker='o')
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

