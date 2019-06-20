str=input("请随便输入一个字符串：")
a=0
b=0
c=0
d=0
for i in range(len(str)):
    if (str[i]>='a' and str[i]<='z')or (str[i]>='A' and str[i]<='Z'):
        a=a+1
    elif str[i]>='0' and str[i]<='9':
        b=b+1
    elif str[i]==' ':
        c=c+1
    else:
        d=d+1
print("英文字符：{}".format(a))
print("数字字符：{}".format(b))
print("空格字符：{}".format(c))
print("其他字符：{}".format(d))
