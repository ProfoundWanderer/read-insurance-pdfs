# standard imports
from collections import defaultdict
import csv
from datetime import datetime
from dateutil.parser import parse
import phonenumbers
import re
import sys
import util_funcs
# local imports


def gather_insurance_information(file_path):
    """
    Gathers insurance information and returns the dict with all the information

    - works for normal/standard acord pdf documents that aren't images
    - even if there are other documents in the pdf it will get the acord document and information
    - if two acord documents in one pdf then it was get the first one but if the second one is different then the info
        will be updated to the info in the next. Will keep happening until it gets to last acord document. Could try to
        handle this differently but this case is pretty rare so hard to test/see.
    - will not work on non acord insurance (e.g. progressive) or if it is a picture even if picture is in pdf
    - There are some scenarios it will not cover but hopefully this takes care of a 90% until it can be improved
    """

    # converts file to csv and checks if the csv file is empty
    new_file_path = util_funcs.convert_pdf_to_csv(file_path)

    # going ot use this to store information for later
    insurance_dict = defaultdict(dict)

    # column before auto and cargo information we need has one of these. Column is empty if the information is not there
    a = 'A', 'A\nA', 'B', 'B\nA', 'B\nC\nD', 'C', 'D\nE'
    col_1_set = set(a)

    with open(new_file_path, 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            for j, column in enumerate(row):
                # Get contact information
                if 'ODUCER\n' in column.upper():
                    result = re.search(r'(?<=\n).*(?=\n)', column)
                    if result is not None and result != '':
                        insu_name = result[0]
                        insurance_dict['contact_info']['producer'] = insu_name
                        print('Insurance name:', insu_name)  # Insurance producer name

                if 'CONTACT\nNAME:' in column.upper():
                    if column.split(":")[1].strip() is not None and column.split(":")[1].strip() != '':
                        cont_name = column.split(":")[1].strip()
                        insurance_dict['contact_info']['contact_name'] = cont_name
                        print('Contact name:', cont_name)  # Contact name

                if 'PHONE\n(A/C, NO, EXT):' in column.upper():
                    try:
                        phone_dirty = column.split(":")[1].strip()
                        if phone_dirty is not None and phone_dirty != '':
                            phone_parsed = phonenumbers.parse(phone_dirty, 'US')
                            phone_formatted = phonenumbers.format_number(phone_parsed, phonenumbers.PhoneNumberFormat.E164)
                            phone = str(phone_formatted).split('+1')[1]
                            insurance_dict['contact_info']['phone'] = phone
                            print('Insurance phone:', phone)
                    except phonenumbers.NumberParseException:
                        phone = column.split(":")[1].strip()
                        if 'description' not in insurance_dict['contact_info']:
                            insurance_dict['contact_info']['description'] = [phone]
                        else:
                            insurance_dict['contact_info']['description'].append(phone)
                        print('Couldn\'t make out phone so putting in description:', phone)

                if 'FAX\n(A/C, NO):' in column.upper():
                    try:
                        fax_dirty = column.split(":")[1].strip()
                        if fax_dirty is not None and fax_dirty != '':
                            fax_parsed = phonenumbers.parse(fax_dirty, 'US')
                            fax_formatted = phonenumbers.format_number(fax_parsed, phonenumbers.PhoneNumberFormat.E164)
                            fax = str(fax_formatted).split('+1')[1]
                            insurance_dict['contact_info']['fax'] = fax
                            print('Insurance fax:', fax)
                    except phonenumbers.NumberParseException:
                        fax = column.split(":")[1].strip()
                        if 'description' not in insurance_dict['contact_info']:
                            insurance_dict['contact_info']['description'] = [fax]
                        else:
                            insurance_dict['contact_info']['description'].append(fax)
                        print('Couldn\'t make out fax so putting in description:', fax)

                if 'E-MAIL\n' in column.upper():
                    pre_result = column.split('\n')[1].strip()
                    result = re.search(r'([\w0-9._-]+@[\w0-9._-]+\.[\w0-9_-]+)', pre_result)  # try to get the email
                    if result is not None and result != '':
                        insur_email = result[0]
                        insurance_dict['contact_info']['insurance_email'] = insur_email
                        print('Insurance email:', insur_email)  # email

                # Get auto insurance
                if 'AUTOMOBILE LIABILITY\n' in column.upper() and row[0].upper() in col_1_set:
                    print('--------------------------------------')
                    type_of_insur = column.split('\n')[0].strip()
                    print('Type of Insurance:', type_of_insur)

                    ind = 0
                    while ind < 20:
                        try:
                            parse(row[ind])

                            poli_num = row[ind - 1]
                            insurance_dict['automobile_liability']['policy_number'] = poli_num
                            print('Policy Number:', poli_num)

                            try:
                                eff_date = row[ind]
                                valid_eff_date = datetime.strptime(eff_date, '%m/%d/%Y').date()
                                insurance_dict['automobile_liability']['effective_date'] = eff_date
                                print('Effective Date:', eff_date)
                            except ValueError:
                                print('Effective Date: Invalid')
                                sys.exit()

                            try:
                                expi_date = row[ind + 1]
                                valid_exp_date = datetime.strptime(expi_date, '%m/%d/%Y').date()
                                util_funcs.date_check(valid_exp_date)
                                insurance_dict['automobile_liability']['expiration_date'] = expi_date
                                print('Expiration Date:', expi_date)
                            except ValueError:
                                print('Expiration Date: Invalid')
                                sys.exit()

                            coverage_amount_list = re.findall(r'[ 0-9]+', row[ind + 3])
                            if '00' in coverage_amount_list:  # ['1', '000', '000','00']
                                coverage_amount_list.remove('00')  # ['1', '000', '000']
                            coverage_amount = ''.join(coverage_amount_list)
                            insurance_dict['automobile_liability']['coverage_amount'] = coverage_amount
                            print('Coverage Amount:', coverage_amount)
                            break
                        except:  # dateutil.parser._parser.ParserError
                            ind += 1

                # Get cargo
                if 'CARGO' in column.upper() and row[0].upper() in col_1_set:
                    print('--------------------------------------')
                    type_of_insur = column.split('\n')[0].strip()
                    print('Type of Insurance:', type_of_insur)

                    ind = 0
                    while ind < 20:
                        try:
                            parse(row[ind].split('\n')[0].strip())

                            poli_num = row[ind - 1].split('\n')[0].strip()
                            insurance_dict['cargo']['policy_number'] = poli_num
                            print('Policy Number:', poli_num)

                            try:
                                eff_date = row[ind].split('\n')[0].strip()
                                valid_eff_date = datetime.strptime(eff_date, '%m/%d/%Y').date()
                                insurance_dict['cargo']['effective_date'] = eff_date
                                print('Effective Date:', eff_date)
                            except ValueError:
                                print('Effective Date: Invalid')
                                sys.exit()

                            try:
                                expi_date = row[ind + 1].split('\n')[0].strip()
                                valid_exp_date = datetime.strptime(expi_date, '%m/%d/%Y').date()
                                util_funcs.date_check(valid_exp_date)
                                insurance_dict['cargo']['expiration_date'] = expi_date
                                print('Expiration Date:', expi_date)
                            except ValueError:
                                print('Expiration Date: Invalid')
                                sys.exit()

                            if 'DED $' in row[7].upper() or 'LIMIT/DED' in row[7].upper() or 'DEDUCTIBLE\n' in row[7].upper():
                                if row[ind + 3].upper().count(',') >= 2:
                                    coverage_amount_list = row[ind + 3].split('\n')[0]
                                    coverage_amount_join = ''.join(coverage_amount_list)
                                    coverage_amount = re.sub('[^0-9]', '', coverage_amount_join)
                                    insurance_dict['cargo']['coverage_amount'] = coverage_amount
                                    print('Coverage Amount0:', coverage_amount)
                                else:
                                    coverage_amount_list = re.findall(r'[ 0-9]+', row[ind + 3])
                                    coverage_amount_join = ''.join(coverage_amount_list)
                                    coverage_amount = coverage_amount_join.split('  ')[0].strip()
                                    insurance_dict['cargo']['coverage_amount'] = coverage_amount
                                    print('Coverage Amount1:', coverage_amount)
                            else:
                                if row[ind + 2] == '' or 'Limit\n' in row[ind + 2]:
                                    coverage_amount_list = re.findall(r'[ 0-9]+', row[ind + 3].split('\n')[0].strip())
                                    coverage_amount_join = ''.join(coverage_amount_list)
                                    coverage_amount = coverage_amount_join.split('  ')[0].strip()
                                    insurance_dict['cargo']['coverage_amount'] = coverage_amount
                                    print('Coverage Amount2:', coverage_amount)
                                else:
                                    coverage_amount_list = re.findall(r'[ 0-9]+', row[ind + 2].split('\n')[0].strip())
                                    coverage_amount = ''.join(coverage_amount_list)
                                    if '  ' in coverage_amount:
                                        if coverage_amount.split('  ')[0].strip() == '':
                                            coverage_amount_f = coverage_amount.split('  ')[1].strip()
                                            insurance_dict['cargo']['coverage_amount'] = coverage_amount_f
                                            print('Coverage Amount3:', coverage_amount_f)
                                        else:
                                            coverage_amount_f = coverage_amount.split('  ')[0].strip()
                                            insurance_dict['cargo']['coverage_amount'] = coverage_amount_f
                                            print('Coverage Amount4:', coverage_amount_f)
                                    else:
                                        coverage_amount_f = coverage_amount.strip()
                                        if ' ' in coverage_amount_f.strip():
                                            ca_split = coverage_amount_f.split(' ')
                                            # changes numbers to int then back to a list
                                            ca_list_map = list(map(int, ca_split))
                                            coverage_amount_max = max(ca_list_map)  # get largest value
                                            insurance_dict['cargo']['coverage_amount'] = coverage_amount_max
                                            print('Coverage Amount5:', coverage_amount_max)
                                        else:
                                            insurance_dict['cargo']['coverage_amount'] = coverage_amount_f
                                            print('Coverage Amount6:', coverage_amount_f)
                            break
                        except:  # dateutil.parser._parser.ParserError
                            ind += 1

    # check dictonary to make sure it contains needed information
    try:
        insurance_dict['automobile_liability']['policy_number']
    except:
        print('Unable to find auto policy number.')

    try:
        insurance_dict['cargo']['policy_number']
    except:
        print('Unable to find cargo policy number.')

    try:
        insurance_dict['automobile_liability']['coverage_amount']
        if int(insurance_dict['automobile_liability']['coverage_amount']) < 1000000:
            print('Unable to find automobile liability coverage amount above $1,000,000.')
            sys.exit()
    except:
        print('Unable to find automobile liability coverage amount.')

    try:
        insurance_dict['cargo']['coverage_amount']
        if int(insurance_dict['cargo']['coverage_amount']) < 100000:
            print('Unable to find cargo coverage amount above $100,000.')
    except:
        print('Unable to find cargo coverage amount.')

    try:
        insurance_dict['automobile_liability']['effective_date']
        insurance_dict['automobile_liability']['expiration_date']
    except:
        print('Unable to find insurance effective date.')

    try:
        insurance_dict['cargo']['effective_date']
        insurance_dict['cargo']['expiration_date']
    except:
        print('Unable to find insurance expiration date.')

    return dict(insurance_dict)


if __name__ == '__main__':
    gather_insurance_information('/test-files/999.pdf')

