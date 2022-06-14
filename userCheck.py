import rfid_with_oled
exec(open('rfid_with_oled.py').read())

exec(open('MCP3008x.py').read())


if (op == True and canudrink == True ):
    print('yes')
    drinkop= True 
elif ((op==False) or (canudrink==False)):
    print ('No drinks anymore')
    drinkop= False 