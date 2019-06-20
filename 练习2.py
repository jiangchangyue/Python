a=int(input("输入一个整数:"))
b=int(input("输入一个整数:"))
c=a
d=b
if a<b:
    a,b=b,a
while b:
    a,b=b,a%b
print("两数最大公约数为：{}".format(a))
e=int(c*d/a)
print("两数的最小公倍数：{}".format(e))
