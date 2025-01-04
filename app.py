import pandas as pd
import json

# Step 1: Load the dataset
shipment_data = pd.read_csv("./data/FAF5.6.1_State.csv")
mapping = pd.read_csv("./data/states.csv")

# Merge mapping file to add state names
shipment_data = pd.merge(shipment_data, mapping, left_on='dms_origst', right_on='Numeric Label', how='left')
shipment_data.rename(columns={'Description': 'Origin_State'}, inplace=True)
shipment_data = pd.merge(shipment_data, mapping, left_on='dms_destst', right_on='Numeric Label', how='left')
shipment_data.rename(columns={'Description': 'Destination_State'}, inplace=True)

# Filter for Maryland
maryland_data = shipment_data[shipment_data['Origin_State'] == 'Maryland']

# Select relevant columns (tons_2017, tons_2018, etc.)
years = [col for col in maryland_data.columns if 'tons_' in col]
maryland_yearly_data = maryland_data[['Destination_State'] + years]

# Group by destination state and sum yearly tons
maryland_grouped = maryland_yearly_data.groupby('Destination_State').sum()

# Reset index
maryland_grouped = maryland_grouped.reset_index()

# Prepare data for Plotly
years = [int(year.split('_')[1]) for year in maryland_grouped.columns if 'tons_' in year]
chart_data = []
for _, row in maryland_grouped.iterrows():
    chart_data.append({
        'state': row['Destination_State'],
        'tons': row[1:].tolist()  # Extract tons columns
    })

# Export data as JSON
output_file = "./data/chart_data.json"
with open(output_file, "w") as f:
    json.dump({'years': years, 'data': chart_data}, f)

print(f"Chart data exported to {output_file}")
