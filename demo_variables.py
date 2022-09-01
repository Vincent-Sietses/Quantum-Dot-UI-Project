from input_variable import InputVariable


def generate_variables():
    """
    Function to define all variables
    """
    return [
        InputVariable(
                variable_name="Real part of first root", 
                unit="", 
                initial_value=1,
                initial_stepsize = None, # None defaults to 10*resolution
                variable_resolution  = 2e-4,
                stepsize_lower_bound = 1e-6,
                stepsize_upper_bound = 1,
                ),
        InputVariable(
                variable_name="Imaginary part of first root", 
                unit="", 
                initial_value=1,
                initial_stepsize = None,  
                variable_resolution  = 2e-4,
                stepsize_lower_bound = 1e-6,
                stepsize_upper_bound = 1,
                ),
        InputVariable(
                variable_name="Real part of second root", 
                unit="", 
                initial_value=-1,
                initial_stepsize = None,  
                variable_resolution  = 2e-4,
                stepsize_lower_bound = 1e-6,
                stepsize_upper_bound = 1,
                ),
        InputVariable(
                variable_name="Imaginary part of second root", 
                unit="", 
                initial_value=-1,
                initial_stepsize = None,  
                variable_resolution  = 2e-4,
                stepsize_lower_bound = 1e-6,
                stepsize_upper_bound = 1,
                ),
    ]