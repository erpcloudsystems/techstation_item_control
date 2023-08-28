// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext.stock");

frappe.ui.form.on("Stock Reconciliation", {
    validate: function(frm){
        frm.trigger("set_warehouse")
    },

	scan_barcode: function(frm) {
		let transaction_controller= new erpnext.TransactionController({frm:frm});
		transaction_controller.scan_barcode();
        frm.trigger("set_warehouse")
	},


	scan_mode: function(frm) {
		if (frm.doc.scan_mode) {
			frappe.show_alert({
				message: __("Scan mode enabled, existing quantity will not be fetched."),
				indicator: "green"
			});
		}
	},

	set_warehouse: function(frm) {
		let transaction_controller = new erpnext.TransactionController({frm:frm});
		transaction_controller.autofill_warehouse(frm.doc.items, "warehouse", frm.doc.set_warehouse);
	},
});

frappe.ui.form.on("Stock Reconciliation Item", {

	// warehouse: function(frm, cdt, cdn) {
	// 	var child = locals[cdt][cdn];
	// 	if (child.batch_no && !frm.doc.scan_mode) {
	// 		frappe.model.set_value(child.cdt, child.cdn, "batch_no", "");
	// 	}

	// 	frm.events.set_valuation_rate_and_qty(frm, cdt, cdn);
	// },

	// item_code: function(frm, cdt, cdn) {
	// 	var child = locals[cdt][cdn];
	// 	if (child.batch_no && !frm.doc.scan_mode) {
	// 		frappe.model.set_value(cdt, cdn, "batch_no", "");
	// 	}

	// 	frm.events.set_valuation_rate_and_qty(frm, cdt, cdn);
	// },

	// batch_no: function(frm, cdt, cdn) {
	// 	frm.events.set_valuation_rate_and_qty(frm, cdt, cdn);
	// },

	// qty: function(frm, cdt, cdn) {
	// 	frm.events.set_amount_quantity(frm, cdt, cdn);
	// },

	// valuation_rate: function(frm, cdt, cdn) {
	// 	frm.events.set_amount_quantity(frm, cdt, cdn);
	// },

	// serial_no: function(frm, cdt, cdn) {
	// 	var child = locals[cdt][cdn];

	// 	if (child.serial_no) {
	// 		const serial_nos = child.serial_no.trim().split('\n');
	// 		frappe.model.set_value(cdt, cdn, "qty", serial_nos.length);
	// 	}
	// },

	items_add: function(frm, cdt, cdn) {
		var item = frappe.get_doc(cdt, cdn);
		if (!item.warehouse && frm.doc.set_warehouse) {
			frappe.model.set_value(cdt, cdn, "warehouse", frm.doc.set_warehouse);
		}
	},

});


cur_frm.cscript = new erpnext.stock.StockReconciliation({frm: cur_frm});