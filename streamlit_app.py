# # streamlit_app.py

# import streamlit as st
# import pandas as pd
# import numpy as np
# from scipy.optimize import minimize
# import io

# st.set_page_config(page_title="Optimized Plantation Planner", layout="wide")

# st.title("🌳 Optimized Plantation Planner 🌳")
# st.write("Plan your tree plantation efficiently based on your desired total trees!")

# # ------------------- Input Section ------------------- #

# desired_total_trees = st.number_input(
#     "Enter Desired Total Number of Trees to Plant",
#     min_value=1000,
#     max_value=10000000,
#     value=3000000,
#     step=1000
# )

# spacing_adjustment_feet = 1
# minimum_trees_per_hectare = 900  # Density constraint

# # Tree data
# data = {
#     'Tree': ['Mango', 'Jackfruit', 'Guava', 'Bael', 'Gooseberry', 'Mahogani', 'Teak', 'Rosewood'],
#     'Target_Percentage': [13, 10, 10, 7, 25, 10, 20, 5],
#     'Spacing': [16.0, 14.0, 12.0, 12.0, 12.0, 9.0, 9.0, 9.0]  # in feet
# }

# df = pd.DataFrame(data)
# df['Adjusted_Spacing'] = df['Spacing'] - spacing_adjustment_feet
# df['Adjusted_Spacing'] = df['Adjusted_Spacing'].clip(lower=1.0)
# areas_per_tree = df['Adjusted_Spacing'] ** 2

# # ------------------- Optimization Functions ------------------- #

# def objective(x):
#     return np.sum(x * areas_per_tree)

# def total_tree_constraint(x):
#     return np.sum(x) - desired_total_trees

# def minimum_density_constraint(x):
#     total_area_used_sqft = np.sum(x * areas_per_tree)
#     total_area_used_hectare = total_area_used_sqft / 107639.104
#     density = np.sum(x) / total_area_used_hectare
#     return density - minimum_trees_per_hectare

# # ------------------- Optimization ------------------- #

# if st.button("Run Optimization 🚀"):
#     with st.spinner('Optimizing...'):
#         x0 = (df['Target_Percentage'] / 100 * desired_total_trees).astype(int)
#         bounds = [(0, None) for _ in range(len(df))]
#         constraints = []

#         for i in range(len(df)):
#             constraints.append({'type': 'ineq', 'fun': lambda x, i=i: (x[i] / np.sum(x)) * 100 - (df.loc[i, 'Target_Percentage'] - 1)})
#             constraints.append({'type': 'ineq', 'fun': lambda x, i=i: (df.loc[i, 'Target_Percentage'] + 1) - (x[i] / np.sum(x)) * 100})

#         constraints.append({'type': 'eq', 'fun': total_tree_constraint})
#         constraints.append({'type': 'ineq', 'fun': minimum_density_constraint})

#         result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

#         if result.success:
#             trees = np.round(result.x).astype(int)
#             df['Trees'] = trees
#             df['Final_Percentage'] = np.round((df['Trees'] / df['Trees'].sum()) * 100, 2)

#             total_trees = df['Trees'].sum()
#             total_area_used_sqft = np.sum(df['Trees'] * areas_per_tree)
#             total_area_used_hectare = total_area_used_sqft / 107639.104
#             density = total_trees / total_area_used_hectare

#             st.success('Optimization Successful! 🎯')

#             st.subheader("🌳 Plantation Plan Summary")
#             st.dataframe(df[['Tree', 'Final_Percentage', 'Adjusted_Spacing', 'Trees']])

#             col1, col2, col3 = st.columns(3)
#             col1.metric("Total Trees", f"{total_trees:,}")
#             col2.metric("Total Area (hectares)", f"{total_area_used_hectare:.2f}")
#             col3.metric("Density (trees/hectare)", f"{density:.2f}")

#             # ------------------- Download Option ------------------- #

#             output = io.BytesIO()
#             with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
#                 df.to_excel(writer, index=False, sheet_name='Plantation_Plan')
#                 summary_df = pd.DataFrame({
#                     "Metric": ["Total Trees", "Total Area (hectares)", "Density (trees/hectare)"],
#                     "Value": [total_trees, total_area_used_hectare, density]
#                 })
#                 summary_df.to_excel(writer, index=False, sheet_name='Summary')

