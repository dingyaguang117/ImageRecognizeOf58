#coding=utf-8
import json
from checkCharData import show
import pickle

'''
小写字母
'''
a = {}
for i in xrange(26):
    try:
        c = chr(ord('a') + i)
        f = open('json/_%s.json'%c)
        d = json.loads(f.read())
        a[c] = d
        f.close()
    except:
        pass
    
for char in a:
    print '====== %s ======'%char
    show('_'+char)
    
    
    
'''
大写字母
'''
A = {}
for i in xrange(26):
    try:
        c = chr(ord('A') + i)
        f = open('json/%s.json'%c)
        d = json.loads(f.read())
        A[c] = d
        f.close()
    except:
        pass
    
for char in A:
    print '====== %s ======'%char
    #show(char)
    
    
    
'''
数字
'''
N = {}
for i in xrange(1,10):
    try:
        c = i
        f = open('json/%s.json'%c)
        d = json.loads(f.read())
        N[c] = d
        f.close()
    except:
        pass
    
for char in N:
    print '====== %s ======'%char
    show(char)

result = {}
result.update(a)
result.update(A)
result.update(N)
for key in  result:
    result[key].pop('x_min')
    result[key].pop('y_min')
    result[key].pop('x_max')
    result[key].pop('y_max')
print result
with open('data.json','wb') as f:
    f.write(json.dumps(result))