





# import streamlit as st
# import pandas as pd
# import numpy as np
# from scipy.optimize import minimize

# st.set_page_config(page_title="Tree Plantation Optimizer", layout="wide")

# st.title("🌳 Navchetna Tree Plantation Optimizer")

# # ------------------- Inputs ------------------- #

# st.sidebar.header("🔧 Configuration")

# desired_total_trees = st.sidebar.number_input("🌲 Desired Total Trees (Minimum)", min_value=1000, value=22500, step=100)
# minimum_trees_per_hectare = st.sidebar.number_input("🌱 Minimum Density (trees/hectare)", min_value=100, value=878, step=10)

# spacing_adjustment_feet = st.sidebar.slider("📏 Spacing Adjustment (feet)", min_value=0.0, max_value=5.0, value=1.0, step=0.1)
# target_percentage_tolerance = st.sidebar.slider("📊 Target Percentage Tolerance (±%)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)

# st.sidebar.markdown("---")

# # ------------------- Default Tree Table ------------------- #
# st.subheader("🌿 Tree Species Configuration")

# default_data = {
#     'Tree': ['Mango', 'Jackfruit', 'Guava', 'Bael', 'Gooseberry', 'Mahogani', 'Teak', 'Rosewood'],
#     # 'Target_Percentage': [11, 10, 10, 7, 25, 12, 20, 5],
#     # 'Spacing': [18.0, 12.0, 9.0, 9.0, 12.0, 7.0, 7.0, 12.0]
#     'Target_Percentage': [13, 10, 10, 7, 25, 10, 20, 5],
#     'Spacing': [15.0, 14.0, 12.0, 12.0, 12.0, 8.0, 8.0, 8.0]
# }

# df_input = pd.DataFrame(default_data)

# st.write("You can edit the Target % and Spacing below or add more rows:")

# edited_df = st.data_editor(df_input, num_rows="dynamic")

# run_opt = st.button("🚀 Run Optimization")

# if run_opt:
#     df = edited_df.copy()

#     # Apply spacing adjustment
#     df['Adjusted_Spacing'] = df['Spacing'] - spacing_adjustment_feet
#     df['Adjusted_Spacing'] = df['Adjusted_Spacing'].clip(lower=1.0)

#     areas_per_tree = df['Adjusted_Spacing'] ** 2  # in sqft

#     # ------------------- Optimization Setup ------------------- #

#     def objective(x):
#         return np.sum(x * areas_per_tree)  # Minimize total area used

#     def min_total_tree_constraint(x):
#         return np.sum(x) - desired_total_trees  # Must be >= desired

#     def minimum_density_constraint(x):
#         total_area_sqft = np.sum(x * areas_per_tree)
#         total_area_hectares = total_area_sqft / 107639.104
#         density = np.sum(x) / total_area_hectares
#         return density - minimum_trees_per_hectare

#     # Initial guess
#     x0 = (df['Target_Percentage'] / 100 * desired_total_trees).astype(int)

#     bounds = [(0, None) for _ in range(len(df))]

#     constraints = []

#     for i in range(len(df)):
#         constraints.append({
#             'type': 'ineq',
#             'fun': lambda x, i=i: (x[i] / np.sum(x)) * 100 - (df.loc[i, 'Target_Percentage'] - target_percentage_tolerance)
#         })
#         constraints.append({
#             'type': 'ineq',
#             'fun': lambda x, i=i: (df.loc[i, 'Target_Percentage'] + target_percentage_tolerance) - (x[i] / np.sum(x)) * 100
#         })

#     constraints.append({'type': 'ineq', 'fun': min_total_tree_constraint})
#     constraints.append({'type': 'ineq', 'fun': minimum_density_constraint})

#     # ------------------- Run Optimization ------------------- #
#     result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

#     # ------------------- Output ------------------- #
#     if result.success:
#         trees = np.round(result.x).astype(int)
#         df['Trees'] = trees
#         df['Final_Percentage'] = np.round((df['Trees'] / df['Trees'].sum()) * 100, 2)

#         total_trees = df['Trees'].sum()
#         total_area_used_sqft = np.sum(df['Trees'] * areas_per_tree)
#         total_area_used_hectare = total_area_used_sqft / 107639.104
#         density = total_trees / total_area_used_hectare

#         st.success("✅ Optimization successful!")

#         st.subheader("📋 Optimized Plantation Plan")
#         st.dataframe(df[['Tree', 'Final_Percentage', 'Adjusted_Spacing', 'Trees']], use_container_width=True)

#         st.markdown(f"**Total Trees:** {total_trees}")
#         st.markdown(f"**Total Area Used:** {total_area_used_sqft:,.2f} sqft ({total_area_used_hectare:.2f} hectares)")
#         st.markdown(f"**Achieved Density:** {density:.2f} trees/hectare")
#         st.markdown(f"**Total Percentage:** {df['Final_Percentage'].sum():.2f}%")

#         # CSV Download
#         csv = df.to_csv(index=False)
#         st.download_button("⬇️ Download Output as CSV", csv, file_name="optimized_plantation.csv", mime="text/csv")
#     else:
#         st.error("⚠️ Optimization failed. Try adjusting parameters.")






import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import minimize

st.set_page_config(page_title="Tree Plantation Optimizer", layout="wide")

