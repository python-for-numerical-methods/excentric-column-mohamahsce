import numpy as np
from scipy.optimize import bisect

def find_critical_load(L, E, A, r, c, e, sigma_allow):
    """
    L: Column length [mm]
    E: Modulus of elasticity [MPa]
    A: Cross-sectional area [mm^2]
    r: Radius of gyration [mm]
    c: Distance to outer fiber [mm]
    e: Eccentricity [mm]
    sigma_allow: Allowable stress [MPa]
    
    Return: P critical load [N]
    """
    
    # Define the objective function f(P) = sigma_max - sigma_allow
    # We want to find P such that f(P) = 0
    def f(P):
        # Secant(x) is 1/cos(x)
        # Formula: sigma_max = (P/A) * [1 + (ec/r^2) * sec( (L/2r) * sqrt(P/EA) )]
        
        inner_term = (L / (2 * r)) * np.sqrt(P / (E * A))
        sec_term = 1 / np.cos(inner_term)
        
        sigma_max = (P / A) * (1 + (e * c / r**2) * sec_term)
        
        return sigma_max - sigma_allow

    # Define the search range for P
    # P_low is nearly 0
    # P_high: A safe upper bound is the Euler Critical Load (P_e = pi^2 * EI / L^2)
    # or simply a very large number based on material yield.
    p_low = 1e-3 
    p_high = sigma_allow * A  # The load cannot exceed yield stress * area
    
    # Use bisection to find the root
    try:
        p_critical = bisect(f, p_low, p_high, xtol=1e-6)
        return p_critical
    except ValueError:
        # If the range doesn't bracket the root, return the high bound as a fallback
        return p_high

# To run the tests mentioned in the image, use:
# pytest test_buckling.py
   **Units:** Ensure your inputs match the units in the docstring ($mm$, $MPa$, $N$). Since $1\text{ MPa} = 1\text{ N/mm}^2$, the units are consistent and don't require conversion factors inside the formula.
