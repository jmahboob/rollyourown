"""
The following code is based off of RFC1321 (https://www.ietf.org/rfc/rfc1321.txt)

"""

import logging
import bitstring
import math

log = logging.getLogger(__name__)

# This value is a precomputed table
rotate_amounts = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                  5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
                  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

constants = [int(abs(math.sin(i+1)) * 2**32) & 0xFFFFFFFF for i in range(64)]

init_variables = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

def pad(plaintext):
    log.debug("\tEntering md5.py_pad")
    bs_plaintext = bitstring.BitArray(plaintext)
    orig_len = len(bs_plaintext.bin)
    log.debug("\t %s", bs_plaintext.bin)
    if (len(bs_plaintext.bin) % 512) != 0:
        log.info("\tMessage of len(%d) requires padding (not on 512-bit) boundary", len(bs_plaintext.bin))
        bs_plaintext.append('0b1')
        # I hate this sentence and I hope whoever wrote it suffers minor injury
        # "This is follow by as many zeros as are required to bring the length of the message up to 64 bits fewer than a multiple of 512"
        for i in range (0, (512 - (len(bs_plaintext.bin)) % 512 - 64)):
            bs_plaintext.append('0b0')
        last64 = bitstring.BitArray(uint = orig_len % pow(2,64), length=64)
        bs_plaintext.append(last64)
        log.info("\t%s len: %d" %  (bs_plaintext.bin, len(bs_plaintext.bin)))
    else:
        log.info("We're totally going to do some crypto now")
