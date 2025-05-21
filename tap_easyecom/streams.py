"""Stream type classes for tap-easyecom."""

from typing import Any, Dict, Iterable, Optional, List
from singer_sdk import typing as th
from tap_easyecom.client import EasyEcomStream
from datetime import datetime, timedelta
import pytz
import copy
from singer_sdk.exceptions import InvalidStreamSortException
from singer_sdk.helpers._state import (
    finalize_state_progress_markers,
    log_sort_error,
)


class ProductsStream(EasyEcomStream):
    name = "products"
    path = "/Products/GetProductMaster"
    primary_keys = ["product_id"]
    replication_key = "updated_at"
    additional_params = {"custom_fields": "1"}

    schema = th.PropertiesList(
        th.Property("cp_id", th.IntegerType),
        th.Property("product_id", th.IntegerType),
        th.Property("sku", th.StringType),
        th.Property("product_name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("inventory", th.IntegerType),
        th.Property("product_type", th.StringType),
        th.Property("brand", th.StringType),
        th.Property("colour", th.StringType),
        th.Property("category_id", th.IntegerType),
        th.Property("brand_id", th.IntegerType),
        th.Property("accounting_sku", th.StringType),
        th.Property("accounting_unit", th.StringType),
        th.Property("category_name", th.StringType),
        th.Property("expiry_type", th.IntegerType),
        th.Property("company_name", th.StringType),
        th.Property("c_id", th.IntegerType),
        th.Property("height", th.NumberType),
        th.Property("length", th.NumberType),
        th.Property("width", th.NumberType),
        th.Property("weight", th.NumberType),
        th.Property("cost", th.NumberType),
        th.Property("mrp", th.NumberType),
        th.Property("size", th.StringType),
        th.Property("cp_sub_products_count", th.IntegerType),
        th.Property("model_no", th.StringType),
        th.Property("hsn_code", th.StringType),
        th.Property("tax_rate", th.NumberType),
        th.Property("product shelf life", th.IntegerType),
        th.Property("product_image_url", th.StringType),
        th.Property("vendor_code", th.ArrayType(th.StringType)),
        th.Property("cp_inventory", th.IntegerType),
        th.Property(
                    "custom_fields",
                        th.CustomType({"type": ["array", "object"]}),
        ),
        th.Property(
            "variants",
            th.ArrayType(
                th.ObjectType(
                    th.Property("sku", th.StringType),
                    th.Property("parent_cpId", th.IntegerType),
                    th.Property("cpId", th.IntegerType),
                    th.Property("active", th.IntegerType),
                    th.Property("accounting_sku", th.StringType),
                    th.Property("accounting_unit", th.StringType),
                    th.Property("product_id", th.IntegerType),
                    th.Property("product_name", th.StringType),
                    th.Property("created_at", th.DateTimeType),
                    th.Property("inventory", th.IntegerType),
                    th.Property("brand", th.StringType),
                    th.Property("colour", th.StringType),
                    th.Property("category_id", th.IntegerType),
                    th.Property("category_name", th.StringType),
                    th.Property("height", th.NumberType),
                    th.Property("length", th.NumberType),
                    th.Property("width", th.NumberType),
                    th.Property("weight", th.NumberType),
                    th.Property("cost", th.NumberType),
                    th.Property("mrp", th.NumberType),
                    th.Property("size", th.StringType),
                    th.Property("model_no", th.StringType),
                    th.Property("EANUPC", th.StringType),
                    th.Property("hsn_code", th.StringType),
                    th.Property("product shelf life", th.IntegerType),
                    th.Property("product_image_url", th.StringType),
                    th.Property("brand_id", th.IntegerType),
                    th.Property("cp_inventory", th.IntegerType),
                    th.Property("tax_rate", th.NumberType),
                    th.Property("tax_rule_name", th.StringType),
                    th.Property(
                        "custom_fields",
                            th.ArrayType(
                                th.ObjectType(
                                th.Property("cp_id", th.IntegerType),
                                th.Property("field_name", th.StringType),
                                th.Property("value", th.StringType),
                                th.Property("enabled", th.IntegerType),
                                )
                            ),
                    ),
                )
            ),
        ),
        th.Property(
            "sub_products",
            th.ArrayType(
                th.ObjectType(
                    th.Property("sku", th.StringType),
                    th.Property("combo_cp_id", th.IntegerType),
                    th.Property("quantity", th.IntegerType),
                    th.Property("cpId", th.IntegerType),
                    th.Property("accounting_sku", th.StringType),
                    th.Property("accounting_unit", th.StringType),
                    th.Property("product_id", th.IntegerType),
                    th.Property("product_name", th.StringType),
                    th.Property("height", th.NumberType),
                    th.Property("length", th.NumberType),
                    th.Property("width", th.NumberType),
                    th.Property("weight", th.NumberType),
                    th.Property("cost", th.NumberType),
                    th.Property("mrp", th.NumberType),
                    th.Property("size", th.StringType),
                    th.Property("model_no", th.StringType),
                    th.Property("EANUPC", th.StringType),
                    th.Property("hsn_code", th.StringType),
                    th.Property("product shelf life", th.IntegerType),
                    th.Property("product_image_url", th.StringType),
                    th.Property("brand_id", th.IntegerType),
                    th.Property("cp_inventory", th.IntegerType),
                    th.Property("tax_rate", th.NumberType),
                    th.Property("tax_rule_name", th.StringType),
                    th.Property(
                        "additional_images",
                            th.ArrayType(th.StringType),
                    ),
                        th.Property(
                            "custom_fields",
                                th.CustomType({"type": ["array", "object"]}),
                    ),
                )
            ),
        ),
    ).to_dict()


class SuppliersStream(EasyEcomStream):
    name = "suppliers"
    path = "/wms/V2/getVendors"
    primary_keys = ["vendor_c_id"]

    schema = th.PropertiesList(
        th.Property("vendor_name", th.StringType),
        th.Property("vendor_c_id", th.IntegerType),
        th.Property("vendor_code", th.StringType),
        th.Property("firstname ", th.StringType),
        th.Property("lastname", th.StringType),
        th.Property("email", th.StringType),
        th.Property(
            "address",
            th.ObjectType(
                th.Property(
                    "dispatch",
                    th.CustomType({"type": ["array", "object"]}),
                ),
                th.Property(
                    "billing",
                    th.CustomType({"type": ["array", "object"]}),
                ),
            ),
        ),
    ).to_dict()

class ProductCompositionsStream(EasyEcomStream):
    name = "product_compositions"
    path = "/Products/getKits"
    primary_keys = ["c_id"]

    schema = th.PropertiesList(
        th.Property("product_id", th.IntegerType),
        th.Property("sku", th.StringType),
        th.Property("accounting_sku", th.StringType),
        th.Property("accounting_unit", th.StringType),
        th.Property("mrp", th.NumberType),
        th.Property("add_date", th.DateTimeType),
        th.Property("lastUpdateDate", th.DateTimeType),
        th.Property("cost", th.NumberType),
        th.Property("HSNCode", th.StringType),
        th.Property("colour", th.StringType),
        th.Property("weight", th.NumberType),
        th.Property("height", th.NumberType),
        th.Property("length", th.NumberType),
        th.Property("width", th.NumberType),
        th.Property("size", th.StringType),
        th.Property("material_type", th.IntegerType),
        th.Property("modelNumber", th.StringType),
        th.Property("modelName", th.StringType),
        th.Property("category", th.StringType),
        th.Property("brand", th.StringType),
        th.Property("c_id", th.IntegerType),
        th.Property(
                    "subProducts",
                    th.CustomType({"type": ["array", "object"]}),
                ),
    ).to_dict()


class SellOrdersStream(EasyEcomStream):
    name = "sell_orders"
    path = "/orders/V2/getAllOrders"
    primary_keys = ["order_id"]
    records_jsonpath = "$.data.orders[*]"
    replication_key = "last_update_date"
    start_date = None
    end_date = None
    today = None
    page_size = 50

    schema = th.PropertiesList(
        th.Property("suborders", th.CustomType({"type": ["array", "string"]})),
        th.Property("invoice_id", th.IntegerType),
        th.Property("order_id", th.IntegerType),
        th.Property("queue_message", th.StringType),
        th.Property("queue_status", th.IntegerType),
        th.Property("order_priority", th.IntegerType),
        th.Property("blockSplit", th.IntegerType),
        th.Property("reference_code", th.StringType),
        th.Property("company_name", th.StringType),
        th.Property("location_key", th.StringType),
        th.Property("warehouseId", th.IntegerType),
        th.Property("seller_gst", th.StringType),
        th.Property("import_warehouse_id", th.IntegerType),
        th.Property("import_warehouse_name", th.StringType),
        th.Property("pickup_address", th.StringType),
        th.Property("pickup_city", th.StringType),
        th.Property("pickup_state", th.StringType),
        th.Property("pickup_state_code", th.StringType),
        th.Property("pickup_pin_code", th.StringType),
        th.Property("pickup_country", th.StringType),
        th.Property("invoice_currency_code", th.StringType),
        th.Property("order_type", th.StringType),
        th.Property("order_type_key", th.StringType),
        th.Property("replacement_order", th.IntegerType),
        th.Property("marketplace", th.StringType),
        th.Property("marketplace_id", th.IntegerType),
        th.Property("qcPassed", th.IntegerType),
        th.Property("salesmanUserId", th.IntegerType),
        th.Property("order_date", th.DateTimeType),
        th.Property("tat", th.DateTimeType),
        th.Property("available_after", th.DateTimeType),
        th.Property("invoice_date", th.DateTimeType),
        th.Property("import_date", th.DateTimeType),
        th.Property("last_update_date", th.DateTimeType),
        th.Property("manifest_date", th.DateTimeType),
        th.Property("manifest_no", th.StringType),
        th.Property("invoice_number", th.StringType),
        th.Property("marketplace_invoice_num", th.StringType),
        th.Property("shipping_last_update_date", th.DateTimeType),
        th.Property("batch_id", th.CustomType({"type": ["string","number"]})),
        th.Property("batch_created_at", th.DateTimeType),
        th.Property("message", th.StringType),
        th.Property("courier_aggregator_name", th.StringType),
        th.Property("courier", th.StringType),
        th.Property("carrier_id", th.IntegerType),
        th.Property("awb_number", th.StringType),
        # TODO: what??
        th.Property("Package Weight", th.NumberType),
        th.Property("Package Height", th.NumberType),
        th.Property("Package Length", th.NumberType),
        th.Property("Package Width", th.NumberType),
        th.Property("order_status", th.StringType),
        th.Property("order_status_id", th.IntegerType),
        th.Property("suborder_count", th.CustomType({"type": ["string","integer"]})),
        th.Property("shipping_status", th.StringType),
        th.Property("shipping_status_id", th.IntegerType),
        th.Property(
            "shipping_history",
            th.ArrayType(th.ObjectType(
                th.Property("qc_pass_datetime", th.DateTimeType),
                th.Property("confirm_datetime", th.DateTimeType),
                th.Property("print_datetime", th.DateTimeType),
                th.Property("manifest_datetime", th.DateTimeType),
            )),
        ),
        th.Property("delivery_date", th.DateTimeType),
        th.Property("payment_mode", th.StringType),
        th.Property("payment_mode_id", th.IntegerType),
        th.Property("payment_gateway_transaction_number", th.StringType),
        th.Property("payment_gateway_name", th.StringType),
        th.Property("buyer_gst", th.StringType),
        th.Property("customer_name", th.StringType),
        th.Property("contact_num", th.StringType),
        th.Property("address_line_1", th.StringType),
        th.Property("address_line_2", th.StringType),
        th.Property("city", th.StringType),
        th.Property("pin_code", th.StringType),
        th.Property("state", th.StringType),
        th.Property("state_code", th.StringType),
        th.Property("country", th.StringType),
        th.Property("email", th.StringType),
        th.Property("latitude", th.StringType),
        th.Property("longitude", th.StringType),
        th.Property("billing_name", th.StringType),
        th.Property("billing_address_1", th.StringType),
        th.Property("billing_address_2", th.StringType),
        th.Property("billing_city", th.StringType),
        th.Property("billing_state", th.StringType),
        th.Property("billing_state_code", th.StringType),
        th.Property("billing_pin_code", th.StringType),
        th.Property("billing_country", th.StringType),
        th.Property("billing_mobile", th.StringType),
        th.Property("order_quantity", th.IntegerType),
        th.Property("meta", th.CustomType({"type": ["object", "null"]})),
        th.Property("documents", th.ObjectType(
            th.Property("originalLabelUrl", th.StringType),
            th.Property("easyecom_invoice", th.StringType),
            th.Property("label", th.StringType),
            th.Property("intaxform", th.StringType),
            th.Property("outtaxform", th.StringType),
            th.Property("marketplaceinvoice", th.StringType),
            th.Property("marketplace_tax_invoice", th.StringType),
        )),
        th.Property("total_amount", th.NumberType),
        th.Property("total_tax", th.NumberType),
        th.Property("total_shipping_charge", th.NumberType),
        th.Property("total_discount", th.NumberType),
        th.Property("collectable_amount", th.NumberType),
        th.Property("tcs_rate", th.CustomType({"type": ["number", "string"]})),
        th.Property("tcs_amount", th.NumberType),
        th.Property("customer_code", th.CustomType({"type": ["number", "string"]})),
        th.Property("fulfillable_status", th.IntegerType),
    ).to_dict()

    def get_next_page_token(self, response, previous_token):
        next_page_token = super().get_next_page_token(response, previous_token)
        if next_page_token:
            next_page_token = next_page_token[0]
        if not next_page_token and self.end_date and self.today and self.end_date < self.today:
            return f"iterate_{self.start_date}"
        return next_page_token
    
    def get_url_params(self, context, next_page_token):
        params = dict()
        if self.page_size:
            params["limit"] = self.page_size
        if next_page_token and not next_page_token.startswith("iterate"):
            params["cursor"] = next_page_token

        # Initialize today, start_date and end_date
        if self.start_date is None:
            self.today = pytz.utc.localize(datetime.utcnow())
            self.start_date = self.get_starting_time(context)
            self.end_date = self.start_date + timedelta(days=7)

        # move to the next date chunk
        if next_page_token and next_page_token.startswith("iterate"):
            self.start_date = self.end_date - timedelta(seconds=1)         
            self.end_date = self.start_date + timedelta(days=7, seconds=1)

        params["updated_after"] = self.start_date.strftime('%Y-%m-%d %H:%M:%S')
        params["updated_before"] = self.end_date.strftime('%Y-%m-%d %H:%M:%S')

        return params
    

class BuyOrdersStream(EasyEcomStream):
    name = "buy_orders"
    path = "/wms/V2/getPurchaseOrderDetails"
    primary_keys = ["po_id"]
    replication_key = "po_updated_date"

    schema = th.PropertiesList(
        th.Property("po_items", th.CustomType({"type": ["array", "string"]})),
        th.Property("po_id", th.IntegerType),
        th.Property("total_po_value", th.StringType),
        th.Property("po_number", th.IntegerType),
        th.Property("po_ref_num", th.StringType),
        th.Property("po_status_id", th.IntegerType),
        th.Property("po_created_date", th.DateTimeType),
        th.Property("po_updated_date", th.DateTimeType),
        th.Property("po_created_warehouse", th.StringType),
        th.Property("po_created_warehouse_c_id", th.IntegerType),
        th.Property("vendor_name", th.StringType),
        th.Property("vendor_c_id", th.IntegerType),
        th.Property("vendor_code", th.StringType),
    ).to_dict()


class ReceiptsStream(EasyEcomStream):
    name = "receipts"
    path = "/Grn/V2/getGrnDetails"
    primary_keys = ["grn_id"]
    replication_key = "po_created_date"
    date_filter_param = "created_after"

    schema = th.PropertiesList(
        th.Property("grn_id", th.IntegerType),
        th.Property("grn_invoice_number", th.StringType),
        th.Property("total_grn_value", th.NumberType),
        th.Property("grn_status_id", th.IntegerType),
        th.Property("grn_status", th.StringType),
        th.Property("grn_created_at", th.DateTimeType),
        th.Property("grn_invoice_date", th.DateType),
        th.Property("po_id", th.IntegerType),
        th.Property("po_number", th.IntegerType),
        th.Property("po_ref_num", th.StringType),
        th.Property("po_status_id", th.IntegerType),
        th.Property("po_created_date", th.DateTimeType),
        th.Property("po_updated_date", th.DateTimeType),
        th.Property("inwarded_warehouse", th.StringType),
        th.Property("inwarded_warehouse_c_id", th.IntegerType),
        th.Property("vendor_name", th.StringType),
        th.Property("vendor_c_id", th.IntegerType),
        th.Property("grn_items", th.CustomType({"type": ["array", "string"]})),
    ).to_dict()


class ReturnsStream(EasyEcomStream):
    name = "returns"
    path = "/orders/getAllReturns"
    primary_keys = ["credit_note_id"]
    records_jsonpath = "$.data.credit_notes[*]"

    schema = th.PropertiesList(
        th.Property("credit_note_id", th.IntegerType),
        th.Property("invoice_id", th.IntegerType),
        th.Property("order_id", th.IntegerType),
        th.Property("reference_code", th.StringType),
        th.Property("company_name", th.StringType),
        th.Property("warehouseId", th.IntegerType),
        th.Property("seller_gst", th.StringType),
        th.Property("forward_shipment_pickup_address", th.StringType),
        th.Property("forward_shipment_pickup_city", th.StringType),
        th.Property("forward_shipment_pickup_state", th.StringType),
        th.Property("forward_shipment_pickup_pin_code", th.StringType),
        th.Property("forward_shipment_pickup_country", th.StringType),
        th.Property("order_type", th.StringType),
        th.Property("order_type_key", th.StringType),
        th.Property("replacement_order", th.IntegerType),
        th.Property("marketplace", th.StringType),
        th.Property("marketplace_id", th.IntegerType),
        th.Property("salesmanUserId", th.IntegerType),
        th.Property("order_date", th.DateTimeType),
        th.Property("invoice_date", th.DateTimeType),
        th.Property("import_date", th.DateTimeType),
        th.Property("last_update_date", th.DateTimeType),
        th.Property("manifest_date", th.DateTimeType),
        th.Property("credit_note_date", th.DateTimeType),
        th.Property("return_date", th.DateTimeType),
        th.Property("manifest_no", th.StringType),
        th.Property("invoice_number", th.StringType),
        th.Property("credit_note_number", th.StringType),
        th.Property("marketplace_credit_note_num", th.StringType),
        th.Property("marketplace_invoice_num", th.StringType),
        th.Property("batch_id", th.NumberType),
        th.Property("batch_created_at", th.DateTimeType),
        th.Property("payment_mode", th.StringType),
        th.Property("payment_mode_id", th.IntegerType),
        th.Property("buyer_gst", th.StringType),
        th.Property("forward_shipment_customer_name", th.StringType),
        th.Property("forward_shipment_customer_contact_num", th.StringType),
        th.Property("forward_shipment_customer_address_line_1", th.StringType),
        th.Property("forward_shipment_customer_address_line_2", th.StringType),
        th.Property("forward_shipment_customer_city", th.StringType),
        th.Property("forward_shipment_customer_pin_code", th.StringType),
        th.Property("forward_shipment_customer_state", th.StringType),
        th.Property("forward_shipment_customer_country", th.StringType),
        th.Property("forward_shipment_customer_email", th.StringType),
        th.Property("forward_shipment_billing_name", th.StringType),
        th.Property("forward_shipment_billing_address_1", th.StringType),
        th.Property("forward_shipment_billing_address_2", th.StringType),
        th.Property("forward_shipment_billing_city", th.StringType),
        th.Property("forward_shipment_billing_state", th.StringType),
        th.Property("forward_shipment_billing_pin_code", th.StringType),
        th.Property("forward_shipment_billing_country", th.StringType),
        th.Property("forward_shipment_billing_mobile", th.StringType),
        th.Property("order_quantity", th.IntegerType),
        th.Property("total_invoice_amount", th.NumberType),
        th.Property("total_invoice_tax", th.NumberType),
        th.Property("invoice_collectable_amount", th.IntegerType),
        th.Property("items", th.CustomType({"type": ["array", "string"]})),
    ).to_dict()
