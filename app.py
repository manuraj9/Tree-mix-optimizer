# import streamlit as st
# import pandas as pd
# import numpy as np
# from scipy.optimize import minimize

# st.title("🌳 Tree Plantation Optimizer")

# st.markdown("Enter your initial inputs below:")

# # Total number of trees
# total_trees = st.number_input("🌱 Total Number of Trees", min_value=100, value=900)

# # Trees per hectare
# trees_per_hectare = st.number_input("🌿 Desired Trees per Hectare", min_value=100, value=900)

# # Editable table for tree inputs
# default_data = {
#     'Tree': ['Mango', 'Jackfruit', 'Guava', 'Bael', 'Gooseberry', 'Mahogani', 'Teak', 'Rosewood'],
#     'Target_Percentage': [13, 10, 10, 7, 25, 10, 20, 5],
#     'Spacing': [16.0, 14.0, 12.0, 12.0, 12.0, 9.0, 9.0, 9.0]
# }

# df_input = pd.DataFrame(default_data)
# edited_df = st.data_editor(df_input, num_rows="dynamic", use_container_width=True)

# if st.button("🚀 Run Optimization"):
#     df = edited_df.copy()
#     df['Adjusted_Spacing'] = df['Spacing'] - 1
#     df['Adjusted_Spacing'] = df['Adjusted_Spacing'].clip(lower=1.0)
#     area_per_tree = df['Adjusted_Spacing'] ** 2

#     total_area_required_sqft = np.sum((df['Target_Percentage'] / 100) * total_trees * area_per_tree)
#     total_area_required_hectare = total_area_required_sqft / 107639.104

#     x0 = (df['Target_Percentage'] / 100 * total_trees).astype(int)

#     bounds = [(0, None) for _ in range(len(df))]

#     def objective(x):
#         return -np.sum(x)

#     def percentage_constraints(x):
#         total = np.sum(x)
#         return [(x[i] / total) * 100 - (df.loc[i, 'Target_Percentage'] - 1) for i in range(len(df))] + \
#                [(df.loc[i, 'Target_Percentage'] + 1) - (x[i] / total) * 100 for i in range(len(df))]

#     def area_constraint(x):
#         return total_area_required_sqft - np.sum(x * area_per_tree)

#     def min_density_constraint(x):
#         hectare_area = np.sum(x * area_per_tree) / 107639.104
#         return (np.sum(x) / hectare_area) - trees_per_hectare

#     constraints = [{'type': 'ineq', 'fun': lambda x, i=i: (x[i]/np.sum(x))*100 - (df.loc[i, 'Target_Percentage'] - 1)} for i in range(len(df))] + \
#                   [{'type': 'ineq', 'fun': lambda x, i=i: (df.loc[i, 'Target_Percentage'] + 1) - (x[i]/np.sum(x))*100} for i in range(len(df))] + \
#                   [{'type': 'ineq', 'fun': area_constraint},
#                    {'type': 'ineq', 'fun': min_density_constraint}]

#     result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

#     if result.success:
#         trees = np.round(result.x).astype(int)
#         df['Trees'] = trees
#         df['Final_Percentage'] = np.round((df['Trees'] / df['Trees'].sum()) * 100, 2)

#         total_planted = df['Trees'].sum()
#         area_sqft = np.sum(df['Trees'] * area_per_tree)
#         area_hectare = area_sqft / 107639.104
#         density = total_planted / area_hectare

#         st.subheader("📊 Optimized Plantation Plan")
#         st.dataframe(df[['Tree', 'Final_Percentage', 'Adjusted_Spacing', 'Trees']], use_container_width=True)

#         st.success(f"🌱 Total Trees: {total_planted}")
#         st.success(f"🌍 Area Required: {area_hectare:.2f} hectares")
#         st.success(f"🌿 Trees per Hectare: {density:.2f}")
#     else:
#         st.error("⚠️ Optimization failed. Try adjusting the percentages or spacing.")




# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# from scipy.optimize import minimize

# st.set_page_config(page_title="Tree Plantation Optimizer", layout="wide")
# st.title("🌳 Tree Plantation Optimizer")

# # User Inputs
# st.sidebar.header("User Inputs")
# total_trees = st.sidebar.number_input("Total Trees to Plant", min_value=1, value=900)
# trees_per_hectare = st.sidebar.number_input("Minimum Trees per Hectare", min_value=1, value=900)

