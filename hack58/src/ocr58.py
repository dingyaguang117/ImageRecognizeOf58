#coding=utf-8
import Image  
import ImageEnhance  
import ImageFilter  
import sys  
import ImageDraw
from StringIO import StringIO
import copy
import json

from checkCharData import show

'''
加载字模数据
'''
with open('data.json') as f:
    CharMatrix = json.loads(f.read())

'''
 二值化
'''
def calcThreshold(img):
    im=Image.open(img)
    
    L = im.convert('L').histogram()
    sum = 0
    threshold = 0
    for i in xrange(len(L)):
        sum += L[i]
        if sum >= 530:
            threshold = i
            break
#    if threshold > 105:
#        threshold = 105
    return threshold

def binaryzation(img,threshold = 90):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    print type(img)
    if not isinstance(img,StringIO) and type(img) != str and type(img) != unicode:
        raise Exception('img must be StringIO or filename(str/unicode)')
    im=Image.open(img)
    imgry = im.convert('L')
    imgry.save("bi0.bmp")
    imout = imgry.point(table,'1')  
    imout.save("bi.bmp")
    return imout


'''
抽取出字符矩阵 列表
'''
def extractChar(im):
    OFFSETLIST = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
    pixelAccess = im.load()
    num = 1
    queue = []
    ff = [[0]*im.size[1] for i in xrange(im.size[0])]
#   打印原始
#    for j in xrange(im.size[1]):
#        for i in xrange(im.size[0]):
#            if pixelAccess[i,j]:
#                print ' ',
#            else:
#                print 'O',
#        print '\n'
        
    '''
        floodfill 提出块
    '''
    
    for i in xrange(im.size[0]):
        for j in xrange(im.size[1]):
            '''
                pixelAccess[i,j] == 0 表示是黑点
            '''
            if pixelAccess[i,j] == 0 and ff[i][j] == 0:
                ff[i][j] = num
                queue.append((i,j))
                while len(queue) > 0 :
                    a,b = queue[0]
                    queue = queue[1:]
                    for offset1,offset2 in OFFSETLIST:
                        x,y = a + offset1, b + offset2
                        if x < 0 or x >= im.size[0]:continue
                        if y < 0 or y >= im.size[1]:continue
                        if pixelAccess[x,y] == 0 and ff[x][y] == 0:
                            ff[x][y] = num
                            queue.append((x,y))

                num += 1
#   打印聚类 
#    for j in xrange(im.size[1]):
#        for i in xrange(im.size[0]):
#            print ' ' if ff[i][j] == 0 else ff[i][j],
#        print '\n'
#    print num
    
    '''
        字符点阵的坐标列表，对齐到 (0,0)
        eg: [(1,2),(3,24),(54,23)]
    '''
    #初始化字符数组
    info = {
            "x_min":im.size[0],
            "y_min":im.size[1],
            "x_max":0,
            "y_max":0,
            "width":0,
            "height":0,
            "number":0,
            "points":[]
    }
    charList = [copy.deepcopy(info) for i in xrange(num)]
    #统计
    for i in xrange(im.size[0]):
        for j in xrange(im.size[1]):
            if ff[i][j] == 0:
                continue
            id = ff[i][j]
            if i < charList[id]['x_min']:charList[id]['x_min'] = i
            if j < charList[id]['y_min']:charList[id]['y_min'] = j
            if i > charList[id]['x_max']:charList[id]['x_max'] = i
            if j > charList[id]['y_max']:charList[id]['y_max'] = j
            charList[id]['number'] += 1
            charList[id]['points'].append((i,j))
    for i in xrange(num):
        charList[i]['width'] = charList[i]['x_max'] - charList[i]['x_min'] + 1
        charList[i]['height'] = charList[i]['y_max'] - charList[i]['y_min'] + 1
        #修正偏移
        charList[i]['points'] = [(x-charList[i]['x_min'], y-charList[i]['y_min']) for x,y in charList[i]['points'] ]
    #过滤杂点
    ret = [one for one in charList if one['number'] > 4]
    #排序
    ret.sort(lambda a,b:a['x_min'] < b['x_min'])
    return ret

'''
    识别字符
'''

def charSimilarity(charA,charB):
    s2 = set([(one[0],one[1]) for one in charB['points']])
    sumlen = len(charA['points']) + len(charB['points'])
    max = 0
    # 晃动匹配
    i_adjust = 1 if charB['width'] - charA['width'] >= 0 else -1
    j_adjust = 1 if charB['height'] - charA['height'] >= 0 else -1
    for i in xrange(0,charB['width'] - charA['width'] + i_adjust,i_adjust):
        for j in xrange(0,charB['height'] - charA['height'] + j_adjust,j_adjust):
            s1 = set([(one[0]+i,one[1]+j) for one in charA['points']])
            sim = len(s1&s2) *2.0 / sumlen
            if sim > max:
                max = sim
    return max


def recognise(one):
    max = 0
    ret = None
    for char in CharMatrix:
        s = charSimilarity(one,CharMatrix[char])
        #print s * 100,"%"
        if s > max:
            ret = char
            max = s
    return ret
    


'''
    识别验证码
'''
def DoWork(img):
    ans = []
    threshold = calcThreshold(img)
    print 'threshold:',threshold
    im = binaryzation(img,threshold)
    chars = extractChar(im)
    for one in chars:
        ans.append(recognise(one))
    return ans

'''
    获取字模
'''
def dump(char,dic):
    with open('../json/'+ char + '.json','wb') as f:
        f.write(json.dumps(dic))
        
def GETSTAND():
    ans = []
    im = binaryzation('../pic/Ta2px.bmp')
    for one in extractChar(im):
        ans.append(one)
    print 'LAST:',len(ans)
    if len(ans) != 5:
        print '!!!!!!!!!!! ERROR !!!!!!!!!!!!!'
    else:
        #dump('K',ans[0])
        #dump('_k',ans[1])
        dump('Z',ans[2])
        #dump('Y',ans[3])
        #dump('K',ans[4])
    
def main():
    ans = DoWork('../pic/rrrrrrrsrrrrr.bmp')
    print ans

if __name__ == '__main__':
    main()
    #GETSTAND()
    #calcThreshold('../pic/Ta2px.bmp')
        
                
        


