def capitalize(s):
    return s[0].upper() + s[1:]

def sqlalchemy_column_types(field_type):
	if field_type == 'int':
		return('Integer')
	else:
		return('String')