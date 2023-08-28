import frappe
import json



@frappe.whitelist()
def re_pricing_item(self,method=None):
    if self.item_group and not self.update_all_items:
        item_list=frappe.db.get_list("Item",filters={"item_group":self.item_group},fields=['item_code'])
        update_all_items(self,item_list)
    elif self.update_all_items:
        item_list=frappe.db.get_list("Item",fields=['item_code'])
        update_all_items(self,item_list)
    frappe.msgprint("Item Price Successfully Updated")

@frappe.whitelist()
def update_all_items(self,item_list):
    if item_list:
        if self.price_list:
            for item in item_list:
                if self.last_incoming_rate:
                    purchase_rate=frappe.db.get_value("Item",item.item_code,"last_purchase_rate")
                    frappe.log_error(purchase_rate,"Update purchase_rate")
                    if purchase_rate:
                        selling_price_list=frappe.db.get_value("Item Price",{"item_code":item.item_code,"price_list":self.price_list},["name"])
                        calculate_percentage(purchase_rate,self,selling_price_list,item.item_code)
                elif self.last_valuation_rate:
                    purchase_rate=frappe.db.get_value("Stock Reconciliation Item",{"item_code":item.item_code},"valuation_rate")
                    if purchase_rate:
                        selling_price_list=frappe.db.get_value("Item Price",{"item_code":item.item_code,"price_list":self.price_list},["name"])
                        calculate_percentage(purchase_rate,self,selling_price_list,item.item_code)
                elif self.item_valuation_rate:
                    purchase_rate=frappe.db.get_value("Item",item.item_code,"valuation_rate")
                    if purchase_rate:
                        selling_price_list=frappe.db.get_value("Item Price",{"item_code":item.item_code,"price_list":self.price_list},["name"])
                        calculate_percentage(purchase_rate,self,selling_price_list,item.item_code)
        else:
            for item in item_list:
                if self.last_incoming_rate:
                    frappe.log_error(item_list,"item_list")
                    purchase_rate=frappe.db.get_value("Item",item.item_code,"last_purchase_rate")
                    if purchase_rate:
                        selling_price_list=frappe.db.get_list("Item Price",filters={"item_code":item.item_code,"selling":1},fields=["name"])
                        calculate_percentage_list(purchase_rate,self,selling_price_list,item.item_code)
                if self.last_valuation_rate:
                    frappe.log_error(item_list,"item_list")
                    purchase_rate=frappe.db.get_value("Stock Reconciliation Item",{"item_code":item.item_code},"valuation_rate")
                    if purchase_rate:
                        selling_price_list=frappe.db.get_list("Item Price",filters={"item_code":item.item_code,"selling":1},fields=["name"])
                        calculate_percentage_list(purchase_rate,self,selling_price_list,item.item_code)
                if self.item_valuation_rate:
                    frappe.log_error(item_list,"item_list")
                    purchase_rate=frappe.db.get_value("Item",item.item_code,"valuation_rate")
                    if purchase_rate:
                        selling_price_list=frappe.db.get_list("Item Price",filters={"item_code":item.item_code,"selling":1},fields=["name"])
                        calculate_percentage_list(purchase_rate,self,selling_price_list,item.item_code)


@frappe.whitelist()
def calculate_percentage(purchase_rate,self,selling_price_list,item_code):
    total_rate=0
    if self.percentage:
        if self.price_increase:
            total_rate=purchase_rate+(purchase_rate*self.percentage/100)    
        elif self.price_reduction:
            total_rate=purchase_rate-(purchase_rate*self.percentage/100)
    if selling_price_list:
        frappe.log_error(selling_price_list,"selling_price_list")
        frappe.db.set_value("Item Price",selling_price_list,"price_list_rate",total_rate)
    else:
        create_selling_price(self,total_rate,item_code)


@frappe.whitelist()
def calculate_percentage_list(purchase_rate,self,selling_price_list,item_code):
    total_rate=0
    if self.percentage:
        if self.price_increase:
            total_rate=purchase_rate+(purchase_rate*self.percentage/100)    
        elif self.price_reduction:
            total_rate=purchase_rate-(purchase_rate*self.percentage/100)
    if selling_price_list:
        for price in selling_price_list:
            frappe.db.set_value("Item Price",price.name,"price_list_rate",total_rate)
    else:
        create_selling_price(self,total_rate,item_code)
    
@frappe.whitelist()
def create_selling_price(self,total_rate,item_code):
    if self:
        if self.price_list:
            price_list_meta=frappe.new_doc("Item Price")
            if self.price_list:
                price_list_meta.item_code=item_code
                price_list_meta.price_list=self.price_list
            price_list_meta.price_list_rate=total_rate
            price_list_meta.save()
        elif not self.price_list:
            price_list_data=frappe.db.get_list("Price List",filters={"selling":1,"enabled":1},fields=["name"])
            frappe.log_error(price_list_data,"price_list_data")
            if price_list_data:
                for data in price_list_data:
                    price_list_meta=frappe.new_doc("Item Price")
                    price_list_meta.item_code=item_code
                    price_list_meta.price_list=data.name
                    price_list_meta.price_list_rate=total_rate
                    price_list_meta.save()
