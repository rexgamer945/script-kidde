import random
import sys
import urllib.request, urllib.error, urllib.parse
import argparse

method = 'GET'
content_type = 'text/html'

def randomKey(charset, len):
    randKey = []
    for i in range(0, len):
        sampl = random.choice(charset)
        randKey.append(sampl)
    return ''.join(randKey)

def sendKey(url, key, suffix, verbose):
    
    if verbose:
        print(key)

    clen = 0
    data = ""
    
    if (method == "GET"):
        full_url = url + key + suffix
    else:
        data = key
        clen = len(data)

    if verbose:
        print("url : " + url)
    data = urllib.parse.urlencode(data).encode('utf-8')
    request = urllib.request.Request(full_url, data, {'Content-Type': content_type, 'Content-Length': clen})
    request.get_method = lambda: method
   
    try:    
        resp = urllib.request.urlopen(request)
        rcode = resp.getcode()
        if rcode == 200:
            print("GOT IT : " + full_url)
        resp.close()

    except urllib.error.HTTPError as e:
        if verbose:
            print(str(e) + " : " + full_url)
        rcode = e.getcode()

    return rcode

def main():
    parser = argparse.ArgumentParser(description="Payload scraper: a tiny scanner that search for the payloads hosted at the given URL, by generating and checking random names.")
    parser.add_argument('--url',dest="url",default=None,help="Base URL (a remote directory that we want to scan in search of payloads)", required=True)
    parser.add_argument('--len',dest="len",default=3, help="Length of the random name to be generated", required=False, type=int)
    parser.add_argument('--verbose',dest="verbose",default=False, help="Enable verbose mode", required=False, type=bool)
    parser.add_argument('--charset',dest="charset",default="abcdefghijklmnopqrstuwvxyz", help="The charset that will be used to generate the name")
    parser.add_argument('--ext',dest="ext",default=".exe", help="The extension of the searched payload")
    args = parser.parse_args()

    v_url = args.url
    len = args.len
    while (True):
        key = randomKey(args.charset, len)
        rcode = sendKey(v_url, key, args.ext, args.verbose)
    if args.verbose:
        print("DONE: " + str(rcode))
    return(0)

if __name__ == "__main__":
    sys.exit(main())