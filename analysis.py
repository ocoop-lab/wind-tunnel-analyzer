"""
analysis.py

Aerodynamic analysis utilities for the Wind Tunnel Analyzer project.

This module currently supports simple calculations based on a linear
lift-curve model. Numerical solver support for finding angle of attack
from a target lift coefficient is planned but not yet implemented.
"""

from scipy.optimize import fsolve


def compute_cl(alpha, cl0=0.10, lift_slope=0.11):
    """
    Compute lift coefficient using a linear lift model.

    Parameters
    ----------
    alpha : float
        Angle of attack in degrees.
    cl0 : float, optional
        Lift coefficient at zero angle of attack.
    lift_slope : float, optional
        Lift curve slope in units of 1/degree.

    Returns
    -------
    float
        Lift coefficient.
    """
    return cl0 + lift_slope * alpha


def print_lift_summary(alpha, cl0=0.10, lift_slope=0.11):
    """
    Print a simple summary of the lift coefficient for a given angle of attack.

    Parameters
    ----------
    alpha : float
        Angle of attack in degrees.
    cl0 : float, optional
        Lift coefficient at zero angle of attack.
    lift_slope : float, optional
        Lift curve slope in units of 1/degree.
    """
    cl = compute_cl(alpha, cl0=cl0, lift_slope=lift_slope)

    print("Wind Tunnel Analyzer")
    print("--------------------")
    print(f"Angle of attack : {alpha:.2f} deg")
    print(f"Lift coefficient: {cl:.3f}")


# TODO:
def alpha_residual(alpha, target_cl, cl0=0.10, lift_slope=0.11):
    """
    Calculate the difference between the computed and target lift coefficient.
    """
    return cl0 + lift_slope * alpha - target_cl


def solve_alpha(target_cl, cl0=0.10, lift_slope=0.11, initial_guess=5.0):
    """
    Solve for the angle of attack that produces a target lift coefficient.

    Parameters
    ----------
    target_cl : float
        Desired lift coefficient.
    cl0 : float, optional
        Lift coefficient at zero angle of attack.
    lift_slope : float, optional
        Lift curve slope in units of 1/degree.
    initial_guess : float, optional
        Initial guess for the angle of attack in degrees.

    Returns
    -------
    float
        Calculated angle of attack in degrees.
    """
    if lift_slope == 0:
        raise ValueError("lift_slope must not be zero.")

    alpha_solution = fsolve(
        alpha_residual,
        initial_guess,
        args=(target_cl, cl0, lift_slope),
    )

    alpha = float(alpha_solution[0])

    # Confirm that the solver actually found a solution.
    residual = alpha_residual(alpha, target_cl, cl0, lift_slope)
    if abs(residual) > 1e-6:
        raise ValueError("Could not find a valid angle of attack.")

    return alpha
# Add a numerical solver that computes angle of attack from a target
# lift coefficient using scipy.optimize.fsolve.
#
# Planned residual form:
#     f(alpha) = cl0 + lift_slope * alpha - target_cl
#
# Possible function names:
#     alpha_residual(...)
#     solve_alpha(...)
#
# This feature has not been implemented yet.
