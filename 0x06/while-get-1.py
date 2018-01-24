get_input_num = int(raw_input("Get First Number"))
while_flag = True
while while_flag:
    out_put = raw_input("Out Put Next ?")
    if out_put == "False":
    	while_flag= False
    get_input_num /= 2
    if get_input_num <= 0:
        while_flag= False
    else:
        print("num :" + str(get_input_num))
