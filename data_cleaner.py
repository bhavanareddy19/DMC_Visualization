import pandas as pd
import os
import sys


def clean_data(input_file, output_file=None):
    """
    Clean data by removing specific columns from XLSX or CSV files.

    Parameters:
    -----------
    input_file : str
        Path to the input file (XLSX or CSV)
    output_file : str, optional
        Path to save the cleaned file. If None, generates a name automatically.

    Returns:
    --------
    pd.DataFrame
        Cleaned DataFrame
    """

    # Columns to remove (exact matches)
    columns_to_remove = [
        'room name',
        'title',
        'customer',
        'Customer name',
        'email',
        'last status update',
        'Charged time',
        'Charged account type',
        'Charged account name',
        'Filename',
        'Additional instructions',
        'Special Information (Operator Only) Operator name',
        'Print Information (DMC staff only) Operator name'
    ]

    # Determine file type and read accordingly
    file_extension = os.path.splitext(input_file)[1].lower()

    try:
        if file_extension == '.xlsx':
            print(f"Reading XLSX file: {input_file}")
            df = pd.read_excel(input_file)
        elif file_extension == '.csv':
            print(f"Reading CSV file: {input_file}")
            # Try different encodings
            try:
                df = pd.read_csv(input_file, encoding='utf-8')
            except UnicodeDecodeError:
                print("UTF-8 failed, trying latin-1 encoding...")
                try:
                    df = pd.read_csv(input_file, encoding='latin-1')
                except UnicodeDecodeError:
                    print("latin-1 failed, trying cp1252 encoding...")
                    df = pd.read_csv(input_file, encoding='cp1252')
        else:
            raise ValueError(f"Unsupported file format: {file_extension}. Please use .xlsx or .csv")

        print(f"Original shape: {df.shape}")
        print(f"Original columns: {list(df.columns)}\n")

        # Find columns that exist in the dataframe (case-insensitive matching)
        columns_found = []
        columns_not_found = []

        for col_to_remove in columns_to_remove:
            # Try exact match first
            if col_to_remove in df.columns:
                columns_found.append(col_to_remove)
            else:
                # Try case-insensitive match
                matched = False
                for col in df.columns:
                    if col.lower() == col_to_remove.lower():
                        columns_found.append(col)
                        matched = True
                        break
                if not matched:
                    columns_not_found.append(col_to_remove)

        # Remove the columns
        if columns_found:
            print(f"Removing {len(columns_found)} columns:")
            for col in columns_found:
                print(f"  - {col}")
            df_cleaned = df.drop(columns=columns_found)
        else:
            print("No columns to remove found in the dataset.")
            df_cleaned = df.copy()

        if columns_not_found:
            print(f"\nColumns not found in dataset ({len(columns_not_found)}):")
            for col in columns_not_found:
                print(f"  - {col}")

        print(f"\nCleaned shape: {df_cleaned.shape}")
        print(f"Remaining columns: {list(df_cleaned.columns)}\n")

        # Generate output filename if not provided
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_cleaned{file_extension}"

        # Save the cleaned data in the same format as input
        if file_extension == '.xlsx':
            df_cleaned.to_excel(output_file, index=False)
            print(f"Cleaned data saved to: {output_file}")
        elif file_extension == '.csv':
            df_cleaned.to_csv(output_file, index=False)
            print(f"Cleaned data saved to: {output_file}")

        return df_cleaned

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        sys.exit(1)


def main():
    """
    Main function to handle command-line usage.
    """
    if len(sys.argv) < 2:
        print("Usage: python data_cleaner.py <input_file> [output_file]")
        print("\nExample:")
        print("  python data_cleaner.py orders.xlsx")
        print("  python data_cleaner.py data.csv cleaned_data.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    clean_data(input_file, output_file)


if __name__ == "__main__":
    main()
