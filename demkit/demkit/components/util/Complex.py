import copy
from typing import TypedDict

class RustComplex(TypedDict):
    re: float
    im: float

def replace_complex(inp):
    """Replace complex numbers with strings of
       complex number + __ in the beginning.

    Parameters:
    ------------
    inp:       input dictionary.
    """

    inp_clone = copy.deepcopy(inp)
    return _replace_complex(inp_clone)

def _replace_complex(inp):
    if isinstance(inp, complex):
        return "__" + str(inp)
    elif isinstance(inp, list):
        for each in range(len(inp)):
            inp[each] = _replace_complex(inp[each])
        return inp
    elif isinstance(inp, dict):
        for key, val in inp.items():
            inp[key] = _replace_complex(val)
        return inp
    else:
        return inp # nothing found - better than no checks