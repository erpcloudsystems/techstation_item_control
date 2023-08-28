# Copyright (c) 2022, lxy and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProfitMargin(Document):
	

	#Call Function on Validate Form
	def on_submit(self):
		self.profit_margin()

	#For Checking that Purchase Order and Purchase Invoice is Present or Not
	def profit_margin(self):
		if self.purchase_invoice_link:
			self.check_price_list()
		elif self.purchase_order_link:
			self.check_price_list()
		frappe.msgprint("Successfully Updated Profit Margin")

	#for Checking that Price list is Selected or Not	
	def check_price_list(self):
		if self.price_list and not self.update_all_price_lists:
			self.check_item_price()
		elif self.update_all_price_lists:
			self.check_item_price()

	def check_item_price(self):
		if self.table_16 and self.price_list:
			for item in self.table_16:
				price_list=frappe.db.get_value("Item Price",{"item_code":item.get("item_code"),"price_list":self.price_list},["name"])
				if price_list:
					self.update_selling_price(price_list,item.rate)
					frappe.log_error(price_list,"price_list")
				elif not price_list:
					if self.create_a_new_price_list_for_item_not_associated_with_price_list:
						frappe.log_error(item.item_code,"New Item price_list")
						self.create_new_item_price(item.item_code,item.rate)
		elif self.table_16 and not self.price_list:
			for item in self.table_16:
				price_list=frappe.db.get_list("Item Price",filters={"item_code":item.get("item_code"),"selling":1},fields=["name"])
				if price_list:
					self.update_all_price(price_list,item.rate)
					frappe.log_error(price_list,"price_list")
				elif not price_list:
					if self.create_a_new_price_list_for_item_not_associated_with_price_list:
						self.create_new_item_price(item.item_code,item.rate)
		
		if self.table_16 and self.apply_discount:
			for item in self.table_16:
				self.update_item_dicount(item.item_code)
			
	
	def update_selling_price(self,price_list,rate):
		if price_list:
			total_rate=self.calculate_percentage(rate)
			frappe.db.set_value("Item Price",price_list,{"price_list_rate":total_rate})
	
	def update_all_price(self,price_list,rate):
		if price_list:
			for price in price_list:
				total_rate=self.calculate_percentage(rate)
				frappe.db.set_value("Item Price",price,{"price_list_rate":total_rate})
	
	def create_new_item_price(self,item_code,rate):
		if item_code:
			new_price=frappe.new_doc("Item Price")
			new_price.price_list="Standard Selling"
			new_price.price_list_rate=self.calculate_percentage(rate)
			new_price.item_code=item_code
			new_price.insert()
	
	def calculate_percentage(self,rate):
		if rate:
			total_rate=0
			if self.percentage > 0:
				if self.price_increase:
					total_rate=rate+(rate*self.percentage/100)
					frappe.log_error(total_rate,"price_list")
				if self.price_reduction:
					total_rate=rate-(rate*self.percentage/100)
					frappe.log_error(total_rate,"price_list")
			else:
				total_rate=rate
			return total_rate

	
	def update_item_dicount(self,item_code):
		if item_code:
			frappe.db.set_value("Item",item_code,{
				"mandatory_discount":self.mandatory_discount,
				"max_discount":self.max_discount
			})
	

