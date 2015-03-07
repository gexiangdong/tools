# coding=utf-8
#
# 生成加减乘除四则混合运算题，小学二年级用
# 使用方法  
#   #python3 suanshuti.py
#           然受查找当前目录下的sxt.html，用浏览器打开后直接打印；或查找sxt.csv，用excel或其他工具打开打印
#   #python3 suanshuti.py test 
#           用于测试，每种类型测试5000道题，看是否会出现小数、负数等，出现会有错误提示
#   #python3 suanshuti.py sample 
#           每种类型打印一个样题
#
import random
import sys


def generateQuestion(t):
    HARD = 3  #尝试使用退位减法、进位加法的次数；越大越难
    q = ""
    x = 0
    y = 0
    z = 0
    
    if(t == 1 or t == 2):
        #(x+y)*z  or z*(x+y)
        x = random.randint(1,15)
        for k in range(HARD):
            y = random.randint(1,10)
            if(x % 10 + y % 10 > 10):
                break
                
        z = random.randint(1,10)
        
        if(t == 1):
            q = '({0} + {1}) * {2}'
        else:
            q = '{2} * ({0} + {1})'
    elif(t == 3 or t == 4):
        #(x-y)*z
        y = random.randint(15,100)
        for k in range(HARD):
            x = y +random.randint(1,15)
            if(x % 10 < y % 10):
                break;
        z = random.randint(1,10)
        if(t == 3):
            q = '({0} - {1}) * {2}'
        else:
            q = '{2} * ({0} - {1})'
    elif(t == 5):
        #(x+y)/z
        r = random.randint(1,10)
        z = random.randint(1,10)
        s = r * z
        for k in range(HARD):
            x = random.randint(1, s)
            if(x % 10 > s % 10):
                break;
        y = s - x
        q = '({0} + {1}) / {2}'
    elif(t == 6):
        r = random.randint(1,10)
        s = random.randint(3,10)
        z = r * s
        x = random.randint(0, s)
        y = s - x;
        q = '{2} / ({0} + {1})'
    elif(t == 7):
        #(x-y)/z
        r = random.randint(1,10)
        z = random.randint(2,10)
        for k in range(HARD):
            x = random.randint(1, r*z)
            if(x % 10 > r * z % 10):
                break
        y = r*z - x
        q = '({0} + {1}) / {2}'
    elif(t == 8):
        #z/(x-y)
        r = random.randint(1,10)
        s = random.randint(1,10)
        z = r * s
        x = random.randint(1, s)
        y = s - x
        q = '{2} / ({0} + {1})'        
    elif(t == 9 or t == 10):
        #x*y+z or z+x*y
        x = random.randint(1,10)
        y = random.randint(1,10)
        for k in range(HARD):
            z = random.randint(10, 100)
            if((z % 10 + x*y % 10) > 10):
                break;
        if(t == 9):
            q = '{0} * {1} + {2}'
        else:
            q = '{2} + {0} * {1}'
    elif(t == 11 or t == 12):
        #x*y-z or z-x*y
        x = random.randint(1,10)
        y = random.randint(1,10)
        if(t == 11):
            for k in range(HARD):
                z = random.randint(0, x * y)
                if(z % 10 > x*y % 10):
                    break;
            q = '{0} * {1} - {2}'
        else:
            for k in range(HARD):
                z = random.randint(x * y, 200)
                if(z % 10 < x*y % 10):
                    break;
            q = '{2} - {0} * {1}'
    elif(t == 13 or t == 14):
            #x/y+z  or z+x/y
        r = random.randint(1,10)
        y = random.randint(1,10)
        x = r * y
        for k in range(HARD):
            z = random.randint(10, 100)
            if((z % 10 + r) > 10):
                break
        if(t == 13):
            q = '{0} / {1} + {2}'
        else:
            q = '{2} + {0} / {1}'
    elif(t == 15 or t == 16):
        #x/y-z or z-x/y
        r = random.randint(2,10)
        y = random.randint(2,10)
        x = r * y
        if(t == 15):
            for k in range(1):
                #尽量寻找退位减法(此处不可能出现）
                z = random.randint(1, r)
                if(z % 10 > r % 10):
                    break
            q = '{0} / {1} - {2}'
        else:
            for k in range(HARD):
                z = random.randint(r, 100)
                if(z % 10 < r % 10):
                    break;
            q = '{2} - {0} / {1}'
    else:
        print("impossible")
        return None

    return q.format(x, y, z)

def test():
    for i in range(1, 17):
        for j in range(5000):
            q = generateQuestion(i)
            #print(i, q, '=', eval(q))
            if(int(eval(q)) != eval(q) or eval(q) < 0):
                print(i, "ERROR.....................", q)

def getQuestion(t):
    q = generateQuestion(t)
    q = q.replace('/', '÷')
    q = q.replace('*', '×')
    q += ' ='
    return q
    
def getRandomQuestion():
    return getQuestion(random.randint(1, 17))


def printSample():
    for i in range(1, 17):
        print(i, getQuestion(i))
    
def writeCSVFile():
    #一页，共100题
    f = open('sxt.csv', 'wt')
    for row in range(1, 21):
        for col in range(1, 6):
            f.write(getQuestion(row * col % 16 + 1))
            f.write(",") if (col<5) else None
        f.write("\n")
    f.close()

def writeHTMLFile():
    #HTML格式的一页题，100题，用于打印
    f = open('sxt.html', 'wt')
    f.write('<!DOCTYPE html>\n<html>')
    f.write('<head><meta charset="UTF-8">')
    f.write('<style type="text/css">')
    f.write('@page{margin: 0.5cm;}')
    f.write('td{text-align:left;font-size:14px; height:1.3cm; width:50cm;}')
    f.write('</style>')
    f.write('</head>')
    f.write('<body>')
    
    f.write('<table cellspacing="0" cellpadding="0">')
    for row in range(1, 21):
        f.write('<tr>')
        for col in range(1, 6):
            f.write('<td>')
            f.write(getQuestion(row * col % 16 + 1))
            f.write("</td>")
        f.write("</tr>")
    f.write('</table>')    
        
    f.write('</body>')
    f.write('</html>')
    f.close()
    
#根据命令行参数执行
if(len(sys.argv) == 1):
    writeCSVFile()
    writeHTMLFile()
    print("Done.")
elif(sys.argv[1] == 'test'):
    test()
    print("Done.")
elif(sys.argv[1] == 'sample'):
    printSample()
else:
    print("Invalid argument: ", sys.argv[1])


    