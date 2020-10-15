import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit, QMainWindow, QListWidget, QMessageBox

from db_conn import SqlServer
from style import global_style
import time
import json


class POS(QMainWindow):

    """ Main Application window.
    """

    def __init__(self):
        super(POS, self).__init__()
        uic.loadUi('main_window.ui', self)

        self.setStyleSheet(global_style())

        self.show()

        # Default total amount.
        self.receipt_total = 0
        self.items = []


        # Input Fields
        self.item_input = self.findChild(QLineEdit, 'BarcodeInput')
        self.customer_input = self.findChild(QLineEdit, 'CustomerLookup')

        # Input Buttons
        self.item_button = self.findChild(QPushButton, 'AddToReceipt')
        self.customer_button = self.findChild(QPushButton, 'AddCustomer')
        self.pay = self.findChild(QPushButton, 'PayButton')

        # Data Fields and messagebox
        self.receipt = self.findChild(QListWidget, 'Receipt')
        self.customer = self.findChild(QListWidget, 'Customer')
        self.total = self.findChild(QListWidget, 'Total')
        self.msg = QMessageBox()

        # Add items to receipt when button is clicked.
        self.item_button.clicked.connect(self.get_price)

        # Add Customer to the receipt when button is clicked.
        self.customer_button.clicked.connect(self.get_customer)

        # Finish and pay the receipt when pay button is clicked.
        self.pay.clicked.connect(self.pay_receipt)


    def get_price(self):

        """ Retrieve price from database and add to total amount.
        """

        with SqlServer() as cursor:

            item = self.item_input.text()

            retrieve_price = 'Select Price from dbo.article_Price where PLU in (Select PLU from dbo.article where PLU = ?)'

            cursor.execute(retrieve_price, item)

            article = cursor.fetchone()

            if article is None:
                self.msg.setText('Article does not have a price.')
                self.msg.exec_()
            else:
                result = str(article[0])
                self.receipt.addItem(self.get_description(item) + '  ' + '€' + result)
                self.items.append(self.get_description(item) + '  ' + '€' + result)

                self.receipt_total += int(result)
                self.total.clear()
                self.total.addItem(str(self.receipt_total))
                self.item_input.clear()


    def get_description(self, item_to_fetch):

        """ Retrieve description from database to show on receipt.
        """

        with SqlServer() as cursor:

            retrieve_descr = 'Select Description from dbo.article where PLU = ?'

            cursor.execute(retrieve_descr, item_to_fetch)

            description = cursor.fetchone()

            if description is None:
                self.msg.setText('Article does not exist or does not a have a description.')
                self.msg.exec_()
            else:
                item_description = str(description[0])
                return item_description


    def get_customer(self):

        """ Lookup customer in the database and add it to the receipt.
        """

        with SqlServer() as cursor:

            customer_lookup = self.customer_input.text()

            retrieve_customer = 'Select Name from dbo.Customer where LoyaltyCard = ?'
            cursor.execute(retrieve_customer, customer_lookup)

            result = cursor.fetchone()

            if result is None:
                self.msg.setText('Loyalty card does not exist.')
                self.msg.exec_()
            else:
                customer = str(result[0])
                self.customer.addItem(customer)
                self.customer_input.clear()


    def save_to_db(self, customer, ticket_total):

        """ Save the receipt in the database.
        """

        if customer.count() != 0:
            for i in range(customer.count()):
                customer_on_receipt = customer.item(i) # returns a QListWidgetItem

            with SqlServer() as cursor:

                query = 'INSERT INTO dbo.Ticket (Customer, TotalAmount) VALUES (?, ?)'
                cursor.execute(query, customer_on_receipt.text(), ticket_total)
        else:
            with SqlServer() as cursor:

                query = 'INSERT INTO dbo.Ticket (Customer, TotalAmount) VALUES (?, ?)'
                cursor.execute(query, 'None', ticket_total)


    def pay_receipt(self):

        """Pay and Finish the receipt.
        """

        self.print_receipt()

    def json_dump(self, items: list, customer: str, total: int):


        timestr = time.strftime("%Y%m%d-%H%M%S")
        backup_dir = f'C:\\Users\\louis\\Documents\\Receipt_Backup\\Receipt_{timestr}.json'

        json_file = open(backup_dir, 'w+')

        json.dump((items, customer, total), json_file)
        json_file.close()


    def print_receipt(self):

        """ Print the receipt after it has been paid.
        """

        self.save_to_db(self.customer, self.receipt_total)
        self.json_dump(self.items, str(self.customer), self.receipt_total)

        self.receipt_total = 0
        self.total.clear()
        self.receipt.clear()
        self.customer.clear()

        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText('Receipt is finished!')
        self.msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = POS()
    sys.exit(app.exec_())