# percent_adjustable = st.sidebar.number_input("Adjustable Percentage (+/- %)", min_value=0.0, value=1.0, step=0.1)
# distance_adjustable = st.sidebar.number_input("Spacing Adjustment (ft)", min_value=0.0, value=1.0, step=0.1)

# st.write("### Initial Tree Data Table")
# if "tree_data" not in st.session_state:
#     st.session_state.tree_data = pd.DataFrame({
#         'Tree': ['Mango', 'Jackfruit', 'Guava', 'Bael', 'Gooseberry', 'Mahogani', 'Teak', 'Rosewood'],
#         'Target_Percentage': [13, 10, 10, 7, 25, 10, 20, 5],
#         'Spacing': [16.0, 14.0, 12.0, 12.0, 12.0, 9.0, 9.0, 9.0]
#     })

# if st.button("➕ Add New Tree Type"):
#     new_row = pd.DataFrame([{'Tree': 'NewTree', 'Target_Percentage': 0, 'Spacing': 1.0}])
#     st.session_state.tree_data = pd.concat([st.session_state.tree_data, new_row], ignore_index=True)

# df = st.data_editor(st.session_state.tree_data, use_container_width=True, num_rows="dynamic")
# st.session_state.tree_data = df.copy()

# if st.button("Run Optimization"):
#     n = len(df)

#     # Adjusted spacing
#     df['Adjusted_Spacing'] = df['Spacing'] - distance_adjustable
#     df['Adjusted_Spacing'] = df['Adjusted_Spacing'].clip(lower=1.0)
#     areas_per_tree = df['Adjusted_Spacing'] ** 2

#     # Calculate average area per tree and total area needed
#     avg_area_per_tree = np.sum(areas_per_tree * df['Target_Percentage']) / 100
#     total_area_required_sqft = total_trees * avg_area_per_tree
#     total_area_hectare = total_area_required_sqft / 107639.104

#     # Optimization setup
#     def objective(x):
#         return -np.sum(x)

#     def area_constraint(x):
#         return total_area_required_sqft - np.sum(x * areas_per_tree)

#     def minimum_tree_constraint(x):
#         return np.sum(x) - total_trees

#     def trees_per_hectare_constraint(x):
#         total_hectares = np.sum(x * areas_per_tree) / 107639.104
#         return (np.sum(x) / total_hectares) - trees_per_hectare

#     # Initial guess and bounds
#     x0 = (df['Target_Percentage'] / 100 * total_trees).astype(int).values
#     bounds = [(0, None) for _ in range(n)]
#     constraints = []

#     for i in range(n):
#         lower_bound = (df.loc[i, 'Target_Percentage'] - percent_adjustable) / 100 * total_trees
#         upper_bound = (df.loc[i, 'Target_Percentage'] + percent_adjustable) / 100 * total_trees
#         constraints.append({'type': 'ineq', 'fun': lambda x, i=i, lb=lower_bound: x[i] - lb})
#         constraints.append({'type': 'ineq', 'fun': lambda x, i=i, ub=upper_bound: ub - x[i]})

#     constraints.append({'type': 'ineq', 'fun': area_constraint})
#     constraints.append({'type': 'eq', 'fun': minimum_tree_constraint})
#     constraints.append({'type': 'ineq', 'fun': trees_per_hectare_constraint})

#     result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

#     if result.success:
#         trees = np.round(result.x).astype(int)
#         df['Trees'] = trees
#         df['Final_Percentage'] = np.round((df['Trees'] / df['Trees'].sum()) * 100, 2)

#         total_trees_final = df['Trees'].sum()
#         total_area_used = np.sum(df['Trees'] * areas_per_tree)
#         used_area_hectare = total_area_used / 107639.104
#         trees_per_hectare_actual = total_trees_final / used_area_hectare

#         st.success("Optimization Successful!")
#         st.write("### 🌱 Optimized Plantation Plan")
#         st.dataframe(df[['Tree', 'Final_Percentage', 'Adjusted_Spacing', 'Trees']])

#         st.markdown(f"**Total Trees Planted:** {total_trees_final}")
#         st.markdown(f"**Total Area Required:** {total_area_used:,.2f} sqft ({used_area_hectare:.2f} hectare)")
#         st.markdown(f"**Trees per Hectare (Achieved):** {trees_per_hectare_actual:.2f}")
#         st.markdown(f"**Total Percentage:** {df['Final_Percentage'].sum():.2f}%")

