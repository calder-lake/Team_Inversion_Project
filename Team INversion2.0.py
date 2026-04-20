#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Team INversion mapping files 2.0
import pandas as pd
df6 = pd.read_csv('TriNetX_EMER_ICD10.csv')
print(df6.columns)


# In[3]:


#Team INversion mapping files 2.0
import pandas as pd
df6 = pd.read_csv('TriNetX_EMER_ICD10.csv')
df6.head()


# In[4]:


#fixing the age, finding trauma falls, struck, firearms


import pandas as pd
from datetime import datetime

# 1. Load the dataframe
df6 = pd.read_csv('TriNetX_EMER_ICD10.csv')

# 2. Calculate current age
current_year = datetime.now().year
df6['age'] = current_year - df6['year_of_birth']

# 3. Define the specific trauma prefixes
falls = ('W0', 'W1')
struck = ('W20', 'W21', 'W22')
firearms = ('W32', 'W33', 'W34')
target_trauma = falls + struck + firearms

# --- NEW CODE GOES HERE ---

# 4. Filter for the trauma codes
specific_trauma_df = df6[df6['code'].str.startswith(target_trauma, na=False)].copy()

# 5. Deduplicate (Removes the repeating rows for the same patient)
unique_trauma_df = specific_trauma_df.drop_duplicates(subset=['patient_id', 'code', 'age'])

# 6. Print results
print(f"Total records found: {len(specific_trauma_df)}")
print(f"Total unique patient-trauma instances: {len(unique_trauma_df)}")
print(unique_trauma_df[['patient_id', 'code', 'age']].head())


# In[5]:


import pandas as pd
from datetime import datetime

# 1. Load the dataframe
df6 = pd.read_csv('TriNetX_EMER_ICD10.csv')

# 2. ADD THIS BACK: Calculate age so the 'age' column exists
current_year = datetime.now().year
df6['age'] = current_year - df6['year_of_birth']

# 3. Define the specific trauma prefixes
falls = ('W0', 'W1')
struck = ('W20', 'W21', 'W22')
firearms = ('W32', 'W33', 'W34')
target_trauma = falls + struck + firearms

# 4. Filter
specific_trauma_df = df6[df6['code'].str.startswith(target_trauma, na=False)].copy()

# 5. Deduplicate (This will work now because 'age' exists!)
unique_trauma_df = specific_trauma_df.drop_duplicates(subset=['patient_id', 'code', 'age']).copy()

# 6. Categorize
def categorize(code):
    if code.startswith(falls): return 'Fall'
    if code.startswith(struck): return 'Struck'
    if code.startswith(firearms): return 'Firearm'
    return 'Other'

unique_trauma_df['category'] = unique_trauma_df['code'].apply(categorize)

# 7. Print the results
print("\nBreakdown by Trauma Type:")
print(unique_trauma_df['category'].value_counts())
print("\nAverage Age by Trauma Type:")
print(unique_trauma_df.groupby('category')['age'].mean())


# In[6]:


import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns  
from datetime import datetime
#1. Load the dataframe
df6 = pd.read_csv('TriNetX_EMER_ICD10.csv')
current_year = datetime.now().year
df6['age'] = current_year - df6['year_of_birth']

#More# 2. COMPLETENESS CHECK (Missing Values)
missing_codes = df6['code'].isnull().sum()
missing_patients = df6['patient_id'].isnull().sum()
missing_birth_years = df6['year_of_birth'].isnull().sum()

print(f"--- Completeness Check ---")
print(f"Missing Diagnosis Codes: {missing_codes}")
print(f"Missing Patient IDs: {missing_patients}")
print(f"Missing Birth Years: {missing_birth_years}")

# 3. PLAUSIBILITY CHECK (Impossible Ages)
# Uses the 'age' column you already created
implausible_ages = df6[(df6['age'] < 0) | (df6['age'] > 115)]

print(f"\n--- Plausibility Check ---")
print(f"Records with impossible ages (<0 or >115): {len(implausible_ages)}")

# 4. VISUALIZATION
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
sns.histplot(df6['age'].dropna(), bins=30, kde=True, color='teal')
plt.title('HIDQF Quality Check: Age Distribution of All Records in df6')
plt.show() 


# In[7]:


#Injury Type By Age
# Define common LOINC codes for TriNetX vitals
# Heart Rate: 8867-4, Systolic BP: 8480-6
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns  
from datetime import datetime
# 1. LOAD THE DATA (This fixes the NameError for df6)
df6 = pd.read_csv('TriNetX_EMER_ICD10.csv')

# 2. CALCULATE AGE (Necessary for deduplication later)
current_year = datetime.now().year
df6['age'] = current_year - df6['year_of_birth']
# 1. Ensure the trauma prefixes are defined
falls = ('W0', 'W1')
struck = ('W20', 'W21', 'W22')
firearms = ('W32', 'W33', 'W34')
target_trauma = falls + struck + firearms

