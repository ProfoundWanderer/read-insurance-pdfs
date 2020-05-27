import csv
from dateutil.parser import parse
import re
import tabula


# convert pdf into csv so we can get information from it
tabula.convert_into('/test-files/2.pdf', '/test-files/2.csv', output_format='csv', pages='all', lattice=True, guess=True)


with open('/test-files/4.csv', 'r') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        for j, column in enumerate(row):
            # Get contact information
            if 'ODUCER\n' in column.upper():
                result = re.search(r'(?<=\n).*(?=\n)', column)
                print('Insurance name:', result[0])  # Insurance producer name
            if 'PHONE\n(A/C, NO, EXT):' in column.upper():
                print('Insurance phone:', column.split(":")[1].strip())  # phone number
            if 'FAX\n(A/C, NO):' in column.upper():
                print('Insurance fax:', column.split(":")[1].strip())  # fax number
            if 'E-MAIL\n' in column.upper():
                pre_result = column.split('\n')[1].strip()
                result = re.search(r'([\w0-9._-]+@[\w0-9._-]+\.[\w0-9_-]+)', pre_result)  # try to get the email
                print('Insurance email:', result[0])  # email

            # Get auto insurance
            if 'AUTOMOBILE LIABILITY\n' in column.upper() and 'A' == row[0].upper():
                print('--------------------------------------')
                print('Type of Insurance:', column.split('\n')[0].strip())

                ind = 0
                while ind < 20:
                    try:
                        parse(row[ind])
                        print('Policy Number:', row[ind - 1])
                        print('Effective Date:', row[ind])
                        print('Expiration Date:', row[ind + 1])
                        coverage_amount_list = re.findall(r'[ 0-9]+', row[ind + 3])
                        coverage_amount = ''.join(coverage_amount_list)
                        print('Coverage Amount:', coverage_amount)
                        break
                    except:  # dateutil.parser._parser.ParserError
                        ind += 1

            # Get cargo
            if 'CARGO' in column.upper() and ('A' == row[0].upper() or 'A\nA' == row[0].upper() or 'B' == row[0].upper()):
                print('--------------------------------------')
                print('Type of Insurance:', column.split('\n')[0].strip())

                ind = 0
                while ind < 20:
                    try:
                        parse(row[ind].split('\n')[0].strip())
                        print('Policy Number:', row[ind - 1].split('\n')[0].strip())
                        print('Effective Date:', row[ind].split('\n')[0].strip())
                        print('Expiration Date:', row[ind + 1].split('\n')[0].strip())
                        if 'DED $' in row[7].upper():
                            coverage_amount_list = re.findall(r'[ 0-9]+', row[ind + 3])
                            coverage_amount = ''.join(coverage_amount_list)
                            print('Coverage Amount:', coverage_amount.split('  ')[0].strip())
                        else:
                            coverage_amount_list = re.findall(r'[ 0-9]+', row[ind + 2].split('\n')[0].strip())
                            coverage_amount = ''.join(coverage_amount_list)
                            print('Coverage Amount:', coverage_amount.split('  ')[0].strip())
                        break
                    except:  # dateutil.parser._parser.ParserError
                        ind += 1