#             output.seek(0)

#             st.download_button(
#                 label="📥 Download Plan as Excel",
#                 data=output,
#                 file_name="plantation_plan.xlsx",
#                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#             )
#         else:
#             st.error("Optimization failed. Please try again or adjust inputs.")


# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import io

st.set_page_config(page_title="Optimized Plantation Planner", layout="wide")

st.title("🌳 Optimized Plantation Planner 🌳")
st.write("Plan your tree plantation efficiently based on your desired total trees!")

# ------------------- Input Section ------------------- #

desired_total_trees = st.number_input(
    "Enter Desired Total Number of Trees to Plant",
    min_value=1000,
    max_value=10000000,
    value=3000000,
    step=1000
)

spacing_adjustment_feet = 1
minimum_trees_per_hectare = 900  # Density constraint

# Tree data
data = {
    'Tree': ['Mango', 'Jackfruit', 'Guava', 'Bael', 'Gooseberry', 'Mahogani', 'Teak', 'Rosewood'],
    'Target_Percentage': [13, 10, 10, 7, 25, 10, 20, 5],
    'Spacing': [16.0, 14.0, 12.0, 12.0, 12.0, 9.0, 9.0, 9.0]  # in feet
}

df = pd.DataFrame(data)
df['Adjusted_Spacing'] = df['Spacing'] - spacing_adjustment_feet
df['Adjusted_Spacing'] = df['Adjusted_Spacing'].clip(lower=1.0)
areas_per_tree = df['Adjusted_Spacing'] ** 2

# ------------------- Optimization Functions ------------------- #

def objective(x):
    return np.sum(x * areas_per_tree)

def total_tree_constraint(x):
    return np.sum(x) - desired_total_trees

def minimum_density_constraint(x):
    total_area_used_sqft = np.sum(x * areas_per_tree)
    total_area_used_hectare = total_area_used_sqft / 107639.104
    density = np.sum(x) / total_area_used_hectare
    return density - minimum_trees_per_hectare

# ------------------- Optimization ------------------- #

if st.button("Run Optimization 🚀"):
    with st.spinner('Optimizing...'):
        x0 = (df['Target_Percentage'] / 100 * desired_total_trees).astype(int)
        bounds = [(0, None) for _ in range(len(df))]
        constraints = []

        for i in range(len(df)):
            constraints.append({'type': 'ineq', 'fun': lambda x, i=i: (x[i] / np.sum(x)) * 100 - (df.loc[i, 'Target_Percentage'] - 1)})
            constraints.append({'type': 'ineq', 'fun': lambda x, i=i: (df.loc[i, 'Target_Percentage'] + 1) - (x[i] / np.sum(x)) * 100})

        constraints.append({'type': 'eq', 'fun': total_tree_constraint})
        constraints.append({'type': 'ineq', 'fun': minimum_density_constraint})

        result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

        if result.success:
            trees = np.round(result.x).astype(int)
            df['Trees'] = trees
            df['Final_Percentage'] = np.round((df['Trees'] / df['Trees'].sum()) * 100, 2)

            total_trees = df['Trees'].sum()
            total_area_used_sqft = np.sum(df['Trees'] * areas_per_tree)
            total_area_used_hectare = total_area_used_sqft / 107639.104
            density = total_trees / total_area_used_hectare

            st.success('Optimization Successful! 🎯')

            st.subheader("🌳 Plantation Plan Summary")
            st.dataframe(df[['Tree', 'Final_Percentage', 'Adjusted_Spacing', 'Trees']])

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Trees", f"{total_trees:,}")
            col2.metric("Total Area (hectares)", f"{total_area_used_hectare:.2f}")
            col3.metric("Density (trees/hectare)", f"{density:.2f}")

            # ------------------- Download Option ------------------- #

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Plantation_Plan')
                summary_df = pd.DataFrame({
                    "Metric": ["Total Trees", "Total Area (hectares)", "Density (trees/hectare)"],
                    "Value": [total_trees, total_area_used_hectare, density]
                })
                summary_df.to_excel(writer, index=False, sheet_name='Summary')

            output.seek(0)

            st.download_button(
                label="📥 Download Plan as Excel",
                data=output,
                file_name="plantation_plan.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("Optimization failed. Please try again or adjust inputs.")
