import sqlite3
from SendCoin import Coupon

# Load Database
DATABASE_FILE = '/root/trc.db'

# Welcome Message and Choice
print("Welcome to Coupon Manager...")
print("1) Generate Coupons")
print("2) Clear Expired Coupons")
choice = raw_input("option: ")

# Generate Coupons
if int(choice) == 1:
	# Input Params
	coupon_num = int(raw_input("Number of Coupons: "))
	coupon_val = float(raw_input("Coupon Value: "))
	coupon_use = int(raw_input("Number of Uses: "))

	# Warning String
	chk_str = "Are you sure you want to create coupon(s) with the following "
	chk_str += "parameters(y/n):\n (Coupons: {0} / Value: {1} / Uses: {2}) \n"
	chk_str = chk_str.format(coupon_num, coupon_val, coupon_use)

	# Create Coupons
	if str(raw_input(chk_str)) == 'y':
		# Connect to Database
		conn = sqlite3.connect(DATABASE_FILE)
		mc = Coupon(conn)
		coupon_list = []

		# Create Coupons
		for i in range(coupon_num):
			coupon_list.append(mc.new(coupon_val, coupon_use))

		# Output Coupon Codes:
		print("Coupon Codes:\n")
		for i in coupon_list: print(i)
		print("Done...")
		conn.close()	

# Clear Expired Coupons
elif int(choice) == 2:
	if str(raw_input("Are you sure(y/n)?")) == 'y':
		conn = sqlite3.connect(DATABASE_FILE)
		Coupon(conn).clear()
		print("Done...")
		conn.close()	

# Close Database
print("Exiting...")