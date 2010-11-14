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
	if ( not instring.startswith('[') or not instring.endswith(']')):
	    raise Exception("Invalid MineSeed")

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

    def make_nbt(self, **kwargs):
	self.root_tag = nbt.TAG_Compound()
	data_base = nbt.TAG_Compound("Data")
	self.root_tag.add(data_base)

	data_base['RandomSeed'] = nbt.TAG_Long(self.random_seed)
	data_base['Time'] = nbt.TAG_Long(kwargs.get('time',self.time))
	data_base['SpawnX'] = nbt.TAG_Int(self.player_x)
	data_base['SpawnY'] = nbt.TAG_Int(self.player_y)
	data_base['SpawnZ'] = nbt.TAG_Int(self.player_z)
	data_base['LastPlayed'] = nbt.TAG_Long(1289561130810)
	data_base['SizeOnDisk'] = nbt.TAG_Long(1000)

	player_base = nbt.TAG_Compound("Player")
	data_base.add(player_base)

	player_base['OnGround'] = nbt.TAG_Byte(1)
	player_base['Air'] = nbt.TAG_Short(300)
	player_base['AttackTime'] = nbt.TAG_Short(0)
	player_base['DeathTime'] = nbt.TAG_Short(0)
	player_base['Fire'] = nbt.TAG_Short(-20)
	player_base['Health'] = nbt.TAG_Short(20)
	player_base['HurtTime'] = nbt.TAG_Short(0)
	player_base['Dimension'] = nbt.TAG_Int(0)
	player_base['Score'] = nbt.TAG_Int(0)
	player_base['FallDistance'] = nbt.TAG_Float(0)

	player_pos = nbt.TAG_List(name='Pos',list_type=nbt.TAG_Double)
	player_base.add(player_pos)
	
	player_pos.append(nbt.TAG_Double(float(self.player_x)))
	player_pos.append(nbt.TAG_Double(float(self.player_y)))
	player_pos.append(nbt.TAG_Double(float(self.player_z)))
	
	player_rot = nbt.TAG_List(name='Rotation',list_type=nbt.TAG_Float)
	player_base.add(player_rot)
	
	player_rot.append(nbt.TAG_Float(self.rotation_x))
	player_rot.append(nbt.TAG_Float(self.rotation_y))

	inventory = nbt.TAG_Compound('Inventory')
	player_base.add(inventory)

	player_mot = nbt.TAG_List(name='Motion',list_type=nbt.TAG_Double)
	player_base.add(player_mot)

	player_mot.append(nbt.TAG_Double(0.0))
	player_mot.append(nbt.TAG_Double(0.0))
	player_mot.append(nbt.TAG_Double(0.0))
	
    def write_nbt(self, outfile):
	self.root_tag.save(outfile)
