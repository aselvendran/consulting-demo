from data_gathering.workflow_scenarios.lapsed_window.lapsed_customers import *
import os

if __name__ == '__main__':

    db_access = DatabaseAccess(os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD"), os.getenv("POSTGRES_HOST"),
                               os.getenv("POSTGRES_PORT"), os.getenv("POSTGRES_DB"))
    mocked_db = MockData(db_access, "lapsed_customers")

    lapsed_customers = LapsedCustomers(mocked_db)

    created_accounts = lapsed_customers.create_accounts(int(os.getenv("NUMBER_ACCOUNTS_TO_CREATE")))
    created_contacts = lapsed_customers.create_user_flow(int(os.getenv("NUMBER_CONTACTS_TO_CREATE")))

    created_products = lapsed_customers.create_products(int(os.getenv("NUMBER_PRODUCTS_TO_CREATE")))
    created_workflow = lapsed_customers.single_multiple_order_flow(account_ids=created_accounts,
                                                                   contact_ids=created_contacts,
                                                                   product_ids=created_products,
                                                                   count_of_order_items_to_create=int(os.getenv(
                                                                       "NUMBER_ORDER_ITEMS_TO_CREATE")),
                                                                   is_multiple=True, is_across_months=True)

    lapsed_customers.create_return_order(order_ids_to_return=created_workflow,
                                         count_of_order_to_return=int(os.getenv("NUMBER_OF_RETURN_ITEMS")))
