sum1=0
for i in range(1,11):
    sum2=1
    for j in range(1,i+1):
        sum2=sum2*j
    sum1=sum1+sum2
print("sum:{}".format(sum1))
