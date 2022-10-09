import random
from faker import Faker
from data_gathering.mock_salesforce_data.salesforce_object import *
from data_gathering.helper_postgres.access_db import *
import uuid


class MockData:
    def __init__(self, database_conn: DatabaseAccess, description):
        self.database_conn = database_conn
        self.description = description
        self.faker = Faker(locale='en_US')

    def fake_address(self, address_type, AddressAlchemy):
        street, city, state, zip = self.faker.street_address(), self.faker.city(), self.faker.state_abbr(), self.faker.postcode()

        data = AddressAlchemy(
            id=str(uuid.uuid4()),
            address=f'{street} \n{city}, {state} {zip}',
            address_type=address_type,
            city=city,
            country=self.faker.current_country_code(),
            description=self.description,
            geocode_accuracy=random.randint(1, 100),
            latitude=self.faker.latitude(),
            longitude=self.faker.longitude(),
            postal_code=zip,
            state=state,
            street=street,
            time_zone=random.choice(['US/Central', 'US/Eastern', 'US/Pacific', 'US/Hawaii'])
        )

        self.database_conn.commit(data)

        return data

    def fake_account(self, billing_address_id, AccountAlchemy):
        data = AccountAlchemy(
            id=str(uuid.uuid4()),
            account_number=self.faker.uuid4(),
            account_source=random.choice(['Brick and mortar', 'Online', 'Mall']),
            billing_address_id=billing_address_id,
            description=self.description,
            has_opted_out_of_email=random.choice([True, False]),
            industry=random.choice(['Clothing', 'Home Goods', 'Fashion', 'Wholesale']),
            is_deleted=False,
            is_person_account=False,
            updated_date=datetime.datetime.now(),
            last_referenced_date=datetime.datetime.now(),
            created_date=datetime.datetime.now(),
            naics_code=random.choice([str(x) for x in range(0, 100, 10)]),
            name=self.faker.bs(),
            number_of_employees=random.choice([str(x) for x in range(0, 10000, 100)]),
            phone=self.faker.phone_number(),
            rating=random.choice([str(x) for x in range(0, 5)]),
            shipping_address_id=billing_address_id,
            site='Headquarters',
            type='Client',
            website=self.faker.company_email(),
            year_started=self.faker.date_between_dates(date_start=datetime.datetime(1940, 1, 1),
                                                       date_end=datetime.datetime(2000, 1, 1))
        )

        self.database_conn.commit(data)

        return data

    def fake_contact(self, address_id, ContactAlchemy):
        first_name, last_name = self.faker.first_name(), self.faker.last_name()

        data = ContactAlchemy(
            id=str(uuid.uuid4()),
            birth_date=self.faker.date_between_dates(date_start=datetime.datetime(1940, 1, 1),
                                                     date_end=datetime.datetime(2000, 1, 1)),
            description=self.description,
            do_not_call=random.choice([True, False]),
            email=self.faker.email(),
            email_bounced_date=random.choice([True, False]),
            first_call_date_time=self.faker.date_between(start_date="-1y", end_date="now"),
            first_email_date_time=self.faker.date_between(start_date="-1y", end_date="now"),
            first_name=first_name,
            has_opted_out_of_email=random.choice([True, False]),
            home_phone=self.faker.phone_number(),
            is_email_bounced=random.choice([True, False]),
            last_name=last_name,
            created_date=datetime.datetime.now(),
            updated_date=datetime.datetime.now(),
            address_id=address_id,
            middle_name=self.faker.first_name(),
            mobile_phone=self.faker.phone_number(),
            name=f'{first_name} {last_name}',
            phone=self.faker.phone_number(),
            suffix=self.faker.suffix(),
            title=self.faker.prefix(),
        )
        self.database_conn.commit(data)

        return data

    def fake_product_category(self, ProductCategoryAlchemy):
        # product_label --- random.choice(['Suits', 'Pants', 'Ties', 'Cologne'])
        data = ProductCategoryAlchemy(
            id=str(uuid.uuid4()),
            currency_iso_code='USD',
            description=self.description,
            created_date=self.faker.date_between_dates(
                date_start=datetime.datetime.now() - datetime.timedelta(
                    days=60),
                date_end=datetime.datetime.now() - datetime.timedelta(
                    days=30)
            ),
            updated_date=self.faker.date_between_dates(
                date_start=datetime.datetime.now() - datetime.timedelta(
                    days=21),
                date_end=datetime.datetime.now()
            ),
            name=random.choice(['Suits', 'Pants', 'Ties', 'Cologne']),
            number_of_products=random.randrange(1000, 100000000, 100000)
        )

        self.database_conn.commit(data)

        return data

    def fake_product(self, product_category_id: str, quantity: int, cost: int, stock_unit: int, ProductAlchemy):
        # product_type
        # e-comm or in-store or third-party (amazon/shopify)
        data = ProductAlchemy(
            id=str(uuid.uuid4()),
            product_category_id=product_category_id,
            can_use_quantity_schedule=True,
            can_use_revenue_schedule=True,
            currency_iso_code='USD',
            description=self.description,
            product_class=random.choice(['e-commerce', 'in-store', 'third-party-amazon', 'third-party-shopify']),
            is_active=True,
            is_deleted=False,
            created_date=self.faker.date_between_dates(
                date_start=datetime.datetime.now() - datetime.timedelta(
                    days=60),
                date_end=datetime.datetime.now() - datetime.timedelta(
                    days=30)
            ),
            updated_date=self.faker.date_between_dates(
                date_start=datetime.datetime.now() - datetime.timedelta(
                    days=21),
                date_end=datetime.datetime.now()
            ),
            name=f'{self.faker.color_name()} product_type',
            number_of_quantity_installments=quantity,
            number_of_revenue_installments=quantity * cost,
            quantity_unit_of_measure='items via units',
            cost=cost,
            stock_keeping_unit=stock_unit
        )

        self.database_conn.commit(data)

        return data

    def fake_order(self, account_id, billing_location_id, contact_id, ordered_date, close_date, order_name,
                   order_number, status, total_amount, total_tax_amount, type, OrderAlchemy,
                   order_item_ids=List[str], original_order_id=None,
                   related_order_id=None):
        data = OrderAlchemy(
            id=str(uuid.uuid4()),
            account_id=account_id,
            billing_address_id=billing_location_id,
            bill_to_contact_id=contact_id,
            description=self.description,
            close_date=close_date,
            name=order_name,
            ordered_date=ordered_date,
            order_number=order_number,
            order_item_ids=order_item_ids,
            original_order_id=original_order_id,
            # RelatedOrderId is a subscriber.
            related_order_id=related_order_id,
            shipping_address_id=billing_location_id,
            status=status,
            total_amount=total_amount,
            total_tax_amount=total_tax_amount,
            type=type,
            currency_iso_code="USD"
        )

        self.database_conn.commit(data)

        return data

    def fake_order_item(self, product_id, quantity, ShipmentItemAlchemy):
        data = ShipmentItemAlchemy(
            id=str(uuid.uuid4()),
            product2_id=product_id,
            quantity=quantity,
            description=self.description
        )

        self.database_conn.commit(data)

        return data

    def fake_return_order(self, order_id, account_id, contact_id, contact_shipping_id,
                          status, total_amount, expected_arrival_date, ReturnOrderAlchemy):
        data = ReturnOrderAlchemy(
            id=str(uuid.uuid4()),
            account_id=account_id,
            contact_id=contact_id,
            description=self.description,
            destination_location_id=contact_shipping_id,
            expected_arrival_date=expected_arrival_date,
            order_id=order_id,
            shipment_type=random.choice(['express', 'standard', 'next-day']),
            status=status,
            total_amount=total_amount
        )

        self.database_conn.commit(data)

        return data

    def fake_shipment(self, delivered_to_id, account_id, ship_from_address_id,
                      ship_to_address_id, shipment_number, status, total_items_quantity,
                      ShipmentAlchemy, return_order_id=None):
        data = ShipmentAlchemy(
            id=str(uuid.uuid4()),
            actual_delivery_date=datetime.datetime.now(),
            delivered_to_id=delivered_to_id,
            delivery_method=random.choice(['home-sign-off', 'home-drop-off', 'store-pick-up']),
            description=self.description,
            expected_delivery_date=datetime.datetime.now() + datetime.timedelta(days=14),
            account_id=account_id,
            return_order_id=return_order_id,
            ship_from_address_id=ship_from_address_id,
            ship_to_address_id=ship_to_address_id,
            shipment_number=shipment_number,
            status=status,
            total_items_quantity=total_items_quantity,
            tracking_number=self.faker.iana_id(),
            tracking_url=self.faker.hostname(1),
            last_viewed_date=datetime.datetime.now()
        )

        self.database_conn.commit(data)

        return data
