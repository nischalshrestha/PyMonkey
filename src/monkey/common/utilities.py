"""
Convenience functions
"""

def make_list(length):
    """
    Creates and initializes a list in a safe manner (avoiding reference issues)
    """
    return [None for x in range(length)]