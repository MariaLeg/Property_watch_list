import datetime
import csv

class Property:
    address: str
    comment: str
    price: int
    tenure: str
    agency: str
    date_added: datetime.date
    epc: str
    total_area: str
    useful_area: float
    link: str
    last_sold: str
    schools: str
    status: str

    def __init__(self):
        self.address = None
        self.comment = None
        self.price = None
        self.tenure = 'Unknown'
        self.agency = None
        self.date_added = None
        self.epc = 'Unknown'
        self.total_area = 'Unknown'
        self.useful_area = 0
        self.link = None
        self.last_sold = 'Unknown'
        self.schools = ''
        self.status = 'For sale'

    def write_property_to_file(self, csvfile):
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([self.status, self.address, self.tenure, self.comment, self.price, self.agency, self.date_added, self.epc, self.total_area, self.useful_area, self.link, self.last_sold, self.schools])
