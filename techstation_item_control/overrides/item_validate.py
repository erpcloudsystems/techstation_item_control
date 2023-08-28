import frappe
import json
from frappe.model.naming import make_autoname
import random
import string

@frappe.whitelist()
def custom_validate(self,method=None):
    if not self.is_new():
        self.flags.ignore_mandatory=True
    #allow_adding_more_than_one_barcode_inside_the_item
    barcode_configuration=frappe.get_doc("Barcode Configuration")
    item_code_configuration=frappe.get_doc("Item Code Configuration")

    if barcode_configuration.get("create_a_barcode_automatically_when_adding_a_new_item"):
        self.create_a_barcode_automatically=1

    if not barcode_configuration.get("allow_adding_more_than_one_barcode_inside_the_item"):
        if len(self.barcodes)>1:
            frappe.throw("Please Activate Allow Adding Multiple Barcode In Item in Barcode Configuration")
    
    if self.create_a_barcode_automatically:
        if not barcode_configuration.get("create_a_barcode_automatically_when_adding_a_new_item"):
            frappe.throw("Please Activate Create A Barcode Automatically for Item in Barcode Configuration")
        
    if  barcode_configuration.get("create_a_barcode_automatically_when_adding_a_new_item"):
        if not barcode_configuration.get("barcode_series") and not barcode_configuration.get("generate_barcode_on_barcode_type"):
            frappe.throw("Please Enter A Barcode Series For the Item Barcode Generation")
        else:
            if self.is_new():
                if not barcode_configuration.get("generate_barcode_on_barcode_type"):
                    data=self.append('barcodes', {})
                    data.barcode=make_autoname(barcode_configuration.get("barcode_series"))
                else:
                    data=self.append('barcodes', {})
                    data.barcode=create_barcode(barcode_configuration.get("barcode_type"),barcode_configuration.get("length"))

    #Generate Item Code Automatically
    # if item_code_configuration.get("generate_item_code_without_selecting_item_group"):
    #     if item_code_configuration.get("item_code_series"):
    #         self.item_code ==make_autoname(item_code_configuration.get("item_code_series"))
    #     else:
    #         frappe.throw("Please Select An Item Barcode Series in Item Barcode Configuration")
    # else:
    #     if not self.item_group:
    #         frappe.throw("Please Select An Item group to Generate Item Code")
    #     else:
    #         check_automatic_item_creation,item_code_series=frappe.db.get_value("Item Group", self.item_group,"automatically_create_a_item_code_when_adding_a_new_item","item_code_series")
    #         if check_automatic_item_creation:
    #             if item_code_series:
    #                 self.item_code ==make_autoname(item_code_series)
    #             else:
    #                 frappe.throw("Please Select An Item Code Series in Item group to Generate Item Code")
    #         else:
    #             frappe.throw("Please Select Automatically Create A Item Code When Adding A New Item in Item Group")



    if self.barcodes:
        if len(self.barcodes) > 1:
            count=0
            for default in self.barcodes:
                if default.default_for_printing:
                    count+=1
            if count > 1:
                frappe.throw("You Can Select only one Barcode For Default printing")

@frappe.whitelist(allow_guest=True)
def generate_barcode(item):
    doc_data=frappe.get_doc("Item",item)
    barcode_configuration=frappe.get_doc("Barcode Configuration")
    barcode=""
    if  doc_data.create_a_barcode_automatically:
        if not barcode_configuration.get("generate_barcode_on_barcode_type"):
            if not barcode_configuration.get("barcode_series"):
                frappe.throw("Please Enter A Barcode Series For the Item Barcode Generation")
            else:
                barcode=make_autoname(barcode_configuration.get("barcode_series"))
        else:
            barcode=create_barcode(barcode_configuration.get("barcode_type"),barcode_configuration.get("length"))
        return barcode

@frappe.whitelist(allow_guest=True)
def generate_item_code(series):
    if series:
        item_code=make_autoname(series)
        return item_code

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


