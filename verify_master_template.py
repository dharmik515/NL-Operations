import pandas as pd
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("MASTER TEMPLATE VERIFICATION")
print("="*80)

# Read the generated master template
master = pd.read_excel('Master_Template_20260502_121630.xlsx', sheet_name='StockTake Template', engine='openpyxl')

print(f"\nTotal rows in Master Template: {len(master)}")
print(f"Total columns: {len(master.columns)}")
print(f"\nColumns: {list(master.columns)}")

print("\n" + "="*80)
print("BREAKDOWN BY SOURCE (Room)")
print("="*80)
room_counts = master['Room'].value_counts()
print(room_counts)

print("\n" + "="*80)
print("BREAKDOWN BY BIN TYPE")
print("="*80)
bin_counts = master['Bin'].value_counts()
print(bin_counts)

print("\n" + "="*80)
print("DEAL ID ANALYSIS")
print("="*80)
no_deal = (master['Deal Id'] == 'No deal ID').sum()
with_deal = (master['Deal Id'] != 'No deal ID').sum()
print(f"With Deal ID: {with_deal}")
print(f"No deal ID: {no_deal}")
print(f"Tracking Rate: {round(with_deal/len(master)*100, 2)}%")

print("\n" + "="*80)
print("STACK BULK DATA ANALYSIS")
print("="*80)
has_category = master['Category'].notna() & (master['Category'].astype(str).str.strip() != '')
has_brand = master['Brand'].notna() & (master['Brand'].astype(str).str.strip() != '')
has_model = master['Model'].notna() & (master['Model'].astype(str).str.strip() != '')

print(f"Rows with Category: {has_category.sum()}")
print(f"Rows with Brand: {has_brand.sum()}")
print(f"Rows with Model: {has_model.sum()}")

print("\n" + "="*80)
print("DETAILED BREAKDOWN BY SOURCE")
print("="*80)

for room in master['Room'].unique():
    room_df = master[master['Room'] == room]
    no_deal_count = (room_df['Deal Id'] == 'No deal ID').sum()
    with_deal_count = (room_df['Deal Id'] != 'No deal ID').sum()
    has_stack_data = (room_df['Category'].notna() & (room_df['Category'].astype(str).str.strip() != '')).sum()
    
    print(f"\n{room}:")
    print(f"  Total: {len(room_df)}")
    print(f"  With Deal ID: {with_deal_count}")
    print(f"  No deal ID: {no_deal_count}")
    print(f"  With Stack Bulk data: {has_stack_data}")
    print(f"  Bin types: {room_df['Bin'].value_counts().to_dict()}")

print("\n" + "="*80)
print("SAMPLE ROWS FROM EACH SOURCE")
print("="*80)

for room in master['Room'].unique():
    print(f"\n{'='*80}")
    print(f"SAMPLE FROM: {room}")
    print('='*80)
    room_df = master[master['Room'] == room]
    
    # Show 3 samples: with Deal ID, without Deal ID, with Stack data
    with_deal = room_df[room_df['Deal Id'] != 'No deal ID'].head(2)
    no_deal = room_df[room_df['Deal Id'] == 'No deal ID'].head(2)
    
    if len(with_deal) > 0:
        print("\nWith Deal ID:")
        for idx, row in with_deal.iterrows():
            print(f"\nRow {idx}:")
            print(f"  Room: {row['Room']}")
            print(f"  Bin: {row['Bin']}")
            print(f"  Location: {row['Location']}")
            print(f"  IMEI: {row['IMEI']}")
            print(f"  Deal Id: {row['Deal Id']}")
            print(f"  Category: {row['Category']}")
            print(f"  Brand: {row['Brand']}")
            print(f"  Model: {row['Model']}")
            print(f"  Grade: {row['Grade']}")
            print(f"  Status: {row['Status']}")
    
    if len(no_deal) > 0:
        print("\nWithout Deal ID:")
        for idx, row in no_deal.iterrows():
            print(f"\nRow {idx}:")
            print(f"  Room: {row['Room']}")
            print(f"  Bin: {row['Bin']}")
            print(f"  Location: {row['Location']}")
            print(f"  IMEI: {row['IMEI']}")
            print(f"  Deal Id: {row['Deal Id']}")
            print(f"  Category: {row['Category']}")
            print(f"  Brand: {row['Brand']}")
            print(f"  Model: {row['Model']}")

