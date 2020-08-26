# import jwt
# from jwt.algorithms import get_default_algorithms
# import base64
# import json
# encoded = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256')
# print(encoded)
# #'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg'
# header, payload, signature = encoded.split(b'.')
# #payload = jwt.decode(encoded, 'secret', algorithms=['HS256'])
# # print(header)
# # print(payload)
# # print(signature)
#
# sign_input, _, _ = encoded.rpartition(b'.')
# # print(sign_input)
# alg = get_default_algorithms()['HS256']
# key = alg.prepare_key('secret')
# alg = alg.sign(sign_input, key)
# print(type(alg))
# print(signature)
# print(base64.urlsafe_b64encode(alg))
#
#
# # print(base64.urlsafe_b64decode(header))
# # print(base64.urlsafe_b64decode(payload))
# # print(base64.urlsafe_b64decode(signature))
# #print(base64.urlsafe_b64encode(simplejson.loads('{'some': 'payload'}')))
# a = {'some': 'payload'}
# b = json.dumps(a, separators=(',', ':'),cls=None)
# print(b)
# print(type(b))
# r= b.encode('utf-8')
# # r=bytes('{}'.format(a),'utf-8')
# print(type(base64.urlsafe_b64encode(r)))

import bcrypt
import datetime
# s1 = bcrypt.gensalt()
# print(s1)
password = b'123456'
print(bcrypt.hashpw(password, bcrypt.gensalt()))
print(bcrypt.hashpw(password, bcrypt.gensalt()))
x = bcrypt.checkpw(password, b'$2b$12$.OWGf8ggxzjeXMBuixEbT.cDGwpIJnUtMALiH3QZ/en58pV8IozyO')
print(x)
x = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
print(type(x))
print(x)