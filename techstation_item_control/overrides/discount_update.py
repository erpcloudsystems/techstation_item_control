import frappe


# It will check the Apply the Discount By Purchase Invoice Or Item Group
@frappe.whitelist()
def custom_validate(self, method=None):
    if self.apply_the_discount_by == "Item Group":
        custom_validate_item_group(self)
        frappe.msgprint("Selling Price and Discount Updated According to Item Group")
    elif self.apply_the_discount_by == "Purchase Invoice":
        custom_validate_purchase_invoice(self)
        frappe.msgprint("Selling Price and Discount Updated According to Purchase Invoice")


# It will check for the Item In Item Group and All Item Group

@frappe.whitelist()
def custom_validate_item_group(self):
    if self.item_group and not self.update_all_items:
        item_list = frappe.db.get_list(
            "Item", filters={"item_group": self.item_group}, fields=["item_code"])
        if item_list:
            for item in item_list:
                update_with_group(self, item)
    elif self.update_all_items:
        item_list = frappe.db.get_list("Item", fields=["item_code"])
        if item_list:
            for item in item_list:
                update_without_group(self,item)

@frappe.whitelist()
def custom_validate_purchase_invoice(self):
    if self.purchase_invoice_link:
        get_purchase_invoice=frappe.get_doc("Purchase Invoice",self.purchase_invoice_link)
        if get_purchase_invoice.items:
            for item in get_purchase_invoice.items:
                update_with_purchase_invoice(self,item)

def update_with_purchase_invoice(self, item):
    update_discount(self, item)
    if self.apply_add_a_profit:
        item_price_list = frappe.db.get_list("Item Price", filters={
                                             "item_code": item.item_code, "selling": 1}, fields=["name", "price_list_rate"])
        if item_price_list:
            for price_name in item_price_list:
                final_price_list_rate = 0
                if self.adda_profit_rate:
                    if self.item_price_value_discount_value_final_sale_price:
                        percentage = 100-self.adda_profit_rate
                        final_price_list_rate = item.rate / \
                            (percentage/100)
                    else:
                        final_price_list_rate = item.rate + \
                            (item.rate *
                             (self.adda_profit_rate/100))
                    frappe.db.set_value("Item Price", price_name.name, {
                                        "price_list_rate": final_price_list_rate})

def update_with_group(self, item):
    update_discount(self, item)
    if self.apply_add_a_profit:
        item_price_list = frappe.db.get_list("Item Price", filters={
                                             "item_code": item.item_code, "selling": 1}, fields=["name", "price_list_rate"])
        if item_price_list:
            for price_name in item_price_list:
                final_price_list_rate = 0
                if self.adda_profit_rate:
                    if self.item_price_value_discount_value_final_sale_price:
                        percentage = 100-self.adda_profit_rate
                        final_price_list_rate = price_name.price_list_rate / \
                            (percentage/100)
                    else:
                        final_price_list_rate = price_name.price_list_rate + \
                            (price_name.price_list_rate *
                             (self.adda_profit_rate/100))
                    frappe.db.set_value("Item Price", price_name.name, {
                                        "price_list_rate": final_price_list_rate})

def update_without_group(self,item):
    update_discount(self,item)
    if self.apply_add_a_profit:
        item_price_list=frappe.db.get_list("Item Price",filters={"item_code":item.item_code,"selling":1},fields=["name","price_list_rate"])
        if item_price_list:
            for price_name in item_price_list:
                final_price_list_rate=0
                if self.adda_profit_rate:
                    if self.item_price_value_discount_value_final_sale_price:
                        percentage=100-self.adda_profit_rate
                        final_price_list_rate=price_name.price_list_rate/(percentage/100)
                    else:
                        final_price_list_rate=price_name.price_list_rate+(price_name.price_list_rate*(self.adda_profit_rate/100))
                    frappe.db.set_value("Item Price",price_name.name,{"price_list_rate":final_price_list_rate})


def update_discount(self,item):
    if self.max_discount > 0:
        frappe.db.set_value("Item",item.item_code,{"max_discount":self.max_discount,"mandatory_discount":self.mandatory_discount})
    else:
        frappe.db.set_value("Item",item.item_code,{"max_discount":0,"mandatory_discount":0})
