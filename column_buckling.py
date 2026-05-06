import numpy as np
from scipy.optimize import bisect

def find_critical_load(L, E, A, r, c, e, sigma_allow):
    """
    Finds the maximum allowable load P based on the Secant Formula.
    """
    
    def f(P):
        # Secant Formula: sigma_max = (P/A) * [1 + (ec/r^2) * sec( (L/2r) * sqrt(P/EA) )]
        # Using 1/cos(...) as per instructions
        
        # Calculate the argument for the secant/cosine term
        argument = (L / (2 * r)) * np.sqrt(P / (E * A))
        
        # Check if argument is too close to pi/2 (asymptote) to avoid division by zero
        if argument >= np.pi / 2:
            return float('inf')
            
        sec_term = 1 / np.cos(argument)
        sigma_max = (P / A) * (1 + (e * c / (r**2)) * sec_term)
        
        return sigma_max - sigma_allow

    # Define bounds: 
    # 1. P_low: Almost zero
    # 2. P_high: Must be less than the theoretical Euler load where cos goes to 0
    # P_euler = (pi^2 * E * I) / L^2, but based on the formula's argument:
    # (L/2r) * sqrt(P/EA) < pi/2  =>  P < (pi^2 * E * A * r^2) / L^2
    p_euler_limit = (np.pi**2 * E * A * r**2) / (L**2)
    
    # We also know P cannot exceed yield load: sigma_allow * A
    p_yield_limit = sigma_allow * A
    
    # The actual upper bound is the smaller of the two, with a tiny safety margin
    p_high = min(p_euler_limit, p_yield_limit) * 0.9999
    p_low = 1e-5

    try:
        #```

### Why this version should pass:
*   **Asymptote Protection**: The Secant formula has a vertical asymptote at the Euler buckling Bisection is recommended for stability in this task
        return bisect(f, p_low, p_high, xtol load ($P_e$). If your `p_high` was too large in the previous attempt, the solver likely failed because=1e-4)
    except ValueError:
        # If the root isn't bracketed, the allowable load is at the limit
         $\cos(arg)$ crossed zero.return p_high