#         fig = px.pie(df, names='Tree', values='Trees', title='Tree Distribution')
#         st.plotly_chart(fig, use_container_width=True)

#         fig2 = px.bar(df, x='Tree', y='Adjusted_Spacing', title='Adjusted Spacing per Tree', text_auto=True)
#         st.plotly_chart(fig2, use_container_width=True)

#     else:
#         st.error("Optimization failed. Try different inputs.")




#ooooooooooookkkkkk

# import streamlit as st
# import pandas as pd
# import numpy as np
# from scipy.optimize import minimize

# st.title("🌳 Tree Plantation Optimizer")

# st.markdown("Enter your initial inputs below:")

# # Total number of trees
# total_trees = st.number_input("🌱 Total Number of Trees", min_value=100, value=900)

# # Desired Trees per Hectare
# trees_per_hectare = st.number_input("🌿 Desired Trees per Hectare", min_value=100, value=900)

# # Adjustable percentage tolerance
# percent_adjustable = st.slider("📊 Allowable Percentage Variation (±%)", min_value=0, max_value=10, value=1)

# # Adjustable spacing variation
# spacing_variation = st.slider("📏 Spacing Reduction (in feet)", min_value=0, max_value=5, value=1)

# # Default data for tree types
# default_data = {
#     'Tree': ['Mango', 'Jackfruit', 'Guava', 'Bael', 'Gooseberry', 'Mahogani', 'Teak', 'Rosewood'],
#     'Target_Percentage': [13, 10, 10, 7, 25, 10, 20, 5],
#     'Spacing': [16.0, 14.0, 12.0, 12.0, 12.0, 9.0, 9.0, 9.0]
# }

# df_input = pd.DataFrame(default_data)

# # Editable DataFrame with option to add more rows
# edited_df = st.data_editor(df_input, num_rows="dynamic", use_container_width=True)

# if st.button("🚀 Run Optimization"):
#     df = edited_df.copy()

#     # Adjust spacing
#     df['Adjusted_Spacing'] = (df['Spacing'] - spacing_variation).clip(lower=1.0)
#     area_per_tree = df['Adjusted_Spacing'] ** 2  # in square feet

#     total_area_required_sqft = np.sum((df['Target_Percentage'] / 100) * total_trees * area_per_tree)
#     total_area_required_hectare = total_area_required_sqft / 107639.104

#     x0 = (df['Target_Percentage'] / 100 * total_trees).astype(int)
#     bounds = [(0, None) for _ in range(len(df))]

#     def objective(x):
#         return 0  # Minimize nothing; constraints will shape the solution

#     def area_constraint(x):
#         return total_area_required_sqft - np.sum(x * area_per_tree)

#     def min_density_constraint(x):
#         hectare_area = np.sum(x * area_per_tree) / 107639.104
#         return (np.sum(x) / hectare_area) - trees_per_hectare

#     def total_trees_constraint(x):
#         return total_trees - np.sum(x)

#     # Constraints list
#     constraints = [
#         {'type': 'ineq', 'fun': lambda x, i=i: (x[i] / np.sum(x)) * 100 - (df.loc[i, 'Target_Percentage'] - percent_adjustable)}
#         for i in range(len(df))
#     ] + [
#         {'type': 'ineq', 'fun': lambda x, i=i: (df.loc[i, 'Target_Percentage'] + percent_adjustable) - (x[i] / np.sum(x)) * 100}
#         for i in range(len(df))
#     ] + [
#         {'type': 'ineq', 'fun': area_constraint},
#         {'type': 'ineq', 'fun': min_density_constraint},
#         {'type': 'eq', 'fun': total_trees_constraint}
#     ]

#     result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

#     if result.success:
#         trees = np.round(result.x).astype(int)
#         df['Trees'] = trees
#         df['Final_Percentage'] = np.round((df['Trees'] / df['Trees'].sum()) * 100, 2)

#         total_planted = df['Trees'].sum()
#         area_sqft = np.sum(df['Trees'] * area_per_tree)
#         area_hectare = area_sqft / 107639.104
#         density = total_planted / area_hectare

#         st.subheader("📊 Optimized Plantation Plan")
#         st.dataframe(df[['Tree', 'Final_Percentage', 'Adjusted_Spacing', 'Trees']], use_container_width=True)