# 3. Re-create specific_trauma_df (This fixes the NameError)
specific_trauma_df = df6[df6['code'].str.startswith(target_trauma, na=False)].copy()

# 4. Deduplicate
unique_trauma_df = specific_trauma_df.drop_duplicates(subset=['patient_id', 'code', 'age']).copy()

# 5. Process Vitals
hr_code = '8867-4'
sbp_code = '8480-6'

vitals_df = df6[df6['code_1'].isin([hr_code, sbp_code])].copy()

vitals_pivot = vitals_df.pivot_table(
    index=['patient_id', 'encounter_id', 'date'], 
    columns='code_1', 
    values='value', 
    aggfunc='first'
).reset_index()

vitals_pivot = vitals_pivot.rename(columns={hr_code: 'heart_rate', sbp_code: 'systolic_bp'})

# 6. Calculate Shock Index
vitals_pivot['shock_index'] = vitals_pivot['heart_rate'] / vitals_pivot['systolic_bp']

print("Shock Index calculated successfully!")
print(vitals_pivot.head())


# In[8]:


#Injury Type By Age, finding heart rate for shock index
# Define common LOINC codes for TriNetX vitals
# Heart Rate: 8867-4, Systolic BP: 8480-6
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns  
from datetime import datetime
# 1. LOAD THE DATA (This fixes the NameError for df6)
df6 = pd.read_csv('TriNetX_EMER_ICD10.csv')

# 2. CALCULATE AGE (Necessary for deduplication later)
current_year = datetime.now().year
df6['age'] = current_year - df6['year_of_birth']
# 1. Ensure the trauma prefixes are defined
falls = ('W0', 'W1')
struck = ('W20', 'W21', 'W22')
firearms = ('W32', 'W33', 'W34')
target_trauma = falls + struck + firearms

# 3. Re-create specific_trauma_df (This fixes the NameError)
specific_trauma_df = df6[df6['code'].str.startswith(target_trauma, na=False)].copy()

# 4. Deduplicate
unique_trauma_df = specific_trauma_df.drop_duplicates(subset=['patient_id', 'code', 'age']).copy()
# 5. CATEGORIZE the trauma (Required for the 'hue' in your graphs)
def categorize(code):
    if code.startswith(falls): return 'Fall'
    if code.startswith(struck): return 'Struck'
    if code.startswith(firearms): return 'Firearm'
    return 'Other'

unique_trauma_df['category'] = unique_trauma_df['code'].apply(categorize)

# 6. PROCESS VITALS (Pivoting from df6)
hr_code = '8867-4'
sbp_code = '8480-6'

vitals_df = df6[df6['code_1'].isin([hr_code, sbp_code])].copy()
vitals_pivot = vitals_df.pivot_table(
    index=['patient_id', 'encounter_id'], 
    columns='code_1', 
    values='value', 
    aggfunc='mean'
).reset_index()

vitals_pivot = vitals_pivot.rename(columns={hr_code: 'heart_rate', sbp_code: 'systolic_bp'})
vitals_pivot['shock_index'] = vitals_pivot['heart_rate'] / vitals_pivot['systolic_bp']

# 7. MERGE & CLEAN (This creates your final analysis table)
import numpy as np
df_analysis = pd.merge(unique_trauma_df, vitals_pivot, on=['patient_id', 'encounter_id'], how='inner')

# Clean up 'inf' and zeros
df_analysis = df_analysis[df_analysis['systolic_bp'] > 0].copy()
df_analysis.replace([np.inf, -np.inf], np.nan, inplace=True)
df_analysis.dropna(subset=['shock_index'], inplace=True)

# 8. VISUALIZE
plt.figure(figsize=(10, 5))
sns.kdeplot(data=df_analysis, x='age', hue='category', fill=True, palette='viridis')
plt.title('Injury Type Density by Age')
plt.show()

# Optional: Print that summary table we discussed
print(df_analysis.groupby('category')['shock_index'].mean())


# In[9]:


#Finding patients with shock
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns  
from datetime import datetime
# 1. LOAD THE DATA (This fixes the NameError for df6)
df6 = pd.read_csv('TriNetX_EMER_ICD10.csv')

# 2. CALCULATE AGE (Necessary for deduplication later)
current_year = datetime.now().year
df6['age'] = current_year - df6['year_of_birth']
# 1. Ensure the trauma prefixes are defined
falls = ('W0', 'W1')
struck = ('W20', 'W21', 'W22')
firearms = ('W32', 'W33', 'W34')
target_trauma = falls + struck + firearms

# 3. Re-create specific_trauma_df (This fixes the NameError)
specific_trauma_df = df6[df6['code'].str.startswith(target_trauma, na=False)].copy()

