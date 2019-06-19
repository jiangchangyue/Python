while 1:
    t = input("t:")
    R = ["RMB"]
    U = ["USD"]
    if t[0:3] in R:
        temp = float(t[3:])/6.78
        temp = "{:.2f}".format(temp)
        temp = "USD" + str(temp)
        print("结果：",temp)
    elif t[0:3] in U:
        temp = float(t[3:])*6.78
        temp = "{:.2f}".format(temp)
        temp = "RMB" + str(temp)
        print("结果：",temp)
    else:
        print("输入错误")
        