#         st.success(f"🌱 Total Trees: {total_planted}")
#         st.success(f"🌍 Area Required: {area_hectare:.2f} hectares")
#         st.success(f"🌿 Trees per Hectare: {density:.2f}")

#         # Download button
#         csv = df.to_csv(index=False)
#         st.download_button("📥 Download Plan as CSV", csv, "optimized_plantation_plan.csv", "text/csv")
#     else:
#         st.error("⚠️ Optimization failed. Try adjusting the percentages or spacing.")




# import streamlit as st
# import pandas as pd
# import numpy as np
# from scipy.optimize import minimize

# st.title("🌳 Tree Plantation Optimizer")

# # ------------------- Inputs ------------------- #
# desired_total_trees = st.number_input("🌱 Desired Total Number of Trees", min_value=100, value=22500)
# minimum_trees_per_hectare = st.number_input("🌾 Minimum Trees per Hectare", min_value=100, value=878)
# spacing_adjustment_feet = st.slider("📏 Spacing Adjustment (feet)", min_value=0, max_value=5, value=1)
# target_percentage_tolerance = st.slider("📊 Target Percentage Tolerance (±%)", min_value=0, max_value=10, value=1)

# st.markdown("### 🌴 Tree Details (editable table)")
# default_data = {
#     'Tree': ['Mango', 'Jackfruit', 'Guava', 'Bael', 'Gooseberry', 'Mahogani', 'Teak', 'Rosewood'],
#     'Target_Percentage': [11, 10, 10, 7, 25, 12, 20, 5],
#     'Spacing': [18.0, 12.0, 9.0, 9.0, 12.0, 7.0, 7.0, 12.0]  # in feet
# }
# df_input = pd.DataFrame(default_data)

# tree_df = st.data_editor(df_input, num_rows="dynamic", use_container_width=True)

# if st.button("🚀 Run Optimization"):
#     df = tree_df.copy()

#     # Adjust spacing
#     df['Adjusted_Spacing'] = (df['Spacing'] - spacing_adjustment_feet).clip(lower=1.0)
#     areas_per_tree = df['Adjusted_Spacing'] ** 2  # sqft per tree

#     # Initial guess
#     x0 = (df['Target_Percentage'] / 100 * desired_total_trees).astype(int)

#     # Objective: Minimize total area
#     def objective(x):
#         return np.sum(x * areas_per_tree)

#     # Constraints
#     def total_tree_constraint(x):
#         return np.sum(x) - desired_total_trees

#     def minimum_density_constraint(x):
#         total_area_sqft = np.sum(x * areas_per_tree)
#         total_area_hectare = total_area_sqft / 107639.104
#         density = np.sum(x) / total_area_hectare
#         return density - minimum_trees_per_hectare

#     constraints = []

#     # Percentage constraints
#     for i in range(len(df)):
#         constraints.append({'type': 'ineq', 'fun': lambda x, i=i: (x[i] / np.sum(x)) * 100 - (df.loc[i, 'Target_Percentage'] - target_percentage_tolerance)})
#         constraints.append({'type': 'ineq', 'fun': lambda x, i=i: (df.loc[i, 'Target_Percentage'] + target_percentage_tolerance) - (x[i] / np.sum(x)) * 100})

#     constraints.append({'type': 'eq', 'fun': total_tree_constraint})
#     constraints.append({'type': 'ineq', 'fun': minimum_density_constraint})

#     # Bounds
#     bounds = [(0, None) for _ in range(len(df))]

#     # Optimization
#     result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

#     if result.success:
#         trees = np.round(result.x).astype(int)
#         df['Trees'] = trees
#         df['Final_Percentage'] = np.round((df['Trees'] / df['Trees'].sum()) * 100, 2)

#         total_trees = df['Trees'].sum()
#         total_area_used_sqft = np.sum(df['Trees'] * areas_per_tree)
#         total_area_used_hectare = total_area_used_sqft / 107639.104
#         density = total_trees / total_area_used_hectare

#         st.success("✅ Optimization successful!")
#         st.dataframe(df[['Tree', 'Final_Percentage', 'Adjusted_Spacing', 'Trees']], use_container_width=True)

