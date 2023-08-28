import frappe
import json

@frappe.whitelist(allow_guest=True)
def get_barcode_print(item_data):
    if item_data:
        items=json.loads(item_data)
        item_list=[]
        for item in items:
            item_dict={}
            item_dict["item_code"]=item.get("item_code")
            if item.get("item_code"):
                barcode=frappe.db.get_value("Item Barcode",{"default_for_printing": 1,"parent":item.get("item_code"),"parenttype": "Item"}, "barcode")
                if barcode:
                    item_dict["item_barcode"]=barcode
                else:
                    item_dict["item_barcode"]=barcode
            if item.get("item_code"):
                default_print=frappe.db.get_value("Item",item.get("item_code"),"print_format")
                if default_print:
                    item_dict["default_print"]=default_print
                else:
                    item_dict["default_print"]=frappe.db.get_value("Item Group",item.get("item_group"),"default_barcode_print_format")
            item_list.append(item_dict)
        return item_list



@frappe.whitelist()
def get_barcode(item_code):
    barcode=""
    if item_code:
        default_barcode=frappe.db.get_list("Item Barcode",filters={"default_for_printing":1,"parent":item_code,"parenttype": "Item"},fields=['barcode'],as_list=True)
        if default_barcode:
            barcode=default_barcode[0]["barcode"]
        else:
            get_barcode_check=frappe.db.sql(f"select barcode from `tabItem Barcode` where parent='{item_code}' order by creation DESC",as_dict=1)
            barcode=get_barcode_check[0]["barcode"]
        return barcode


@frappe.whitelist(allow_guest=True)
def get_updates(name):
    # frappe.set_user("Administrator")
    if name:
        update_item_list=[]
        get_barcode_doc=frappe.get_doc("Barcode Printing",name)
        if get_barcode_doc.items:
            for item in get_barcode_doc.items:
                barcode_dict={}
                if item.item_code:
                    barcode_dict["item_code"]=item.item_code
                    barcode_dict["item_name"]=item.item_name
                    barcode_dict["item_group"]=item.item_group
                    barcode_dict["qty"]=item.qty
                    default_print=frappe.db.get_value("Item",item.item_code,"print_format")
                    if default_print:
                        barcode_dict["default_print"]=default_print
                    else:
                        print_format_list=frappe.db.get_value("Item Group",item.item_group,"default_barcode_print_format")
                        if print_format_list:
                            barcode_dict["default_print"]=print_format_list
                        else:
                            frappe.throw(f"Please Enter a Default Print Format In Item Group for Item {item.item_code}")
                    default_barcode=frappe.db.get_list("Item Barcode",filters={"default_for_printing":1,"parent":item.item_code,"parenttype": "Item"},fields=['barcode'])
                    if default_barcode:
                       barcode_dict["barcode"]=default_barcode[0]["barcode"]
                    else:
                        get_barcode_check=frappe.db.sql(f"select barcode from `tabItem Barcode` where parent='{item.item_code}' order by creation DESC",as_dict=1)
                        barcode_dict["barcode"]=get_barcode_check[0]["barcode"]
                update_item_list.append(barcode_dict)
        return update_item_list