print("\n" + "="*80)
print("CHECKING FOR ISSUES")
print("="*80)

# Check 1: Rows with Deal ID but no Stack Bulk data
has_deal_no_data = master[
    (master['Deal Id'] != 'No deal ID') & 
    (master['Category'].isna() | (master['Category'].astype(str).str.strip() == ''))
]
print(f"\n⚠️  Rows with Deal ID but NO Stack Bulk data: {len(has_deal_no_data)}")
if len(has_deal_no_data) > 0:
    print("Sample Deal IDs not found in Stack Bulk:")
    print(has_deal_no_data['Deal Id'].value_counts().head(10))

# Check 2: Empty IMEI
empty_imei = master[master['IMEI'].isna() | (master['IMEI'].astype(str).str.strip() == '')]
print(f"\n⚠️  Rows with empty IMEI: {len(empty_imei)}")

# Check 3: Duplicate IMEIs
dup_imei = master[master.duplicated('IMEI', keep=False) & (master['IMEI'].astype(str).str.strip() != '')]
print(f"\n⚠️  Duplicate IMEIs: {len(dup_imei)}")
if len(dup_imei) > 0:
    print("Sample duplicates:")
    print(dup_imei[['Room', 'Bin', 'Location', 'IMEI', 'Deal Id']].head(10))

# Check 4: INBOUND specific analysis
print("\n" + "="*80)
print("INBOUND SPECIFIC ANALYSIS")
print("="*80)
if 'INBOUND' in master['Room'].values:
    inbound = master[master['Room'] == 'INBOUND']
    print(f"Total INBOUND rows: {len(inbound)}")
    
    # Check Deal ID patterns
    ae_codes = inbound[inbound['Deal Id'].astype(str).str.contains('AE', na=False, case=False)]
    print(f"INBOUND with AE codes: {len(ae_codes)}")
    
    # Check Stack Bulk matching
    inbound_with_data = inbound[inbound['Category'].notna() & (inbound['Category'].astype(str).str.strip() != '')]
    print(f"INBOUND with Stack Bulk data: {len(inbound_with_data)}")
    
    print("\nSample INBOUND Deal IDs:")
    print(inbound['Deal Id'].value_counts().head(10))

# Check 5: EVAL specific analysis
print("\n" + "="*80)
print("EVAL SPECIFIC ANALYSIS")
print("="*80)
if 'EVAL' in master['Room'].values:
    eval_df = master[master['Room'] == 'EVAL']
    print(f"Total EVAL rows: {len(eval_df)}")
    
    eval_with_data = eval_df[eval_df['Category'].notna() & (eval_df['Category'].astype(str).str.strip() != '')]
    print(f"EVAL with Stack Bulk data: {len(eval_with_data)}")
    
    print("\nSample EVAL Deal IDs:")
    print(eval_df['Deal Id'].value_counts().head(10))

# Check 6: LV ERROR BOX specific analysis
print("\n" + "="*80)
print("LV ERROR BOX SPECIFIC ANALYSIS")
print("="*80)
inventory = master[master['Room'] == 'Inventory']
if len(inventory) > 0:
    r151 = inventory[inventory['Location'] == 'R151']
    print(f"Total Inventory rows: {len(inventory)}")
    print(f"R151 (Error Box) rows: {len(r151)}")
    
    if len(r151) > 0:
        print(f"All R151 have 'No deal ID': {(r151['Deal Id'] == 'No deal ID').all()}")
        print(f"R151 with Stack Bulk data: {(r151['Category'].notna() & (r151['Category'].astype(str).str.strip() != '')).sum()}")

print("\n" + "="*80)
print("VERIFICATION COMPLETE")
print("="*80)