#         st.markdown(f"**🌱 Total Trees Planted:** {total_trees}")
#         st.markdown(f"**🌍 Total Area Used:** {total_area_used_sqft:,.2f} sqft / {total_area_used_hectare:.2f} hectares")
#         st.markdown(f"**📈 Achieved Density:** {density:.2f} trees per hectare")
#         st.markdown(f"**📊 Final Percentages Total:** {df['Final_Percentage'].sum():.2f}%")

#         # Download button
#         csv = df.to_csv(index=False)
#         st.download_button("📥 Download CSV", csv, "optimized_plantation.csv", "text/csv")
#     else:
#         st.error("⚠️ Optimization failed. Try adjusting the inputs or constraints.")




# import streamlit as st
# import pandas as pd
# import numpy as np
# from scipy.optimize import minimize

# st.set_page_config(page_title="Tree Plantation Optimizer", layout="wide")

# st.title("🌳 Tree Plantation Optimizer")

# # ------------------- Inputs ------------------- #

# st.sidebar.header("🔧 Configuration")

# desired_total_trees = st.sidebar.number_input("🌲 Desired Total Trees", min_value=1000, value=22500, step=100)
# minimum_trees_per_hectare = st.sidebar.number_input("🌱 Minimum Density (trees/hectare)", min_value=100, value=878, step=10)

# spacing_adjustment_feet = st.sidebar.slider("📏 Spacing Adjustment (feet)", min_value=0.0, max_value=5.0, value=1.0, step=0.1)
# target_percentage_tolerance = st.sidebar.slider("📊 Target Percentage Tolerance (±%)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)

# st.sidebar.markdown("---")

# # ------------------- Default Tree Table ------------------- #
# st.subheader("🌿 Tree Species Configuration")

# default_data = {
#     'Tree': ['Mango', 'Jackfruit', 'Guava', 'Bael', 'Gooseberry', 'Mahogani', 'Teak', 'Rosewood'],
#     'Target_Percentage': [11, 10, 10, 7, 25, 12, 20, 5],
#     'Spacing': [18.0, 12.0, 9.0, 9.0, 12.0, 7.0, 7.0, 12.0]
# }

# df_input = pd.DataFrame(default_data)

# st.write("You can edit the Target % and Spacing below or add more trees:")
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
#         return np.sum(x * areas_per_tree)

#     def total_tree_constraint(x):
#         return np.sum(x) - desired_total_trees

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

#     constraints.append({'type': 'eq', 'fun': total_tree_constraint})
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




# import streamlit as st
# import pandas as pd
# import numpy as np
# from scipy.optimize import minimize

# st.set_page_config(page_title="Tree Plantation Optimizer", layout="wide")

# st.title("🌳 Tree Plantation Optimizer")

# # ------------------- Inputs ------------------- #

# st.sidebar.header("🔧 Configuration")

# desired_total_trees = st.sidebar.number_input("🌲 Desired Total Trees", min_value=1000, value=22500, step=100)
# minimum_trees_per_hectare = st.sidebar.number_input("🌱 Minimum Density (trees/hectare)", min_value=100, value=878, step=10)

# spacing_adjustment_feet = st.sidebar.slider("📏 Spacing Adjustment (feet)", min_value=0.0, max_value=5.0, value=1.0, step=0.1)
# target_percentage_tolerance = st.sidebar.slider("📊 Target Percentage Tolerance (±%)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)

# st.sidebar.markdown("---")

# # ------------------- Default Tree Table ------------------- #
# st.subheader("🌿 Tree Species Configuration")

# default_data = {
#     'Tree': ['Mango', 'Jackfruit', 'Guava', 'Bael', 'Gooseberry', 'Mahogani', 'Teak', 'Rosewood'],
#     'Target_Percentage': [11, 10, 10, 7, 25, 12, 20, 5],
#     'Spacing': [18.0, 12.0, 9.0, 9.0, 12.0, 7.0, 7.0, 12.0]
# }

# df_input = pd.DataFrame(default_data)

# st.write("You can edit the Target % and Spacing below or add more trees:")
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
#         return np.sum(x * areas_per_tree)

#     def total_tree_constraint(x):
#         return np.sum(x) - desired_total_trees

#     def minimum_density_constraint(x):
#         total_area_sqft = np.sum(x * areas_per_tree)
#         total_area_hectares = total_area_sqft / 107639.104
#         density = np.sum(x) / total_area_hectares
#         return density - minimum_trees_per_hectare

#     # Initial guess
#     x0 = (df['Target_Percentage'] / 100 * desired_total_trees).to_numpy()

