import frappe
from frappe.model.mapper import get_mapped_doc



@frappe.whitelist()
def map_purchase_order(source_name, target_doc=None,ignore_permissions=False):
    def set_missing_values(source, target):
        if source.name:
            target.purchase_order = 1
        if source.items:
            for item in source.items:
                data=target.append('table_16', {})
                data.item_code=item.item_code
                data.item_name=item.item_name
                data.qty=item.qty
                data.rate=item.rate
                data.amount=item.amount
			
    doclist = get_mapped_doc(
        "Purchase Order",
        source_name,
        {
            "Purchase Order": {
                "doctype": "Profit Margin",
                "field_map": {
                    "name": "purchase_order_link"
                },
                "Purchase Order Item": {
                    "doctype": "Profit Margin Item",
                    
				
			    },
            }
        },
        target_doc,
        set_missing_values,
        ignore_permissions=ignore_permissions,
    )
    return doclist