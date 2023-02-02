#----------------------------------------------------
# Assignment 1: Delivery
# 
# Author: Peishu Huang 
# Collaborators/References: N/A
#----------------------------------------------------
# the program below is a small business app
# it can show the order of a specific address
# it can show the summary of this week
#----------------------------------------------------

class Smallbussiness():
    '''
    this is a class, take no argument,just run it.
    '''
    def __init__(self):
        # create the zone dictionary
        self.postal_dict = {}
        self.postal_dictionary()
        # create the product dictionary
        self.product_dict = {}
        self.product_dictionary()
        # create the order dictionary
        self.order_dict = {}
        self.order_dictionary()
        # create a month dictionary
        self.month_dict = {}
        self.month_dictionary()
        # create a zone summary dictionary
        self.zone_dict = {}
        self.zone_summary_dictionary()
        # some other necessary attribute
        self.total_drivers = 0
        self.total_deliveries = 0
        self.total_income = 0
        self.total_income_this_week()
        # show the menu while the user hasn't choosen quit
        self.quit = False
        self.user_interface()
    
    def ceiling(self,number):  
        '''
        argument "number" is numerical characters
        '''
        # since no module can be imported
        # I have no choice but write a ceiling function by myself
        # it will be used in the summary part
        if int(number) == float(number):  # this means the "number" is an "integer"
            return int(number)
        else:
            return int(str(number)[0]) + 1
    
    def symbol_index(self,string,symbol):  
        '''
        the argument sting is a string, and the symbol is also a string
        '''
        # this method will find all the index of a given symbol in thegiven string
        index_list = []
        i = 0
        for character in string:
            if character == symbol:
                index_list.append(i)
            i = i + 1
        return index_list
    
    def postal_dictionary(self):  
        '''
        no argument need to take in this function
        this method will create a dictionary which keys are postal and values are zone
        '''
        # read file from zones.txt
        text = open("zones.txt", "r")
        content = text.readlines()
        text.close()
        for i in range(len(content)):
            content[i] = content[i].strip("\n")  # strip the "\n"
            
        # create a zone dictionary
        for zone_code in content:
            hashtag_index = zone_code.index("#")
            zone = zone_code[:hashtag_index]  # this is the zone string
            postal_string = zone_code[hashtag_index:]  # this is the string that contains all the postal prefix of that zone    
            comma_index_list = self.symbol_index(postal_string,",")
            comma_index_list.append(0)  # the 0 index is symbol hashtag
            for i in comma_index_list:  # postal_string[i+1] is exactly "T" of "T**"
                postal = postal_string[i+1:i+4]  # we get all the strings which have the form "T**"
                self.postal_dict[postal] = zone
                
    def product_dictionary(self):
        '''
        no argument need to take in this function
        this method will create a dictionary which keys are product ID and values are list
        the list will contain its name and price
        '''
        # read file from products.txt
        text = open("products.txt", "r")
        content = text.readlines()
        text.close()        
        for i in range(len(content)):
            content[i] = content[i].strip("\n")  # strip the "\n"    
    
        # create the product_dictionary
        for product_info in content:
            semicolon_index_list = self.symbol_index(product_info,";")
            product_id = product_info[0:semicolon_index_list[0]]  # this is the product ID
            product_name = product_info[semicolon_index_list[0]+1:semicolon_index_list[1]]  # its name
            product_price = int(product_info[semicolon_index_list[1]+1:len(product_info)])  # its label price
            self.product_dict[product_id]=[product_name,product_price]  # the value

    def order_dictionary(self):
        '''
        this method will create a dictionary which keys are the address and values are a list
        the list contains the order(s) from that address,including on which date, of what product, and of what amount
        '''
        # read file from orders.txt
        text = open("orders.txt", "r")
        content = text.readlines()
        text.close()
        for i in range(len(content)):
            content[i] = content[i].strip("\n")
            
        # create an order dictionary
        for order_info in content:
            percent_index_list = self.symbol_index(order_info,"%")  # this is the index of all %
            date = order_info[0:percent_index_list[0]]  # this is the date string
            address = order_info[percent_index_list[1]+1:percent_index_list[2]]  # this is the address string
            merchant_id = order_info[percent_index_list[2]+1:percent_index_list[3]]  # this is the product ID string
            quantity = order_info[percent_index_list[3]+1:len(order_info)]  # this is the amount string(not integer)
            # the below conditional statement will update the order to dictionary
            if self.order_dict.get(address,0) == 0:
                self.order_dict[address] = [[date,merchant_id,quantity]]  # nested list
            else:
                value= self.order_dict.get(address)
                value.append([date,merchant_id,quantity])
                self.order_dict[address] = value   
                
    def month_dictionary(self):
        '''
        this method is just for creating a month dictionary
        '''
        month_in_number = []
        for number in range(1,10):
            month = "0" + str(number)
            month_in_number.append(month)
        for number in range(10,13):
            month_in_number.append(str(number))
        month_in_letter = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
        for number,letter in zip(month_in_number,month_in_letter):  # because they are bijection, so I can use zip funtion
            self.month_dict[number]=letter
    
    def zone_summary_dictionary(self): 
        '''
        this method will create a dictionary which keys are zone and values are the order(s) number in that zone
        the order from same address will be classified to ONE order
        '''
        # read file from zones.txt
        text = open("zones.txt", "r")
        content = text.readlines()
        text.close()
        for i in range(len(content)):
            content[i] = content[i].strip("\n")  # strip the "\n"
            
        # create a zone dictionary
        for zone_code in content:
            hashtag_index = zone_code.index("#")
            zone = zone_code[:hashtag_index] 
            self.zone_dict[zone] = 0  # initializing all values to 0
            
        # calculate the total deliveries of each zone
        for address in self.order_dict.keys():
            postal = address[-7:-4]  # this is the postal of an order
            zone = self.postal_dict.get(postal)  # this will get the zone of that postal from dictionary
            self.zone_dict[zone] = self.zone_dict.get(zone) + 1  # add once
            
    def total_income_this_week(self):
        '''
        this will calculate the total income of this week (not profit)
        '''
        for order in self.order_dict.values():  # search all orders in order dictionary
            for a_buying in order:  # for each buying from a same address
                product_info= self.product_dict.get(a_buying[1])  # retrieve the info from product dictionary
                product_name = product_info[0] 
                label_price = product_info[1]
                amount = int(a_buying[2])  # the amount of one buying
                self.total_income = self.total_income + amount * label_price  # in cents
        self.total_income = self.total_income/100  # in dollars            
            
    def menu(self):
        # just the menu
        print("*"*46)
        print("Welcome to the Small Business Delivery Program")
        print("*"*46)
        print("What would you like to do?")
        print("1. Display DELIVERY SUMMARY TABLE for this week")
        print("2. Display and save DELIVERY ORDER for specific address")
        print("3. Quit")
        
    def user_interface(self):
        # just the interface
        while not self.quit:
            self.menu()
            user_option = input("> ")
            while user_option not in ["1","2","3"]:
                print("Sorry, invalid entry. Please enter a choice from 1 to 3")
                user_option = input("> ")  
            if user_option == "3":  # if user inputs this, then the interface will quit
                print("Thank you for using the Small Business Delivery Program! Goodbye. ")
                self.quit = True
            elif user_option == "2":
                address = input("Address: ")
                self.delivery_order_receipt(address)
            elif user_option == "1":
                self.summary_print()
            
    def delivery_order_receipt(self,address):
        '''
        this method will print the delivery order receipt of a given address, if address valid
        the address argument is a string
        '''
        if address in self.order_dict.keys():
            current_order = self.order_dict.get(address)
            current_order.sort()  # so that the content will be sorted by date
            self.order_print(address,current_order)
        else:
            print("Invalid address. ")
            
    def order_print(self,address,order_list):
        '''
        this method will print a receipt
        the address argunment is a string(no matter valid or not)
        the order_list argument is a list and takes from the order_dict
        '''
        # this is a part of the receipt --- the title of it
        print("\n")
        self.save_as_invoice("\n")
        if len(address) <= 29:
            line1 = "Delivery for:" + "{:>32}".format(address)  # this is line 1 when address lenth is not greater than 29
            print(line1)
            self.save_as_invoice(line1+"\n")
        else:
            line1 = "Delivery for:" + "{:>31}*".format(address[:29])  # this is also line 1 but lenth greater than 29
            print(line1)
            self.save_as_invoice(line1+"\n")            
        line2 = "="*45  # this is line2
        print(line2)
        self.save_as_invoice(line2+"\n")        
        line3 = "%s%s%s%s%s%s" % ("Date"," "*4,"Item"," "*24,"Price"," "*4)  # this is line 3
        print(line3)
        self.save_as_invoice(line3+"\n")        
        line4 = "%s  %s  %s" % ("-"*6,"-"*26,"-"*9)  # this is line 4
        print(line4)
        self.save_as_invoice(line4+"\n")        
        # the below is the order infomation
        self.orderprint_main_part(order_list)
        print("\n")
        self.save_as_invoice("\n")

    def orderprint_main_part(self,order_list):
        # this is the main part of the receipt
        # it contains which product the customer(s) bought, on what date, of what amount, and paid how much (under the same address)
        # and it also contains the total paid from a same address
        total_price = 0
        for an_order in order_list:
            month = self.month_dict.get(an_order[0][5:7])
            date = an_order[0][-2:]
            product_info= self.product_dict.get(an_order[1])
            product_name = product_info[0]
            label_price = product_info[1]
            amount = int(an_order[2])
            price = amount * label_price  # in cents
            total_price = total_price + price
            if len(product_name) > 19:
                productline = "{0:^3} {1:^2}  {2:{fill}>3} x {3:<19}*  ${4:>8.2f}".format(month,date,str(amount),product_name[:19],price/100,fill = "0")
                print(productline)
                self.save_as_invoice(productline+"\n")
            else:
                productline = "{0:^3} {1:^2}  {2:{fill}>3} x {3:<19}   ${4:>8.2f}".format(month,date,str(amount),product_name,price/100,fill = "0")
                print(productline)
                self.save_as_invoice(productline+"\n")                
        print("{0:^36}{1:{fill}^9}".format(" ","",fill = "-"))
        self.save_as_invoice("{0:^36}{1:{fill}^9}".format(" ","",fill = "-")+"\n")
        print("{0:^36}${1:>8.2f}".format(" ",total_price/100)) 
        self.save_as_invoice("{0:^36}${1:>8.2f}".format(" ",total_price/100)+"\n")
        
    def summary_print(self):
        '''
        this method will print the summary of this week
        and it takes no argument
        '''
        # the below is title
        print("\n")
        print("+{0:{fill}^15}+{1:{fill}^12}+{2:{fill}^11}+".format("","","",fill = "-"))
        print("|{0:^15}|{1:^12}|{2:^11}|".format("Delivery Zone","Deliveries","Drivers"))
        print("+{0:{fill}^15}+{1:{fill}^12}+{2:{fill}^11}+".format("","","",fill = "-"))
        
        # the below is the summary of each zone
        self.summary_part1()
        print("+{0:{fill}^15}+{1:{fill}^12}+{2:{fill}^11}+".format("","","",fill = "-"))
        
        # the below is the summary of all
        self.summary_part2()   
        print("+{0:{fill}^15}+{1:{fill}^12}+{2:{fill}^11}+".format("","","",fill = "-"))
        print("\n")
    
    def summary_part1(self):
        # this method will print the summary of each zone in sorted 
        for key in sorted(self.zone_dict):
            if self.zone_dict[key] != 0:
                self.total_deliveries = self.total_deliveries + self.zone_dict[key]
                drivers = self.ceiling(self.zone_dict[key]/10)
                self.total_drivers = self.total_drivers + drivers
                print("|{0:^15}|{1:^12}|{2:^11}|".format(key,self.zone_dict[key],drivers)) 
                
    def summary_part2(self):
        # this will print the summary of all
        percentage = ((self.total_deliveries*12)/self.total_income)*100
        print("|{0:^22}{1:>17} |".format("Total drivers needed", self.total_drivers))
        print("|{0:^21}{1:>10}{2:>8.2f} |".format("Total delivery cost","$",self.total_deliveries*12))
        print("|{0:^25}{1:>13.1f}% |".format("Delivery cost/purchases",percentage))
    
    def save_as_invoice(self,content):
        '''
        the content argument is a string
        this method will save the content to a txt called invoice
        '''
        file = open("invoice.txt","a")
        file.write(content)
        file.close()

def main():
    # just a main function
    table = Smallbussiness()

main()