#     # Bounds based on ± tolerance
#     bounds = []
#     for i, pct in enumerate(df['Target_Percentage']):
#         min_pct = max(0, pct - target_percentage_tolerance)
#         max_pct = min(100, pct + target_percentage_tolerance)
#         min_trees = (min_pct / 100) * desired_total_trees
#         max_trees = (max_pct / 100) * desired_total_trees
#         bounds.append((min_trees, max_trees))

#     constraints = [
#         {'type': 'eq', 'fun': total_tree_constraint},
#         {'type': 'ineq', 'fun': minimum_density_constraint}
#     ]

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




# import streamlit as st
# import pandas as pd
# import numpy as np
# from scipy.optimize import minimize

# st.set_page_config(page_title="Tree Plantation Optimizer", layout="wide")

# st.title("🌳 Tree Plantation Optimizer")

# # ------------------- Inputs ------------------- #

# st.sidebar.header("🔧 Configuration")

# desired_total_trees = st.sidebar.number_input("🌲 Desired Total Trees", min_value=1000, value=22500, step=100)
# minimum_trees_per_hectare = st.sidebar.number_input("🌱 Minimum Density (trees/hectare)", min_value=100, value=878, step=10)

# spacing_adjustment_feet = st.sidebar.slider("📏 Spacing Adjustment (feet)", min_value=0.0, max_value=5.0, value=1.0, step=0.1)
# target_percentage_tolerance = st.sidebar.slider("📊 Target Percentage Tolerance (±%)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)

# additional_rows = st.sidebar.number_input("➕ Extra Blank Rows", min_value=0, max_value=20, value=0, step=1)

# st.sidebar.markdown("---")

# # ------------------- Default Tree Table ------------------- #
# st.subheader("🌿 Tree Species Configuration")

# default_data = {
#     'Tree': ['Mango', 'Jackfruit', 'Guava', 'Bael', 'Gooseberry', 'Mahogani', 'Teak', 'Rosewood'],
#     'Target_Percentage': [11, 10, 10, 7, 25, 12, 20, 5],
#     'Spacing': [18.0, 12.0, 9.0, 9.0, 12.0, 7.0, 7.0, 12.0]
# }

# df_input = pd.DataFrame(default_data)

# # Add blank rows
# if additional_rows > 0:
#     blank_rows = pd.DataFrame({
#         'Tree': [''] * additional_rows,
#         'Target_Percentage': [0.0] * additional_rows,
#         'Spacing': [1.0] * additional_rows
#     })
#     df_input = pd.concat([df_input, blank_rows], ignore_index=True)

# st.write("You can edit the Target % and Spacing below or add more trees:")
# edited_df = st.data_editor(df_input, num_rows="dynamic")

# run_opt = st.button("🚀 Run Optimization")

# if run_opt:
#     df = edited_df.copy()

#     # Drop incomplete or zero-percentage entries
#     df = df[(df['Tree'].astype(str).str.strip() != '') & (df['Target_Percentage'] > 0)]

#     # Apply spacing adjustment
#     df['Adjusted_Spacing'] = df['Spacing'] - spacing_adjustment_feet
#     df['Adjusted_Spacing'] = df['Adjusted_Spacing'].clip(lower=1.0)

#     areas_per_tree = df['Adjusted_Spacing'] ** 2  # in sqft

#     # ------------------- Optimization Setup ------------------- #

#     def objective(x):
#         return np.sum(x * areas_per_tree)

#     def total_tree_constraint(x):
#         return np.sum(x) - desired_total_trees

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

#     constraints.append({'type': 'eq', 'fun': total_tree_constraint})
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
    # 'Target_Percentage': [11, 10, 10, 7, 25, 12, 20, 5],
    # 'Spacing': [18.0, 12.0, 9.0, 9.0, 12.0, 7.0, 7.0, 12.0]
    'Target_Percentage': [13, 10, 10, 7, 25, 10, 20, 5],
    'Spacing': [15.0, 14.0, 12.0, 12.0, 12.0, 8.0, 8.0, 8.0]
}

df_input = pd.DataFrame(default_data)

st.write("You can edit the Target % and Spacing below or add more rows:")

edited_df = st.data_editor(df_input, num_rows="dynamic")

run_opt = st.button("🚀 Run Optimization")

if run_opt:
    df = edited_df.copy()

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



