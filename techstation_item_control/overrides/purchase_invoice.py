import frappe
from frappe.model.mapper import get_mapped_doc



@frappe.whitelist()
def map_purchase_invoice(source_name, target_doc=None,ignore_permissions=False):
    def set_missing_values(source, target):
        if source.name:
            target.purchase_invoice = 1
        if source.items:
            for item in source.items:
                data=target.append('table_16', {})
                data.item_code=item.item_code
                data.item_name=item.item_name
                data.qty=item.qty
                data.rate=item.rate
                data.amount=item.amount
			
    doclist = get_mapped_doc(
        "Purchase Invoice",
        source_name,
        {
            "Purchase Invoice": {
                "doctype": "Profit Margin",
                "field_map": {
                    "name": "purchase_invoice_link"
                },
                "Purchase Invoice Item": {
                    "doctype": "Profit Margin Item",
                    
				
			    },
            }
        },
        target_doc,
        set_missing_values,
        ignore_permissions=ignore_permissions,
    )
    return doclist


@frappe.whitelist()
def save_discount(self,method=None):
    if self.apply_mandatory_discount:
        if self.items:
            for item in self.items:
                get_discount=frappe.db.get_value("Item",item.item_code,"max_discount")
                if get_discount:
                    item.discount_percentage=get_discount
            # self.calculate_taxes_and_totals()
    elif not self.apply_mandatory_discount:
        if self.items:
            for item in self.items:
                # get_discount=frappe.db.get_value("Item",item.item_code,"max_discount")
                # if get_discount:
                item.discount_percentage=0
    # self.save()
            # self.calculate_taxes_and_totals()