"""
Utility functions for the Botwell test framework.
"""

from botwell.utils.model_standardization import standardize_model_name, standardize_model_names_in_dict, standardize_model_names_in_list
from botwell.utils.tokenization import *
from botwell.utils.caching import *
from botwell.utils.standardize_model_names import *
from botwell.utils.create_cross_grading_table import *

def median_of_list(lst):
    """Returns the middle sorted values for both even and odd n;
    for odd n, just take the middle sorted value; for even n,
    take the average of the two middle sorted values.
    
    Args:
        lst: A list of numeric values
        
    Returns:
        The median value as a float, or 0.0 if the list is empty
    """
    if not lst:
        return 0.0  # Handle empty list case
    n, srtlst = len(lst), sorted(lst)
    return (srtlst[n//2] + srtlst[(n-1)//2])/2