import frappe



@frappe.whitelist()
def custom_validate(self,method=None):
    if self.item_group and not self.update_all_items:
        item_list=frappe.db.get_list("Item",filters={"item_group":self.item_group},fields=['item_code'])
        if item_list:
            if not self.price_list:
                for item in item_list:
                    get_item_price=[]
                    if self.selling:
                        get_item_price=frappe.db.get_list("Item Price",filters={"item_code":item.item_code,"selling":1},fields=["price_list_rate","name"])
                    elif self.buying:
                        get_item_price=frappe.db.get_list("Item Price",filters={"item_code":item.item_code,"buying":1},fields=["price_list_rate","name"])
                
                    if get_item_price:
                        for price in get_item_price:
                            price_rate=price.price_list_rate*(self.percentage/100)
                            if self.price_increase:
                                frappe.db.set_value('Item Price',price.name, {
                                        'price_list_rate': price.price_list_rate+price_rate
                                    })
                            elif self.price_reduction:
                                frappe.db.set_value('Item Price',price.name, {
                                        'price_list_rate': price.price_list_rate-price_rate
                                    })
            else:
                for item in item_list:
                    get_item_price=[]
                    get_item_price=frappe.db.get_list("Item Price",filters={"item_code":item.item_code,"price_list":self.price_list},fields=["price_list_rate","name"])
                
                    if get_item_price:
                        for price in get_item_price:
                            price_rate=price.price_list_rate*(self.percentage/100)
                            if self.price_increase:
                                frappe.db.set_value('Item Price',price.name, {
                                        'price_list_rate': price.price_list_rate+price_rate
                                    })
                            elif self.price_reduction:
                                frappe.db.set_value('Item Price',price.name, {
                                        'price_list_rate': price.price_list_rate-price_rate
                                    })
    elif self.update_all_items:
        item_list=frappe.db.get_list("Item",fields=['item_code'])
        frappe.log_error(item_list,"Item List")
        if item_list:
            if not self.price_list:
                for item in item_list:
                    get_item_price=[]
                    if self.selling:
                        get_item_price=frappe.db.get_list("Item Price",filters={"item_code":item.item_code,"selling":1},fields=["price_list_rate","name"])
                    elif self.buying:
                        get_item_price=frappe.db.get_list("Item Price",filters={"item_code":item.item_code,"buying":1},fields=["price_list_rate","name"])
                
                    if get_item_price:
                        for price in get_item_price:
                            price_rate=price.price_list_rate*(self.percentage/100)
                            if self.price_increase:
                                frappe.db.set_value('Item Price',price.name, {
                                        'price_list_rate': price.price_list_rate+price_rate
                                    })
                            elif self.price_reduction:
                                frappe.db.set_value('Item Price',price.name, {
                                        'price_list_rate': price.price_list_rate-price_rate
                                    })
            else:
                for item in item_list:
                    get_item_price=[]
                    get_item_price=frappe.db.get_list("Item Price",filters={"item_code":item.item_code,"price_list":self.price_list},fields=["price_list_rate","name"])
                
                    if get_item_price:
                        for price in get_item_price:
                            price_rate=price.price_list_rate*(self.percentage/100)
                            if self.price_increase:
                                frappe.db.set_value('Item Price',price.name, {
                                        'price_list_rate': price.price_list_rate+price_rate
                                    })
                            elif self.price_reduction:
                                frappe.db.set_value('Item Price',price.name, {
                                        'price_list_rate': price.price_list_rate-price_rate
                                    })

    
    frappe.msgprint("Item Price Update Successfully")
                        