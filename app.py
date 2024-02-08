from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
app = Flask(__name__)

CORS(app)
def filter_price(df, price_value):
    if pd.notna(price_value) and price_value != 'nan' and price_value != '0':
        if price_value == 'pocket friendly':
            return df[df['Pocket Friendly'] == 1]
        elif price_value == 'mid range':
            return df[df['Mid Range'] == 1]
        elif price_value == 'high end':
            return df[df['High End'] == 1]
        else:
            print("Invalid price category. Please choose 'Pocket Friendly', 'Mid Range', or 'High End'.")
            return None
    else:
        print("Invalid price value. Please provide a valid value.")
        return None

def filter_brand(df, brand_value):
    if not pd.notna(brand_value) or brand_value == 'nan' or brand_value == '0':
        return df
    else:
        brand_list = df['Brand'].value_counts().index
        if brand_value in brand_list:
            return df[df['Brand'] == brand_value]
        else:
            print("Invalid brand value. Please provide a valid brand.")
            return None

def filter_usecase(df, usecase_value):
    if pd.isna(usecase_value) or usecase_value == 'nan' or usecase_value == '0':
        return df
    else:
        if usecase_value == 'everyday':
            return df[df['EveryDay'] == 1]
        elif usecase_value == 'professional':
            return df[df['Professional'] == 1]
        elif usecase_value == 'gaming':
            return df[df['Gaming'] == 1]
        else:
            print("Invalid UseCase value. Please provide a valid UseCase.")
            return None

def filter_os(df, os_value):
    if not pd.notna(os_value) or os_value == 'nan' or os_value == '0':
        return df
    else:
        return df[df['Operating System'] == os_value]


def get_top_laptops(df):
    # Define weights for each feature
    weights = {
        'Price_Normalized': -0.2,
        'Number of Cores_Normalized': 0.1,
        'HDD Capacity_Normalized': 0.1,
        'SSD Capacity Normalized': 0.2,
        'Normalized review': 0.2,
        'RAM(in GB)': 0.1,
        'MS Office Provided': 0.1
    }

    # Calculate the weighted values for each row
    df['Weighted_Score'] = df[list(weights.keys())].dot(pd.Series(weights))

    # Sort the DataFrame based on the weighted score in descending order
    sorted_df = df.sort_values(by='Weighted_Score', ascending=False)

    # Get the top 5 rows
    top_laptops = sorted_df.head(5)

    return top_laptops

def master_filter(df,input_values):
    values = [v.strip().lower() for v in input_values]
    print( "values", values[0], values[1], values[2], values[3])
    filtered_df = df.copy() 

    # Apply filters based on user input
    filtered_df = filter_price(filtered_df, values[0])
    filtered_df = filter_usecase(filtered_df, values[1])
    filtered_df = filter_os(filtered_df, values[2])
    filtered_df = filter_brand(filtered_df, values[3])
    # filtered_df = filter_os(filtered_df, values[3])

    return filtered_df

# Assuming df is your original DataFrame
df = pd.read_csv("Laptop_Dataset_completed.csv")

@app.route('/get_top_laptops', methods=['POST'])

def get_top_laptops_api():
    try:
     
        input_values = request.json.get('input_values')
        print(input_values)
        result_df_master = master_filter(df, input_values)
        top_laptops_result = get_top_laptops(result_df_master)
        return jsonify(top_laptops_result.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)