# cleaning.py
import pandas as pd
import project_environment as env

def header_fix(df, new_header):
    # Remove all product like 京都念慈菴XX潤喉糖 except 京都念慈菴枇杷潤喉糖 - 原味
    df.drop(index=df.index[10:15], inplace=True) 
    
    # Rename header
    df.columns = new_header  # Set the new header
    df.columns = [f'Column{i+1}' if pd.isna(col) else col for i, col in enumerate(df.columns)]
    column_names = df.columns.tolist()
    reserve_list = [column_names[0], column_names[3]] + column_names[7:-5]

    for col in column_names:
        if col not in reserve_list:
            df.drop(columns=[col], inplace=True)

    # Rename "京都念慈菴枇杷潤喉糖 - 原味" as "京都念慈菴潤喉糖"
    df.loc[df["product"] == "京都念慈菴枇杷潤喉糖 - 原味", "product"] = "京都念慈菴潤喉糖"

    # Column Rename
    new_columns = ['index', 'product','diabetes', 'pregnancy', 'duration', 'severity', 'frequency', 'phlegm', 'phlegm_color', 'phlegm_thickness']
    col_map = {}
    for i in range(len(reserve_list)):
        col_map[reserve_list[i]] = new_columns[i]

    df.rename(columns=col_map, inplace=True)

    return df, new_columns

def first_time_resize(df):
    df = df.iloc[1:23] # Get the necessary rows

    new_header = df.iloc[0]
    df = df[1:]  # Get the DataFrame without the header (first row)
    df.drop(index=df.index[1], inplace=True) # Remove the product 京都念慈菴蜜煉川貝枇杷膏（便利裝）, as it's identical as 京都念慈菴蜜煉川貝枇杷膏
    
    return df, new_header

def observation(df, new_columns):
    for column_name in new_columns[2:]:
        unique_values = sorted(df[column_name].unique())
        print('Column Name:', column_name)
        print('Unique values:', unique_values)
        print('Number of unique values:', len(unique_values))
        print()

def second_time_rename(df, new_columns):
    # Special columns
    value_base = ['severity', 'frequency']

    # rename mapping
    main_mapping = {}

    for column_name in new_columns[2:]:
        map = {}
        unique_values = sorted(df[column_name].unique())

        if column_name in value_base:
            for value in unique_values:
                if not int(value[-1]):
                    map[value] = 10
                else:
                    map[value] = int(value[-1])
        elif column_name == "phlegm_color":
            for value in unique_values:
                if value != '不適用, 黃':
                    map[value] = 0
                else:
                    map[value] = 1
        elif column_name == "phlegm_thickness":
            for value in unique_values:
                if value != '不適用, 黏稠':
                    map[value] = 0
                else:
                    map[value] = 1
        else:
            i = 0
            for value in unique_values:
                map[value] = i
                i += 1
        main_mapping[column_name] = map
    return main_mapping

def cleaning(df, col, mapping):
    for cond_value in df[col].unique():
        df.loc[df[col] == cond_value, col] = mapping[cond_value]
    return df

def final_clean(df, new_columns, main_mapping):
    for column_name in new_columns[2:]:
        cleaning(df, column_name, main_mapping[column_name])
        #cleaning(column_name, target_value, cond_value)
    return df

def first_time_fix():
    df = pd.read_excel(env.teammate_file)
    df, new_header = first_time_resize(df)
    return header_fix(df.reset_index(drop=True), new_header)

def second_time_fix(df, new_columns):
    main_mapping = second_time_rename(df, new_columns)
    final_clean(df, new_columns, main_mapping)
    return df

def load_and_clean_data():
    df, new_columns = first_time_fix()
    return second_time_fix(df, new_columns)