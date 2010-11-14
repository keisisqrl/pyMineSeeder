import base64
import struct
import nbt
from itertools import izip,cycle
from math import floor




class Seed:


    def __init__(self):
	pass

    def _cipher(self, data_string):
	xor_key = [108,111,108,32,101,97,115,116,101,114,32,101,103,103]

	return ''.join(chr(ord(x) ^ y) for (x,y) in \
	    izip(data_string, cycle(xor_key)))
	
    def load_tag(self, nbt_file):
	self.root_tag = nbt.load(nbt_file)

	data_base = self.root_tag['Data']
	    
	self.random_seed = data_base['RandomSeed'].value
	self.time = data_base['Time'].value

	self.player_x = int(floor(data_base['Player']['Pos'][0].value))
	self.player_y = int(floor(data_base['Player']['Pos'][1].value))
	self.player_z = int(floor(data_base['Player']['Pos'][2].value))
	
	self.rotation_x = data_base['Player']['Rotation'][0].value
	self.rotation_y = data_base['Player']['Rotation'][1].value

    def load_string(self, instring):
	self.seed_string = instring

    def encode(self):
	data_pack = struct.pack('<qqiiiff',self.random_seed, self.time, 
	                        self.player_x, self.player_y, self.player_z,
				self.rotation_x,self.rotation_y)
	ciphertext = base64.b64encode(self._cipher(data_pack))
	self.seed_string = ''.join(('[',ciphertext,']'))

    def decode(self):
	data_pack = self._cipher(base64.b64decode( \
	    self.seed_string.strip('[]')))
	(self.random_seed, self.time, self.player_x, self.player_y,
	 self.player_z, self.rotation_x, self.rotation_y) = \
	    struct.unpack('<qqiiiff',data_pack)