st.title("🌳 Navchetna Tree Plantation Optimizer")

# ------------------- Inputs ------------------- #

st.sidebar.header("🔧 Configuration")

desired_total_trees = st.sidebar.number_input("🌲 Desired Total Trees (Minimum)", min_value=1000, value=22500, step=100)
minimum_trees_per_hectare = st.sidebar.number_input("🌱 Minimum Density (trees/hectare)", min_value=100, value=878, step=10)

spacing_adjustment_feet = st.sidebar.slider("📏 Spacing Adjustment (feet)", min_value=0.0, max_value=5.0, value=1.0, step=0.1)
target_percentage_tolerance = st.sidebar.slider("📊 Target Percentage Tolerance (±%)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)

st.sidebar.markdown("---")

# ------------------- Default Tree Table ------------------- #
st.subheader("🌿 Tree Species Configuration")

default_data = {
    'Tree': ['Mango', 'Jackfruit', 'Guava', 'Bael', 'Gooseberry', 'Mahogani', 'Teak', 'Rosewood'],
    'Target_Percentage': [13, 10, 10, 7, 25, 10, 20, 5],
    'Spacing': [15.0, 14.0, 12.0, 12.0, 12.0, 8.0, 8.0, 8.0]
}

df_input = pd.DataFrame(default_data)

st.write("You can edit the Target % and Spacing below or add/remove rows:")

edited_df = st.data_editor(df_input, num_rows="dynamic")

run_opt = st.button("🚀 Run Optimization")

if run_opt:
    df = edited_df.copy()

    # Convert columns to numeric and drop NaNs (in case user deletes rows)
    df['Target_Percentage'] = pd.to_numeric(df['Target_Percentage'], errors='coerce')
    df['Spacing'] = pd.to_numeric(df['Spacing'], errors='coerce')
    df = df.dropna(subset=['Target_Percentage', 'Spacing'])

    # Check if target percentages sum to 100
    total_percentage = df['Target_Percentage'].sum()
    if not np.isclose(total_percentage, 100.0, atol=0.1):
        st.error(f"❌ The total of Target Percentages must be 100%. Currently, it is {total_percentage:.2f}%.")
    elif df.empty:
        st.error("❌ No valid data to optimize. Please check the table.")
    else:
        # Apply spacing adjustment
        df['Adjusted_Spacing'] = df['Spacing'] - spacing_adjustment_feet
        df['Adjusted_Spacing'] = df['Adjusted_Spacing'].clip(lower=1.0)

        areas_per_tree = df['Adjusted_Spacing'] ** 2  # in sqft

        # ------------------- Optimization Setup ------------------- #

        def objective(x):
            return np.sum(x * areas_per_tree)  # Minimize total area used

        def min_total_tree_constraint(x):
            return np.sum(x) - desired_total_trees  # Must be >= desired

        def minimum_density_constraint(x):
            total_area_sqft = np.sum(x * areas_per_tree)
            total_area_hectares = total_area_sqft / 107639.104
            density = np.sum(x) / total_area_hectares
            return density - minimum_trees_per_hectare

        # Initial guess
        x0 = (df['Target_Percentage'] / 100 * desired_total_trees).astype(int)

        bounds = [(0, None) for _ in range(len(df))]

        constraints = []

        for i in range(len(df)):
            constraints.append({
                'type': 'ineq',
                'fun': lambda x, i=i: (x[i] / np.sum(x)) * 100 - (df.loc[i, 'Target_Percentage'] - target_percentage_tolerance)
            })
            constraints.append({
                'type': 'ineq',
                'fun': lambda x, i=i: (df.loc[i, 'Target_Percentage'] + target_percentage_tolerance) - (x[i] / np.sum(x)) * 100
            })

        constraints.append({'type': 'ineq', 'fun': min_total_tree_constraint})
        constraints.append({'type': 'ineq', 'fun': minimum_density_constraint})

        # ------------------- Run Optimization ------------------- #
        result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

        # ------------------- Output ------------------- #
        if result.success:
            trees = np.round(result.x).astype(int)
            df['Trees'] = trees
            df['Final_Percentage'] = np.round((df['Trees'] / df['Trees'].sum()) * 100, 2)

            total_trees = df['Trees'].sum()
            total_area_used_sqft = np.sum(df['Trees'] * areas_per_tree)
            total_area_used_hectare = total_area_used_sqft / 107639.104
            density = total_trees / total_area_used_hectare

            st.success("✅ Optimization successful!")

            st.subheader("📋 Optimized Plantation Plan")
            st.dataframe(df[['Tree', 'Final_Percentage', 'Adjusted_Spacing', 'Trees']], use_container_width=True)

            st.markdown(f"**Total Trees:** {total_trees}")
            st.markdown(f"**Total Area Used:** {total_area_used_sqft:,.2f} sqft ({total_area_used_hectare:.2f} hectares)")
            st.markdown(f"**Achieved Density:** {density:.2f} trees/hectare")
            st.markdown(f"**Total Percentage:** {df['Final_Percentage'].sum():.2f}%")

            # CSV Download
            csv = df.to_csv(index=False)
            st.download_button("⬇️ Download Output as CSV", csv, file_name="optimized_plantation.csv", mime="text/csv")
        else:
            st.error("⚠️ Optimization failed. Try adjusting parameters.")
