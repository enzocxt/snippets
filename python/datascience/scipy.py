import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(0, 1e6, 10)
plt.plot(x, 8.0 * (x**2) / 1e6, lw=5)
plt.xlabel('size n')
plt.ylabel('memory [MB]')

'''
seven sparse matrix types in scipy.sparse:
    1. csc_matrix: Compressed Sparse Column format
    2. csr_matrix: Compressed Sparse Row format
    3. bsr_matrix: Block Sparse Row format
    4. lil_matrix: List of Lists format
    5. dok_matrix: Dictionary of Keys format
    6. coo_matrix: COOrdinate format (aka IJV, triplet format)
    7. dia_matrix: DIAgonal format

WARNINGS for NumPy users:
    the multiplication with '*' is the matrix multiplication (dot product)
    not part of NumPy!
    passing a sparse matrix object to NumPy functions expecting ndarray/matrix
    does not work

all scipy.sparse classes are subclasses of spmatrix
    default implementation of arithmetic operations
        always converts to CSR
        subclasses override for efficiency
    shape, data type set/get
    nonzero indices
    format conversion, interaction with NumPy (toarray(), todense())
    …
attributes:
    mtx.A - same as mtx.toarray()
    mtx.T - transpose (same as mtx.transpose())
    mtx.H - Hermitian (conjugate) transpose
    mtx.real - real part of complex matrix
    mtx.imag - imaginary part of complex matrix
    mtx.size - the number of nonzeros (same as self.getnnz())
    mtx.shape - the number of rows and columns (tuple)
data usually stored in NumPy arrays

Summary of storage schemes:
http://www.scipy-lectures.org/advanced/scipy_sparse/storage_schemes.html
'''
