get_input_num = int(raw_input("Get First Num ?"))

while get_input_num > 0:
    out_put = raw_input("Out Put Next ?")
    if out_put == 'False':
        break
    print("num :" + str(get_input_num))
    get_input_num /= 2
