import frappe
import json



@frappe.whitelist()
def custom_validation(self,method):
    if frappe.get_meta(self.doctype).has_field("total"):
        frappe.log_error(self.as_dict())
    # else:
    #     frappe.log_error(self.as_dict())
        # frappe.msgprint(self.do)
        # meta=frappe.get_meta("Customer").has_field("total")


@frappe.whitelist()
def validate_item_rate(self,method=None):
    if self.items:
        doc_data=frappe.get_doc("Selling Settings")
        if doc_data.not_allowed_to_sell_the_item_maintain_stock_at_a_price_of_0 == 1:
            for item in self.items:
                get_stock_item=frappe.db.get_value("Item",item.item_code,"is_stock_item")
                if get_stock_item == 1:
                    if item.rate == 0:
                        frappe.throw("Stock Item Rate Can Not be 0. It Should be greater than 0")