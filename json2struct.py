import json


def getType(val):
	return type(val).__name__ 


def OutPutFile(filepath, struct_list, name):
	f = open(filepath, mode='w', encoding='utf8')
	txt = ''
	for i in struct_list[-1::-1]:
		print(i)
		txt += 'struct ' + i[0] + '\n'
		txt += '{\n'
		for k in i[1:]:
			print(k)
			txt += '    ' + k[0] + ' ' + k[1] + ';\n'
		txt += '};\n\n'

	f.write(txt)
	f.close()
	print(txt)


def dict2struct(obj, root_name, filepath):
	struct_list = []
	dst = [[root_name, obj]]
	while len(dst) > 0:
		cur = dst[0]
		if len(dst) > 1:
			dst = dst[1:]
		else:
			dst = []

		one_struct = [cur[0]]
		for x in cur[1].items():
			str_type = getType(x[1])
			if str_type == 'int':
				one_struct += [['int', x[0]]]
			elif str_type == 'bool':
				one_struct += [['bool', x[0]]]
			elif str_type == 'str':
				one_struct += [['std::string', x[0]]]
			elif str_type == 'float':
				one_struct += [['double', x[0]]]
			elif str_type == 'dict':
				one_struct += [['st_' + x[0],x[0]]]
				dst += [['st_' + x[0],x[1]]]
			elif str_type == 'list':
				if len(x[1]) > 0:
					str_arr_type = getType(x[1][0])
					if str_arr_type == 'dict':
						one_struct += [['std::vector<st_' + x[0] + '>', 'vec'+x[0]]]
						dst += [['st_' + x[0],x[1][0]]]
					elif str_arr_type == 'str':
						one_struct += [['std::vector<std::string>', 'vec'+x[0]]]
					else:
						one_struct += [['std::vector<' + str_arr_type + '>', 'vec'+x[0]]]
				else:
					str_arr_type = 'unknown'
					one_struct += [['std::vector<' + str_arr_type + '>', x[0]]]

		struct_list += [one_struct]
	print(struct_list)
	OutPutFile(filepath, struct_list, root_name)
	
if __name__ == '__main__':
	obj = {'aaa':1, 'bbb':True, 'cccc':{'a':1, 'c': 2, 'd':{'t':'1'}, 'y':[1,2,3], 'z':['a'], 'x':[{}] }}
	dict2struct(obj, "yyyyy", 'demo.h')



