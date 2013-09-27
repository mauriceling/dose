'''
Hash Generators
Date created: 16th April 2013
Licence: Python Software Foundation License version 2
'''

import hashlib as h

def forward_file_hash(f, fsize, start, blocksize, algorithm):
    '''
    Forward file hashing. It takes file and generate repeated 
    hashes to the end of the file in blocks.
    
    Algorithm:
        1. block <- file from position N to N + blocksize
        2. hash <- generate hash from block
        3. N = N + blocksize
        4. block <- file from position N to N + blocksize
        5. block = block + hash
        6. hash <- generate hash from block
        7. Repeat steps 3 to 6 until end of file
        8. Return hash
        
    @param f: file handle of file to hash
    @param fsize: file size of f
    @type fsize: integer
    @param start: file location to start hashing
    @type start: integer
    @param blocksize: block size for hash generation
    @type blocksize: integer
    @param algorithm: algorithm to generate hash. Allowable
    options are {md5|sha1|sha244|sha256|sha384|sha512}
    @type algorithm: strong
    @return: generated hash in string
    '''
    hash_result = ''
    count = 0
    while start < fsize:
        f.seek(start)
        data = str(f.read(blocksize))
        if algorithm == 'md5':
            hash_result = h.md5(data + str(hash_result)).hexdigest()
        if algorithm == 'sha1':
            hash_result = h.sha1(data + str(hash_result)).hexdigest()
        if algorithm == 'sha244':
            hash_result = h.sha244(data + str(hash_result)).hexdigest()
        if algorithm == 'sha256':
            hash_result = h.sha256(data + str(hash_result)).hexdigest()
        if algorithm == 'sha384':
            hash_result = h.sha384(data + str(hash_result)).hexdigest()
        if algorithm == 'sha512':
            hash_result = h.sha244(data + str(hash_result)).hexdigest()
        start = start + blocksize
        count = count + 1
##        print start, hash_result
    print 'forward hash:', start, count
    return hash_result
    
def backward_file_hash(f, end, blocksize, algorithm):
    '''
    Forward file hashing. It takes file and generate repeated 
    hashes to the end of the file in blocks.
    
    Algorithm:
        1. block <- file from position N - blocksize to N
        2. hash <- generate hash from block
        3. N = N - blocksize
        4. block <- file from position N - blocksize to N
        5. block = block + hash
        6. hash <- generate hash from block
        7. Repeat steps 3 to 6 until start of file
        8. Return hash
        
    @param f: file handle of file to hash
    @param end: file location to start hashing
    @type end: integer
    @param blocksize: block size for hash generation
    @type blocksize: integer
    @param algorithm: algorithm to generate hash. Allowable
    options are {md5|sha1|sha244|sha256|sha384|sha512}
    @type algorithm: strong
    @return: generated hash in string
    '''
    hash_result = ''
    current = 0
    count = 0
    while current < end:
        f.seek(current)
        data = str(f.read(blocksize))
        if algorithm == 'md5':
            hash_result = h.md5(data + str(hash_result)).hexdigest()
        if algorithm == 'sha1':
            hash_result = h.sha1(data + str(hash_result)).hexdigest()
        if algorithm == 'sha244':
            hash_result = h.sha244(data + str(hash_result)).hexdigest()
        if algorithm == 'sha256':
            hash_result = h.sha256(data + str(hash_result)).hexdigest()
        if algorithm == 'sha384':
            hash_result = h.sha384(data + str(hash_result)).hexdigest()
        if algorithm == 'sha512':
            hash_result = h.sha244(data + str(hash_result)).hexdigest()
        current = current + blocksize
        count = count + 1
##        print end, hash_result
    print 'backward hash:', end, count
    return hash_result
    
def cfh(filename,
        blocksize=1024,
        startpoints=10,
        algorithm='md5'):
    '''
    Circular file hasher. This function uses repeated forward
    and backward hash functions to generate hash for the 
    entire file. Hence, a byte in the file will be hashed 
    multiple times. The length of hash generated will be 
    dependent on the block size and number of start points.
    
    Algorithm:
        1. forward hash <- hash(start) + [hash(start + 1) 
        for start = 0 to startpoints]
        2. backward hash <- hash(start) + [hash(start - 1) 
        for start = startpoints to 0]
        3. Return forward hash + backward hash
    
    @param filename: name of file to hash
    @type filename: string
    @param blocksize: block size for hash generation. 
    Default = 1024
    @type blocksize: integer
    @param startpoints: defines the number of start point on
    the file for hash generation. Default = 10.
    @type startpoints: integer
    @param algorithm: algorithm to generate hash. Allowable
    options are {md5|sha1|sha244|sha256|sha384|sha512}
    @type algorithm: strong
    @return: generated hash in string
    '''
    f = open(filename, 'rb')
    f.seek(-1, 2)
    fsize = f.tell()
    file_block_size = int(fsize/int(startpoints))
    startpoints = [x*file_block_size
                   for x in range(int(startpoints))]
    fhash = [forward_file_hash(f, fsize, start, blocksize, algorithm)
             for start in startpoints]
    bhash = [backward_file_hash(f, startpoints[-1], blocksize, algorithm)]
    bhash = bhash + [backward_file_hash(f, start, blocksize, algorithm)
                     for start in startpoints[1:]]
    return ''.join(fhash + bhash)
