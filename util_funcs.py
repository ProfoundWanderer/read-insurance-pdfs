from datetime import datetime
import glob
import os
import sys
import tabula


def convert_pdf_to_csv(file_path):
    """
    Convert pdf into csv so we can get information from it
    This appears to be the best way to get progressive insurance file information into CSV

    tabula.convert_into(
        '/test-files/pogressive-test.pdf',
        '/test-files/pogressive-test.csv',
        output_format='csv',
        pages='all',
        lattice=False,
        guess=False,
    )
    """

    file_path_base = os.path.splitext(file_path)[0]  # /test-files/9
    new_file_path = f'{file_path_base}.csv'  # /test-files/9.csv

    tabula.convert_into(
        file_path,
        new_file_path,
        output_format='csv',
        pages='all',
        lattice=True,
        guess=True,
    )

    # If file is empty then convert did not work likely due to the pdf being an image or
    # none "standard" insurance format
    try:
        if os.stat(new_file_path).st_size == 0:
            print('File empty')
            sys.exit()
    except FileNotFoundError:
        print('CSV file not found, please make sure it was created.')
        sys.exit()

    return new_file_path


def date_check(input_date):
    """
    Used to make sure insurance is not expired
    """
    today = datetime.now().date()
    if input_date <= today:
        print('This insurance appears to be expired.')
        sys.exit()


def dir_cleanup():
    for f in glob.glob('./test-files/tmp/.*'):
        os.remove(f)
