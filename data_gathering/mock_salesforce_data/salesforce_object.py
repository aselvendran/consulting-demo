import datetime
from sqlalchemy import Integer, String, DateTime, Boolean, BigInteger, DECIMAL
import dataclasses
from sqlalchemy.dialects.postgresql import ARRAY
from dataclasses import dataclass
from typing import List


def sqlalchemy_datatype(sqlalchemy_type) -> dataclasses.field:
    return dataclasses.field(
        metadata={
            "sqlalchemy_type": sqlalchemy_type
        }
    )


@dataclass
class Address:
    address: str = sqlalchemy_datatype(String)
    address_type: str = sqlalchemy_datatype(String)
    city: str = sqlalchemy_datatype(String)
    country: str = sqlalchemy_datatype(String)
    description: str = sqlalchemy_datatype(String)
    geocode_accuracy: int = sqlalchemy_datatype(Integer)
    latitude: str = sqlalchemy_datatype(String)
    longitude: str = sqlalchemy_datatype(String)
    postal_code: str = sqlalchemy_datatype(String)
    state: str = sqlalchemy_datatype(String)
    street: str = sqlalchemy_datatype(String)
    time_zone: str = sqlalchemy_datatype(String)


@dataclass
class Shipment:
    actual_delivery_date: datetime.datetime = sqlalchemy_datatype(DateTime)
    delivered_to_id: str = sqlalchemy_datatype(String)
    delivery_method: str = sqlalchemy_datatype(String)
    description: str = sqlalchemy_datatype(String)
    expected_delivery_date: datetime.datetime = sqlalchemy_datatype(DateTime)
    account_id: str = sqlalchemy_datatype(String)
    return_order_id: str = sqlalchemy_datatype(String)
    ship_from_address_id: str = sqlalchemy_datatype(String)
    ship_to_address_id: str = sqlalchemy_datatype(String)
    # number of times the shipment was delivered max is 5.
    shipment_number: str = sqlalchemy_datatype(String)
    status: str = sqlalchemy_datatype(String)
    total_items_quantity: int = sqlalchemy_datatype(Integer)
    tracking_number: str = sqlalchemy_datatype(String)
    tracking_url: str = sqlalchemy_datatype(String)
    last_viewed_date: datetime.datetime = sqlalchemy_datatype(DateTime)


@dataclass
class Order:
    account_id: str = sqlalchemy_datatype(String)
    billing_address_id: str = sqlalchemy_datatype(String)
    bill_to_contact_id: str = sqlalchemy_datatype(String)
    description: str = sqlalchemy_datatype(String)
    close_date: str = sqlalchemy_datatype(String)
    name: str = sqlalchemy_datatype(String)
    ordered_date: datetime.datetime = sqlalchemy_datatype(DateTime)
    order_number: str = sqlalchemy_datatype(String)
    order_item_ids: List[str] = sqlalchemy_datatype(ARRAY(String))
    original_order_id: str = sqlalchemy_datatype(String)
    related_order_id: str = sqlalchemy_datatype(String)
    shipping_address_id: str = sqlalchemy_datatype(String)
    status: str = sqlalchemy_datatype(String)
    total_amount: int = sqlalchemy_datatype(Integer)
    total_tax_amount: int = sqlalchemy_datatype(DECIMAL)
    type: str = sqlalchemy_datatype(String)
    currency_iso_code: str = sqlalchemy_datatype(String)


@dataclass
class OrderItem:
    product2_id: str = sqlalchemy_datatype(String)
    quantity: int = sqlalchemy_datatype(Integer)
    description: str = sqlalchemy_datatype(String)


@dataclass
class ReturnOrder:
    account_id: str = sqlalchemy_datatype(String)
    contact_id: str = sqlalchemy_datatype(String)
    description: str = sqlalchemy_datatype(String)
    destination_location_id: str = sqlalchemy_datatype(String)
    expected_arrival_date: datetime.datetime = sqlalchemy_datatype(DateTime)
    order_id: str = sqlalchemy_datatype(String)
    shipment_type: str = sqlalchemy_datatype(String)
    status: str = sqlalchemy_datatype(String)
    total_amount: int = sqlalchemy_datatype(Integer)


