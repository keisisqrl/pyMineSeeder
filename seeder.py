#!/usr/bin/env python
import codec
import sys

def load(nbt_path):
    # Load a level file, parse, and print the mineseed
    model = codec.Seed()
    model.load_tag(nbt_path)
    model.parse_nbt()
    model.encode()
    print model.get_seed()

def write(nbt_path):
    model = codec.Seed()
    model.load_string(raw_input('Please enter the mineseed: '))
    model.decode()
    model.make_nbt()
    model.write_nbt(nbt_path)

def usage():
    print '''Usage:
    seeder.py [-l|-w] level.dat

    -l - load level.dat, produce mineseed
    -w - prompt for mineseed, write level.dat

    level.dat should be the full path to the level.dat file you wish to use'''
    sys.exit(2)

def main():
    if len(sys.argv) != 3:
	usage()
    if sys.argv[1] == '-l':
	load(sys.argv[2])
    elif sys.argv[1] == '-w':
	write(sys.argv[2])
    else:
	usage()

if __name__ == "__main__":
    main()
