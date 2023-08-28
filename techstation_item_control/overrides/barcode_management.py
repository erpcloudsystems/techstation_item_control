import frappe
from frappe.model.naming import make_autoname
import json
import random
import string


@frappe.whitelist(allow_guest=True)
def update_item_and_barcode(item_group):
    if item_group:
        get_list=frappe.db.get_list("Item",filters={"item_group":item_group},fields=["item_name","item_code"])
        return get_list
    elif not item_group:
        get_list=frappe.db.get_list("Item",fields=["item_name","item_code"])
        return get_list


@frappe.whitelist(allow_guest=True)
def update_barcode():
    get_series=frappe.get_doc("Barcode Configuration")
    if get_series.generate_barcode_on_barcode_type:
        barcode = create_barcode(get_series.get("barcode_type"),get_series.get("length"))
        return barcode
    else:
        barcode=make_autoname(get_series.barcode_series)
        return barcode


#Create A Barcode Based On Barcode Type
def create_barcode(barcode_type,length_data=None):
    barcode=""
    if barcode_type:
        if barcode_type == "CODE 128":
            barcode = get_random_string(length_data)
        elif barcode_type == "EAN-13":
            barcode = get_random_number(12)
        elif barcode_type == "UPC-A":
            barcode = get_random_number(11)
    return barcode


def get_random_string(length):
	# choose from all lowercase letter
	letters = string.ascii_uppercase
	# call random.choices() string module to find the string in Uppercase + numeric data.
	result_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))    
	return result_str

def get_random_number(length):
	# choose from all lowercase letter
	letters = string.ascii_uppercase
	# call random.choices() string module to find the string in Uppercase + numeric data.
	result_str = ''.join(random.choices(string.digits, k = length))    
	return result_str


@frappe.whitelist(allow_guest=True)
def get_item(data):
    doc_data=json.loads(data)
    if doc_data.get("item_group"):
        if doc_data.get("table_5"):
            item_group_list=frappe.db.get_list("Item",filters={"item_group":doc_data.get("item_group")},fields=["item_name","item_code"])
            list_return=list_contains(doc_data.get("table_5"),item_group_list)
            return list_return
            # item_group_list
        elif not doc_data.get("table_5"):
            get_list=frappe.db.get_list("Item",filters={"item_group":doc_data.get("item_group")},fields=["item_name","item_code"])
            item_list=[]
            if get_list:
                for item in get_list:
                    data_dict={}
                    data_dict["item_code"]=item.item_code
                    data_dict["item_name"]=item.item_name
                    data_dict["barcode"]=update_barcode()
                    item_list.append(data_dict)
                return item_list
            #item_group_list
    elif doc_data.get("update_all_item_group"):
        if doc_data.get("table_5"):
            item_group_list=frappe.db.get_list("Item",fields=["item_name","item_code"])
            list_return=list_contains(doc_data.get("table_5"),item_group_list)
            return list_return
            # item_group_list
        elif not doc_data.get("table_5"):
            get_list=frappe.db.get_list("Item",fields=["item_name","item_code"])
            item_list=[]
            if get_list:
                for item in get_list:
                    data_dict={}
                    data_dict["item_code"]=item.item_code
                    data_dict["item_name"]=item.item_name
                    data_dict["barcode"]=update_barcode()
                    item_list.append(data_dict)
                return item_list
            #item_group_list
        


def list_contains(table_5, item_group_list):
     # Iterate in the 1st list
    final_list=[]
    for item in item_group_list:
        data_dict={}
        for n in table_5:
            if item.item_code == n.get("item"):
                data_dict["item_code"]=n.get("item")
                data_dict["item_name"]=n.get("item_name")
                data_dict["barcode"]=n.get("barcode")
                break
            elif item.item_code != n.get("item"):
                data_dict["item_code"]=item.item_code
                data_dict["item_name"]=item.item_name
                data_dict["barcode"]=update_barcode()

        final_list.append(data_dict)
    return final_list


@frappe.whitelist()
def update_item_barcode(self,method=None):
    if self.type == "Generate Barcode":
        if self.get("table_5"):
            for item in self.get("table_5"):
                item_doc=frappe.get_doc("Item",item.item)
                data=item_doc.append('barcodes', {})
                data.barcode=item.barcode
                item_doc.flags.ignore_mandatory=True
                item_doc.save()
                frappe.msgprint("Barcode Updated Successfully")
    elif self.type == "Delete Barcode":
        if self.get("table_5"):
            for item in self.get("table_5"):
                if item.barcode != "There are Multiple Barcodes":
                    frappe.db.sql(f"""delete from `tabItem Barcode` where barcode = '{item.barcode}' and parent='{item.item}'""")
                else:
                    frappe.db.sql(f"""delete from `tabItem Barcode` where parent='{item.item}'""")
            frappe.msgprint("Barcode Deleted Successfully")


@frappe.whitelist(allow_guest=True)
def delete_item_group(data):
    doc_data=json.loads(data)
    if doc_data.get("item_group"):
        item_group_list=frappe.db.get_list("Item",filters={"item_group":doc_data.get("item_group")},fields=["item_name","item_code"])
        item_delete_list=[]
        if item_group_list:
            for item in item_group_list:
                item_doc=frappe.get_doc("Item",item.item_code)
                dict_data={}
                dict_data["item_code"]=item.item_code
                dict_data["item_name"]=item.item_name
                if len(item_doc.barcodes) >1 :
                    dict_data["barcode"]="There are Multiple Barcodes"
                else:
                    dict_data["barcode"]=item_doc.barcodes[0].barcode
                item_delete_list.append(dict_data)

        return item_delete_list
    elif doc_data.get("update_all_item_group"):
        item_group_list=frappe.db.get_list("Item",fields=["item_name","item_code"])
        item_delete_list=[]
        if item_group_list:
            for item in item_group_list:
                item_doc=frappe.get_doc("Item",item.item_code)
                dict_data={}
                dict_data["item_code"]=item.item_code
                dict_data["item_name"]=item.item_name
                if item_doc.barcodes:
                    if len(item_doc.barcodes) >1 :
                        dict_data["barcode"]="There are Multiple Barcodes"
                    else:
                        dict_data["barcode"]=item_doc.barcodes[0].barcode
                item_delete_list.append(dict_data)

        return item_delete_list