# 4. Deduplicate
unique_trauma_df = specific_trauma_df.drop_duplicates(subset=['patient_id', 'code', 'age']).copy()

# 1. Define the shock threshold
shock_threshold = 0.9

# 2. Filter for patients in early/hidden shock
hidden_shock_df = df_analysis[df_analysis['shock_index'] > shock_threshold]

# 3. Calculate counts and percentages
shock_counts = hidden_shock_df['category'].value_counts()
total_counts = df_analysis['category'].value_counts()
percentage_shock = (shock_counts / total_counts) * 100

# 4. Combine into a nice summary table
shock_summary = pd.DataFrame({
    'Total Patients': total_counts,
    'Patients in Shock (>0.9)': shock_counts,
    'Percentage (%)': percentage_shock
}).fillna(0) # Fill 0 if a category has no shock cases

print("--- Patients in Hidden Shock (>0.9) ---")
print(shock_summary.sort_values(by='Percentage (%)', ascending=False))


# In[10]:


import seaborn as sns
import matplotlib.pyplot as plt

# Plotting the Percentage in Shock
plt.figure(figsize=(10, 6))
ax = sns.barplot(
    x=shock_summary.index, 
    y=shock_summary['Percentage (%)'], 
    hue=shock_summary.index,  # Assign x to hue
    palette='Reds_r', 
    legend=False)

# Add labels on top of bars
for p in ax.patches:
    ax.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', xytext=(0, 9), textcoords='offset points')

plt.title('Percentage of Patients in "Hidden Shock" (SI > 0.9)', fontsize=14)
plt.ylabel('Percentage of Category (%)')
plt.ylim(0, max(percentage_shock) + 2) # Give some space for labels
plt.show()


# In[11]:


#shock by age
import seaborn as sns
import matplotlib.pyplot as plt


# 1. Create age groups (decades) to smooth the data
df_analysis['age_decade'] = (df_analysis['age'] // 10) * 10

# 2. Calculate the % in shock per decade and category
df_analysis['in_shock_binary'] = (df_analysis['shock_index'] > 0.9).astype(int)
shock_trend = df_analysis.groupby(['age_decade', 'category'])['in_shock_binary'].mean().reset_index()

# 3. Create a clean Line Plot
plt.figure(figsize=(12, 6))
sns.lineplot(data=shock_trend, x='age_decade', y='in_shock_binary', 
             hue='category', marker='o', linewidth=2.5)

# 4. Clean up the styling
plt.title('Probability of Hidden Shock by Age Decade', fontsize=15)
plt.ylabel('Probability of Shock Index > 0.9', fontsize=12)
plt.xlabel('Age Group (Decades)', fontsize=12)
plt.xticks(range(20, 90, 10)) # Sets clear 10-year markers
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.legend(title='Trauma Category', frameon=True)

plt.show()


# In[12]:


#Trauma patients by region

#1. Aggregate unique patients by region
regional_counts = df_analysis.groupby('patient_regional_location')['patient_id'].nunique().sort_values(ascending=False)
region_map = {
    'Pacific': 'West', 'Mountain': 'West',
    'West North Central': 'Midwest', 'East North Central': 'Midwest',
    'New England': 'Northeast', 'Middle Atlantic': 'Northeast',
    'West South Central': 'South', 'East South Central': 'South', 'South Atlantic': 'South'
}

# Apply the mapping
df_analysis['census_region'] = df_analysis['patient_regional_location'].map(region_map)

# Plot the breakdown
plt.figure(figsize=(10,6))
sns.countplot(data=df_analysis, x='census_region', hue='category', palette='viridis')
plt.title('Trauma Cases by US Census Region')
plt.show()
# 2. Visualize the distribution
plt.figure(figsize=(12, 6))
sns.barplot(
    x=regional_counts.index, 
    y=regional_counts.values, 
    hue=regional_counts.index, 
    palette='magma', 
    legend=False
)

plt.title('Unique Trauma Patients by Regional Location')
plt.xlabel('Region')
plt.ylabel('Unique Patient Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3. Print the summary
print("Regional Distribution Summary:")
print(regional_counts)


# In[13]:


print(df_analysis['patient_regional_location'].unique())


# In[14]:


# 1. Distribution of Trauma Categories by Gender
plt.figure(figsize=(10, 6))
sns.countplot(data=df_analysis, x='category', hue='sex', palette='coolwarm')
plt.title('Trauma Categories by Gender')
plt.ylabel('Number of Records')
plt.xlabel('Injury Category')
plt.legend(title='Gender')
plt.show()

# 2. Percentage Breakdown
gender_counts = df_analysis.groupby(['sex', 'category']).size().unstack(fill_value=0)
gender_percentages = gender_counts.div(gender_counts.sum(axis=1), axis=0) * 100

print("--- Percentage of Injury Types Within Each Gender ---")
print(gender_percentages.round(2))


# In[ ]:




