# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "techstation_item_control"
app_title = "Techstation Item Control"
app_publisher = "lxy"
app_description = "Generate barcode for items"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "xlee0008@student.monash.edu"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/techstation_item_control/css/techstation_item_control.css"
# app_include_js = "/assets/techstation_item_control/js/techstation_item_control.js"

# include js, css files in header of web template
# web_include_css = "/assets/techstation_item_control/css/techstation_item_control.css"
# web_include_js = "/assets/techstation_item_control/js/techstation_item_control.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
        "Stock Reconciliation" : "public/stock_reconciliation.js"
    }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "techstation_item_control.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "techstation_item_control.install.before_install"
# after_install = "techstation_item_control.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "techstation_item_control.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Item":{
        "validate":"techstation_item_control.overrides.item_validate.custom_validate"
    },
    "Price Update":{
        "on_submit":"techstation_item_control.overrides.price_update.custom_validate"
    },
    "Barcode Management":{
        "on_submit":"techstation_item_control.overrides.barcode_management.update_item_barcode"
    },
    "*":{
        "validate":"techstation_item_control.overrides.custom_validation.custom_validation"
    },
    "Re Pricing":{
        "on_submit":"techstation_item_control.overrides.re_pricing.re_pricing_item"
    },
    "Discount Update":{
        "on_submit":"techstation_item_control.overrides.discount_update.custom_validate"
    },
    "Sales Invoice":{
        "validate":"techstation_item_control.overrides.custom_validation.validate_item_rate"
    },
    "Sales Order":{
        "validate":"techstation_item_control.overrides.custom_validation.validate_item_rate"
    },
    "Delivery Note":{
        "validate":"techstation_item_control.overrides.custom_validation.validate_item_rate"
    },
    "Quotation":{
        "validate":"techstation_item_control.overrides.custom_validation.validate_item_rate"
    },
    # "Purchase Invoice":{
    #     "validate":"techstation_item_control.overrides.purchase_invoice.save_discount"
    # }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"techstation_item_control.tasks.all"
# 	],
# 	"daily": [
# 		"techstation_item_control.tasks.daily"
# 	],
# 	"hourly": [
# 		"techstation_item_control.tasks.hourly"
# 	],
# 	"weekly": [
# 		"techstation_item_control.tasks.weekly"
# 	]
# 	"monthly": [
# 		"techstation_item_control.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "techstation_item_control.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "techstation_item_control.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "techstation_item_control.task.get_dashboard_data"
# }

# fixtures
# fixtures = ['Print Format','Report', 'Role Profile', 'Role', 'Custom Field', 'Client Script', 'Property Setter', 'Workflow', 'Workflow State', 'Workflow Action']


fixtures = [{"dt": "Custom Field", "filters": [
                [
                    "name", "in", [
                        "Item-create_a_barcode_automatically","Item-automatically_create_item_code","Item-print_format","Item-mandatory_discount","Item-item_code",
                        "Item Barcode-posa_uom","Item Barcode-default_for_printing","Stock Reconciliation-scan_barcode",
                        "Stock Reconciliation-column_break_9","Stock Reconciliation-scan_mode","Stock Reconciliation-set_warehouse",
                        "Item Group-default_print_format","Item Group-default_barcode_print_format","Item Group-item_code_format","Item Group-automatically_create_a_item_code_when_adding_a_new_item","Item Group-item_code_series",
                        "Purchase Invoice-appy_mandatory_discount","Selling Settings-not_allowed_to_sell_the_item_maintain_stock_at_a_price_of_0",
                    ]
                ]
            ]},
            {"dt": "Client Script", "filters": [
                [
                    "dt", "in", [
                        "Sales Order","Sales Invoice","Delivery Note","Barcode Generator Items","Item Code Configuration","Barcode Configuration","Item","Item Barcode","Item Group",
                        "Purchase Invoice","Purchase Invoice Item","Purchase Order","Purchase Order Item","Profit Margin","Discount Update","Profit Margin Item",
                        "Re Pricing","Item Price","Barcode Printing","Barcode Management","Price Update","Barcode Items"
                    ]
                ]
                ]},

            {"dt": "Property Setter", "filters": [
                [
                    "name", "in", [
                        "Item-create_a_barcode_automatically","Item-automatically_create_item_code","Item-print_format","Item-mandatory_discount","Item-item_code",
                        "Item Barcode-posa_uom","Item Barcode-default_for_printing",
                        "Item Group-default_print_format","Item Group-default_barcode_print_format","Item Group-item_code_format","Item Group-automatically_create_a_item_code_when_adding_a_new_item","Item Group-item_code_series",
                        "Purchase Invoice-appy_mandatory_discount","Selling Settings-not_allowed_to_sell_the_item_maintain_stock_at_a_price_of_0",
                    ]
                ]
            ]
        }]

# javascript
# doctype_js = {
#     'Item':'public/js/....'
# }
# # will extend 

# # python
# override_whitelisted_methods ={
#     "":""
# }
# write in events 