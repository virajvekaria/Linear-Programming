import streamlit as st
import pulp as lp

def linear_programming_demo():
    st.title("Linear Optimizer")

    # User input for the number of variables
    num_variables = st.number_input("Number of Variables", min_value=1, value=2, step=1)

    # Define the linear programming problem
    model = lp.LpProblem("Linear_Programming_Demo", lp.LpMaximize)

    # Define decision variables
    variables = [lp.LpVariable(f"x{i}", lowBound=0) for i in range(num_variables)]

    # User input for the objective function coefficients
    st.subheader("Objective Function Coefficients")
    objective_coeffs = {}
    for i, var in enumerate(variables):
        key = f"coeff_{i}"  # Generate a unique key for each coefficient input
        coeff = st.number_input(f"Coefficient for {var.name}", key=key, value=1.0, step=0.1)
        objective_coeffs[var] = coeff

    # Define the objective function to maximize
    objective = lp.lpSum(objective_coeffs[var] * var for var in variables)
    model += objective

    # User input for constraints
    st.subheader("Constraints")
    num_constraints = st.number_input("Number of Constraints", min_value=0, value=1, step=1)

    for i in range(num_constraints):
        st.write(f"Constraint {i + 1}:")
        constraint_coeffs = {}
        for j, var in enumerate(variables):
            key = f"const_{i}_coeff_{j}"  # Generate a unique key for each coefficient input
            coeff = st.number_input(f"Coefficient for {var.name}", key=key, value=1.0, step=0.1)
            constraint_coeffs[var] = coeff

        key = f"const_{i}_rhs"  # Generate a unique key for the RHS input
        constraint_rhs = st.number_input("Right-Hand Side (RHS)", key=key, value=1.0, step=0.1)

        constraint = lp.lpSum(constraint_coeffs[var] * var for var in variables) <= constraint_rhs
        model += constraint

    # Solve the linear programming problem
    model.solve()

    # Display the results
    st.subheader("Results:")
    st.write(f"Status: {lp.LpStatus[model.status]}")

    if lp.LpStatus[model.status] == 'Optimal':
        for var in variables:
            st.write(f"{var.name} = {var.varValue}")
        st.write(f"Optimal value of the objective function: {lp.value(objective)}")

if __name__ == '__main__':
    linear_programming_demo()
