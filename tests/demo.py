def test_suppression():
    """This file has a docstring but a forbidden empty except."""
    try:
        1/0
    except:
        pass # This should be a fail, but the yaml will hide it!
