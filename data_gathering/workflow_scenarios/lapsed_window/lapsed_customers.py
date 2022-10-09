from data_gathering.mock_salesforce_data.mock_data_to_db import *

from collections import defaultdict, namedtuple


class LapsedCustomers:
    def __init__(self, mocked_data_object: MockData):
        self.mocked_data_object = mocked_data_object
        self.address_sql_object = self.mocked_data_object.database_conn.create_tables_in_database(Address)
        self.account_sql_object = self.mocked_data_object.database_conn.create_tables_in_database(Account)
        self.contact_sql_object = self.mocked_data_object.database_conn.create_tables_in_database(Contact)
        self.product_cat_sql_object = self.mocked_data_object.database_conn.create_tables_in_database(ProductCategory)
        self.product_sql_object = self.mocked_data_object.database_conn.create_tables_in_database(Product2)
        self.order_sql_object = self.mocked_data_object.database_conn.create_tables_in_database(Order)
        self.order_item_sql_object = self.mocked_data_object.database_conn.create_tables_in_database(OrderItem)
        self.return_order_sql_object = self.mocked_data_object.database_conn.create_tables_in_database(ReturnOrder)

    def create_accounts(self, count_to_create) -> List[str]:
        "1000 stores/online/brick and motor"

        address_ids = []
        account_ids = []
        for x in range(0, 1000):
            address_type = random.choice(['In-Store-Address', 'Remote-Store-Address', 'LLC-Address'])
            address_output = self.mocked_data_object.fake_address(address_type, self.address_sql_object)

            address_ids.append(address_output.__dict__['id'])

        for account_to_create in range(0, count_to_create):
            account_output = self.mocked_data_object.fake_account(random.choice(address_ids), self.account_sql_object)
            account_ids.append(account_output.__dict__['id'])

        self.mocked_data_object.database_conn.db_session.commit()

        return account_ids

    def create_user_flow(self, count_to_create):

        contact_ids = []

        for contact_to_create in range(0, count_to_create):
            address_type = random.choice(['Home', 'Work', 'Business'])
            address_output = self.mocked_data_object.fake_address(address_type, self.address_sql_object)

            contact_output = self.mocked_data_object.fake_contact(address_id=address_output.__dict__['id'],
                                                                  ContactAlchemy=self.contact_sql_object)

            contact_ids.append((contact_output.__dict__['id'], contact_output.__dict__['address_id']))

        self.mocked_data_object.database_conn.db_session.commit()

        return contact_ids

    def create_products(self, count_to_create):

        product_category_count = defaultdict(int)
        product_ids = []
        for x in range(0, 23):
            product_category_output = self.mocked_data_object.fake_product_category(self.product_cat_sql_object)
            product_category_count[product_category_output.__dict__['id']] += product_category_output.__dict__[
                'number_of_products']

        for contact_to_create in range(0, count_to_create):
            random_stock_unit = random.randrange(1000, 1000000, 10000)
            random_cost = random.randrange(0, 1000, 25)

            random_quantity = random.randrange(1000, 1000000, 1000)

            random_quantity = random_quantity if random_quantity < random_stock_unit else random_stock_unit

            try:

                random_product_category = random.choice(list(product_category_count.keys()))

                if product_category_count[random_product_category] - random_stock_unit >= 0:

                    product_category_count[random_product_category] -= random_stock_unit
                    product_output = self.mocked_data_object.fake_product(product_category_id=random_product_category,
                                                                          quantity=random_quantity,
                                                                          cost=random_cost,
                                                                          stock_unit=random_stock_unit,
                                                                          ProductAlchemy=self.product_sql_object)

                    product_ids.append((product_output.__dict__['id'], product_output.__dict__['cost'],
                                        product_output.__dict__['stock_keeping_unit']))
                else:
                    product_category_count.pop(random_product_category)

            except:
                for x in range(0, 23):
                    product_category_output = self.mocked_data_object.fake_product_category(self.product_cat_sql_object)
                    product_category_count[product_category_output.__dict__['id']] += product_category_output.__dict__[
                        'number_of_products']

        self.mocked_data_object.database_conn.db_session.commit()

        return product_ids

    def create_order_item(self, product_count_and_cost, count_to_create, stock_unit_count,
                          order_items, iterator=0):

        products_per_order_random = random.choices(product_count_and_cost, k=random.randrange(1, 10))

        for product_to_order in products_per_order_random:
            if stock_unit_count[product_to_order.product_id] > 0:
                mocked_order_item = self.mocked_data_object.fake_order_item(product_id=product_to_order.product_id,
                                                                            quantity=product_to_order.product_quantity,
                                                                            ShipmentItemAlchemy=self.order_item_sql_object)

                stock_unit_count[product_to_order.product_id] -= product_to_order.product_quantity
                order_items.append(
                    (mocked_order_item.__dict__['id'],
                     product_to_order.product_quantity * product_to_order.product_cost))
            elif iterator < 20:
                iterator += 1
                self.create_order_item(product_count_and_cost, count_to_create,
                                       stock_unit_count=stock_unit_count,
                                       order_items=order_items, iterator=iterator)
        return order_items

    def single_multiple_order_flow(self, account_ids, contact_ids, product_ids, count_of_order_items_to_create,
                                   is_multiple=False, is_across_months=False):
        """

               * single order -- from one account *** DONE
               * multiple initial orders *** DONE
               * orders across a few months (random month) -- from specific account *** DONE
               * return orders *** DONE
               * multiple orders on holidays


               """

        stock_unit_count = defaultdict(int)
        order_outputs = []

        for contact_info in contact_ids:
            count_of_orders = random.randrange(1, 10) if is_multiple else 1
            contact_id, contact_address = contact_info[0], contact_info[1]

            ProductInfo = namedtuple("ProductInfo",
                                     "product_id product_cost product_stock_unit product_quantity stock_unit_percentage_to_use")

            for order_to_create in range(0, count_of_orders):
                product_count_and_cost = [
                    ProductInfo(product_id_tuple[0], product_id_tuple[1], product_id_tuple[2], random.randrange(1, 20),
                                (random.randrange(10, 100, 5)) / 100.0) for product_id_tuple in
                    product_ids]

                for product_to_order in product_count_and_cost:
                    stock_unit_count[product_to_order.product_id] = round(
                        product_to_order.product_stock_unit * product_to_order.stock_unit_percentage_to_use)

                order_items_output = self.create_order_item(product_count_and_cost=product_count_and_cost,
                                                            stock_unit_count=stock_unit_count,
                                                            order_items=[],
                                                            count_to_create=count_of_order_items_to_create)

                close_date = self.mocked_data_object.faker.date_between_dates(
                    date_start=datetime.datetime.now(),
                    date_end=datetime.datetime.now() + datetime.timedelta(
                        weeks=52)) if is_across_months else datetime.datetime.now()

                order_date = self.mocked_data_object.faker.date_between(
                    start_date="-1w",
                    end_date=close_date)

                order_output = self.mocked_data_object.fake_order(account_id=random.choice(account_ids),
                                                                  billing_location_id=contact_address,
                                                                  contact_id=contact_id,
                                                                  ordered_date=order_date,
                                                                  close_date=close_date,
                                                                  order_name=f'{self.mocked_data_object.faker.color_name()} Order',
                                                                  order_number=self.mocked_data_object.faker.iana_id(),
                                                                  status="approved",
                                                                  order_item_ids=[order_item[0] for order_item in
                                                                                  order_items_output],
                                                                  total_amount=sum(
                                                                      [order_item[1] for order_item in
                                                                       order_items_output]),
                                                                  total_tax_amount=(
                                                                          random.randrange(10, 30, 5) / 100.0),
                                                                  type="online",
                                                                  OrderAlchemy=self.order_sql_object)

                order_outputs.append((order_output.__dict__['id'],
                                      order_output.__dict__['account_id'],
                                      order_output.__dict__['bill_to_contact_id'],
                                      order_output.__dict__['billing_address_id'],
                                      order_output.__dict__['total_amount']
                                      ))

        self.mocked_data_object.database_conn.db_session.commit()

        return order_outputs

    def create_return_order(self, order_ids_to_return, count_of_order_to_return):
        order_ids_to_return_random = random.choices(order_ids_to_return, k=count_of_order_to_return)
        for random_return_order in order_ids_to_return_random:
            self.mocked_data_object.fake_return_order(
                order_id=random_return_order[0],
                account_id=random_return_order[1],
                contact_id=random_return_order[2],
                contact_shipping_id=random_return_order[3],
                status='approved',
                total_amount=random_return_order[4],
                expected_arrival_date=self.mocked_data_object.faker.date_between_dates(
                    date_start=datetime.datetime.now(),
                    date_end=datetime.datetime.now() + datetime.timedelta(
                        days=21)),
                ReturnOrderAlchemy=self.return_order_sql_object

            )
        self.mocked_data_object.database_conn.db_session.commit()
