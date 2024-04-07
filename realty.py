import pandas as pd
#https://download.hcad.org/data/CAMA/2024/Real_acct_owner.zip
#unzip the real_acct.txt file to work with

# Define file paths
file1_path = 'real_acct.txt'  # Replace 'file1.csv' with the path to your first file
#file2_path = 'building_res.txt'  # Replace 'file2.csv' with the path to your second file

# Read files into pandas dataframes
try:
    df1 = pd.read_csv(file1_path, delimiter='\t', on_bad_lines='skip', low_memory=False, encoding='iso-8859-1')
#    df2 = pd.read_csv(file2_path, delimiter='\t', on_bad_lines='skip', low_memory=False, encoding='iso-8859-1')
except pd.errors.ParserError as e:
    print("ParserError:", e)


def derive_years(start = "none" , end = 'none'):
    array = []
    try:
        range(start, end)
        for each in range(start, end):
            array.append(str(each))
        return array
    except:
        array = 0
        return array
    
def filter_homes(df, market_area_codes, sqft, build_val, land_val, land_ar, years):
    # Filter based on state_class and years
    state_class = ['A1']
    if type(years) == list:
        filtered_df = df[df['state_class'].isin(state_class) & df['yr_impr'].isin(years)]
    else:
        filtered_df = df[df['state_class'].isin(state_class)]
    # Calculate desired_base_ar based on sqft looking for homes with at least 5 percent more sqft than the account chosen
    desired_base_ar = (sqft * 0.05) + sqft
    
    # Create criteria for filtering
    criteria = (filtered_df['Market_Area_1'].isin(market_area_codes)) & \
               (filtered_df['bld_ar'] >= desired_base_ar) & \
               (filtered_df['land_ar'] >= land_ar) & \
               (filtered_df['assessed_val'] < build_val) &\
               (filtered_df['land_val'] <= land_val)
    
    # Apply criteria to filter DataFrame
    final_filtered_df = filtered_df[criteria]
    
    return final_filtered_df


#year range you'd like to query for, can give it no range of years to retrieve all years
years = derive_years()

# Define parameters per the account you choose. or you can define your own data manually as well.
account = df1[df1['acct'] == INSERT_ACCT_NUMBER_HERE]

#add market codes to define the area you are looking in for houses. should be a list of strings
market_area_codes = [account['Market_Area_1'].iloc[0]]
#the listed living sqft as an int
bld_ar  = account['bld_ar'].iloc[0]
#your homes assessed_val per the building and land as ints
bld_val = account["bld_val"].iloc[0]
land_val = account["land_val"].iloc[0]

#sqft of the plot as int
land_ar = account["land_ar"].iloc[0]


# Call the function to filter homes
filtered_homes = filter_homes(df1, market_area_codes, bld_ar, bld_val, land_val, land_ar, years)

# Save the filtered DataFrame to a CSV file
filtered_homes.to_csv('list_of_lower_assessed_homes.csv', index=False)