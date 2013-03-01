import json

def show(char):
    with open('json/%s.json'%char) as f:
        dic = json.loads(f.read())
        print dic
        for i in xrange(dic['height']):
            for j in xrange(dic['width']):
                if [j,i] in dic['points']:
                    print 'O',
                else:
                    print ' ',
            print '\n'
                    

def main():
    pass
    show('_k')

    
if __name__ == '__main__':  
    main()