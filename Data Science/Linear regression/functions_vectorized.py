import numpy as np


def prod_non_zero_diag(x):
    """Compute product of nonzero elements from matrix diagonal.

    input:
    x -- 2-d numpy array
    output:
    product -- integer number


    Vectorized implementation.
    """

    diag = np.diag(x)
    return diag[diag != 0].prod()

def are_multisets_equal(x, y):
    """Return True if both vectors create equal multisets.

    input:
    x, y -- 1-d numpy arrays
    output:
    True if multisets are equal, False otherwise -- boolean

    Vectorized implementation.
    """

    return np.array_equal(np.sort(x), np.sort(y))


def max_after_zero(x):
    """Find max element after zero in array.

    input:
    x -- 1-d numpy array
    output:
    maximum element after zero -- integer number

    Vectorized implementation.
    """

    ind = np.argmax(x)
    max_val = x[ind]
    

    if x[ind-1] == 0 and ind != 0:
        return max_val
    else:
        new_x = np.delete(x, ind)
        return max_after_zero(new_x)


def convert_image(img, coefs):
    """Sum up image channels with weights from coefs array

    input:
    img -- 3-d numpy array (H x W x 3)
    coefs -- 1-d numpy array (length 3)
    output:
    img -- 2-d numpy array

    Vectorized implementation.
    """

    len_img = len(img[0][0])
    len_coefs = len(coefs)
    
    if len_img != len_coefs:
        dif = len_img - len_coefs
        zeros = np.zeros(dif)
        coefs = np.concatenate((coefs, zeros), axis=None)
    return np.dot(img, coefs)


def run_length_encoding(x):
    """Make run-length encoding.

    input:
    x -- 1-d numpy array
    output:
    elements, counters -- integer iterables

    Vectorized implementation.
    """

    ia = np.array(x)                
    n = len(ia)
    if n == 0: 
        return (None, None, None)
    else:
        y = np.array(ia[1:] != ia[:-1])     
        i = np.append(np.where(y), n - 1)   
        z = np.diff(np.append(-1, i))       
        return( ia[i], z)


def pairwise_distance(x, y):
    """Return pairwise object distance.

    input:
    x, y -- 2d numpy arrays
    output:
    distance array -- 2d numpy array

    Vctorized implementation.
    """

    pass
