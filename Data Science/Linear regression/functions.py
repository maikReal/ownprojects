from math import sqrt

def prod_non_zero_diag(x):
    """Compute product of nonzero elements from matrix diagonal.

    input:
    x -- 2-d numpy array
    output:
    product -- integer number


    Not vectorized implementation.
    """

    cols = len(x[0])
    rows = len(x)
    prod_val = 1
    cols_num = 0
    if cols == rows or cols > rows:
        for i in range(rows):
            if x[i][cols_num] == 0:
                cols_num += 1
                continue
            else:
                prod_val *= x[i][cols_num]
            cols_num += 1

    if rows > cols:
        for i in range(cols):
            if x[i][cols_num] == 0:
                cols_num += 1
                continue
            else:
                prod_val *= x[i][cols_num]
            cols_num += 1
            
    return prod_val


def are_multisets_equal(x, y):
    """Return True if both vectors create equal multisets.

    input:
    x, y -- 1-d numpy arrays
    output:
    True if multisets are equal, False otherwise -- boolean

    Not vectorized implementation.
    """

    return sorted(x) == sorted(y) 
            
    

import numpy as np

def max_after_zero(x):
    """Find max element after zero in array.

    input:
    x -- 1-d numpy array
    output:
    maximum element after zero -- integer number

    Not vectorized implementation.
    """

    if type(x) == np.ndarray:
        x = x.tolist()

    max_val = max(x)
    ind = x.index(max_val)
    if ind != 0 and x[ind-1] == 0:
        return max_val
    else:
        x.pop(ind)
        return max_after_zero(x)


def convert_image(img, coefs):
    """Sum up image channels with weights from coefs array

    input:
    img -- 3-d numpy array (H x W x 3)
    coefs -- 1-d numpy array (length 3)
    output:
    img -- 2-d numpy array

    Not vectorized implementation.
    """

    inner_len = len(img[0][0])
    len_coefs = len(coefs)
    if inner_len != len_coefs:
        dif = inner_len - len_coefs
        zeros = [0] * dif
        coefs = coefs + zeros
    
    for row_i, row_el in enumerate(img):
        for col_i, col_el in enumerate(row_el):
            val = 0
            for i in range(inner_len):
                val += col_el[i] * coefs[i]
            img[row_i][col_i] = val
    return img


def run_length_encoding(x):
    """Make run-length encoding.

    input:
    x -- 1-d numpy array
    output:
    elements, counters -- integer iterables

    Not vectorized implementation.
    """
    out = [[x[0]], []]
    cur = x[0]
    counter = 1
    
    for i in range(1, len(x)):
        if x[i] == cur:
            counter += 1
        else:
            out[1].append(counter)
            counter = 1
            cur = x[i]
            out[0].append(cur)
    out[1].append(counter)
    
    return out 


def pairwise_distance(x, y):
    """Return pairwise object distance.

    input:
    x, y -- 2d numpy arrays
    output:
    distance array -- 2d numpy array

    Not vectorized implementation.
    """

    dist_matrix = []
    for i in range(len(x)):
        
        summary = list(map(lambda z: list(map(lambda q, s: (q - s)**2, x[i], z)), y))
        dist = list(map(lambda x: sqrt(sum(x)), summary))
        dist_matrix.append(dist)    
    
    
    return dist_matrix
