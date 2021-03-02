import argparse

def decode1(data, key, max_key=0):
    if max_key == 0 or max_key > len(key):
        max_key = len(key)
    l = len(key)
    j = 0 #key index
    decoded = bytearray()
    for i in range(0, len(data)):
        decoded.append(data[i] ^ key[j % l])
        if (i > 0):
            j += 1
        if (j == max_key):
            j = 0
    return decoded

def decode2(data, key, max_key=0):
    if max_key == 0 or max_key > len(key):
        max_key = len(key)
    j = 0 #key index
    prev_j = 0
    decoded = bytearray()
    for i in range(0, len(data)):
        val = data[i] + prev_j
        val = ((val ^ key[j]) ^ key[prev_j]) % 256
        decoded.append(val)
        prev_j = j
        j = j + 1
        if (j == max_key):
            j = 0
    return decoded

def decode(data, key, offset=0):
    maxlen = len(data)
    keylen = len(key)
    j = 0 #key index
    decoded = bytearray()
    for i in range(offset, maxlen):
        dec = key[j % keylen] ^ data[i]
        j += 1
        decoded.append(dec) 
    return decoded

def main():
    parser = argparse.ArgumentParser(description="Data XOR")
    parser.add_argument('--file', dest="file", default=None, help="Input file", required=True)
    parser.add_argument('--key', dest="key", default=None, help="Value with which to XOR")
    parser.add_argument('--keyfile', dest="keyfile", default=None, help="File with which to XOR")
    parser.add_argument('--offset',dest="offset", default=0,type=int, help="Offset in file from which XOR should start")
    parser.add_argument('--maxkey',dest="maxkey", default=0, type=int, help="Maximal length of the key")
    parser.add_argument('--mode',dest="mode", default=0, type=int, help="Choose algorithm [0,1,2] 0 for simple xor")
    args = parser.parse_args()


    data = bytearray(open(args.file, 'rb').read())
    if (args.key == None and args.keyfile == None):
        print "Supply key or keyfile"
        exit (-1)
    if args.keyfile:
        key = bytearray(open(args.keyfile, 'rb').read())
    else:
        key = bytearray(args.key)

    if args.mode == 1:
        print decode1(data, key, args.maxkey)
    elif args.mode == 2:
        print decode2(data, key, args.maxkey)
    else:
        print decode(data, key, args.offset)


if __name__ == "__main__":
    main()