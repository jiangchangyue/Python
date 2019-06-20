a=input("输入一个五位数:")
i=0
j=len(a)-1
while i<=j:
    if a[i]!=a[j]:
        break
    else:
        i=i+1
        j=j-1
if i>=j:
    print("是回文数.")
else:
    print("不是回文数.")