@dataclass
class Product2:
    can_use_quantity_schedule: bool = sqlalchemy_datatype(Boolean)
    can_use_revenue_schedule: bool = sqlalchemy_datatype(Boolean)
    currency_iso_code: str = sqlalchemy_datatype(String)
    description: str = sqlalchemy_datatype(String)
    product_class: str = sqlalchemy_datatype(String)
    is_active: bool = sqlalchemy_datatype(Boolean)
    is_deleted: bool = sqlalchemy_datatype(Boolean)
    created_date: datetime.datetime = sqlalchemy_datatype(DateTime)
    updated_date: datetime.datetime = sqlalchemy_datatype(DateTime)
    name: str = sqlalchemy_datatype(String)
    product_category_id: str = sqlalchemy_datatype(String)
    number_of_quantity_installments: int = sqlalchemy_datatype(BigInteger)
    number_of_revenue_installments: int = sqlalchemy_datatype(BigInteger)
    quantity_unit_of_measure: str = sqlalchemy_datatype(String)
    cost: int = sqlalchemy_datatype(BigInteger)
    stock_keeping_unit: int = sqlalchemy_datatype(BigInteger)


@dataclass
class ProductCategory:
    currency_iso_code: str = sqlalchemy_datatype(String)
    description: str = sqlalchemy_datatype(String)
    created_date: str = sqlalchemy_datatype(String)
    updated_date: str = sqlalchemy_datatype(String)
    name: str = sqlalchemy_datatype(String)
    number_of_products: int = sqlalchemy_datatype(Integer)


@dataclass
class Account:
    account_number: str = sqlalchemy_datatype(String)
    account_source: str = sqlalchemy_datatype(String)
    billing_address_id: str = sqlalchemy_datatype(String)
    description: str = sqlalchemy_datatype(String)
    has_opted_out_of_email: bool = sqlalchemy_datatype(Boolean)
    industry: str = sqlalchemy_datatype(String)
    is_deleted: bool = sqlalchemy_datatype(Boolean)
    is_person_account: bool = sqlalchemy_datatype(Boolean)
    updated_date: datetime.datetime = sqlalchemy_datatype(DateTime)
    last_referenced_date: datetime.datetime = sqlalchemy_datatype(DateTime)
    created_date: datetime.datetime = sqlalchemy_datatype(DateTime)
    naics_code: str = sqlalchemy_datatype(String)
    name: str = sqlalchemy_datatype(String)
    number_of_employees: str = sqlalchemy_datatype(String)
    phone: str = sqlalchemy_datatype(String)
    rating: str = sqlalchemy_datatype(String)
    site: str = sqlalchemy_datatype(String)
    shipping_address_id: str = sqlalchemy_datatype(String)
    type: str = sqlalchemy_datatype(String)
    website: str = sqlalchemy_datatype(String)
    year_started: str = sqlalchemy_datatype(String)


@dataclass
class Contact:
    birth_date: str = sqlalchemy_datatype(String)
    description: str = sqlalchemy_datatype(String)
    do_not_call: bool = sqlalchemy_datatype(Boolean)
    email: str = sqlalchemy_datatype(String)
    email_bounced_date: bool = sqlalchemy_datatype(Boolean)
    first_call_date_time: str = sqlalchemy_datatype(String)
    first_email_date_time: str = sqlalchemy_datatype(String)
    first_name: str = sqlalchemy_datatype(String)
    has_opted_out_of_email: bool = sqlalchemy_datatype(Boolean)
    home_phone: str = sqlalchemy_datatype(String)
    is_email_bounced: bool = sqlalchemy_datatype(Boolean)
    last_name: str = sqlalchemy_datatype(String)
    created_date: datetime.datetime = sqlalchemy_datatype(DateTime)
    updated_date: datetime.datetime = sqlalchemy_datatype(DateTime)
    address_id: str = sqlalchemy_datatype(String)
    middle_name: str = sqlalchemy_datatype(String)
    mobile_phone: str = sqlalchemy_datatype(String)
    name: str = sqlalchemy_datatype(String)
    phone: str = sqlalchemy_datatype(String)
    suffix: str = sqlalchemy_datatype(String)
    title: str = sqlalchemy_datatype(String)
