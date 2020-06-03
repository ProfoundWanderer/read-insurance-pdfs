# standard imports
from exchangelib import DELEGATE, Account, Credentials, FileAttachment
import os.path
# local imports
import config
from con_add import update_insurance
from read_ins import gather_insurance_information
from util_funcs import dir_cleanup


def get_pdf_and_dot_mc_from_email():
    credentials = Credentials(username=config.email, password=config.email_password)
    cs_account = Account(primary_smtp_address=config.email, credentials=credentials,
                         autodiscover=True, access_type=DELEGATE)

    ins_upd_folder = cs_account.root / 'Top of Information Store' / 'Inbox' / 'Insurance Updates - Completed'

    # Streaming downloads of attachments since this reduces memory consumption due to never
    # storing the full content of the file in-memory
    for item in cs_account.inbox.all():
        for attachment in item.attachments:
            if isinstance(attachment, FileAttachment):
                local_path = os.path.join('./test-files/tmp', attachment.name)
                if '.pdf' in attachment.name:
                    with open(local_path, 'wb') as f, attachment.fp as fp:
                        buffer = fp.read(1024)
                        while buffer:
                            f.write(buffer)
                            buffer = fp.read(1024)
                    print('Saved attachment to', local_path)

                    # handle DOT
                    if 'DOT# ' in item.subject.upper():
                        for subject_item in item.subject.upper().split('DOT# '):
                            if subject_item.strip().isdigit():
                                ins_dict = gather_insurance_information(local_path)
                                result = update_insurance('DOT', subject_item.strip(), ins_dict)

                                # item.reply_all(subject=f'{item.subject}', body='Insurance updated and the carrier has been set to true; MG will update in a few minutes.')

                                # clean up
                                dir_cleanup()
                                # item.move(ins_upd_folder)
                    elif 'DOT#' in item.subject.upper():
                        for subject_item in item.subject.upper().split('DOT#'):
                            if subject_item.strip().isdigit():
                                ins_dict = gather_insurance_information(local_path)
                                result = update_insurance('DOT', subject_item.strip(), ins_dict)
                                # item.reply_all(subject=f'{item.subject}', body='Insurance updated and the carrier has been set to true; MG will update in a few minutes.')

                                # clean up
                                dir_cleanup()
                                # item.move(ins_upd_folder)
                    elif 'DOT: ' in item.subject.upper():
                        for subject_item in item.subject.upper().split('DOT: '):
                            if subject_item.strip().isdigit():
                                ins_dict = gather_insurance_information(local_path)
                                result = update_insurance('DOT', subject_item.strip(), ins_dict)
                                # item.reply_all(subject=f'{item.subject}', body='Insurance updated and the carrier has been set to true; MG will update in a few minutes.')

                                # clean up
                                dir_cleanup()
                                # item.move(ins_upd_folder)
                    elif 'DOT:' in item.subject.upper():
                        for subject_item in item.subject.upper().split('DOT:'):
                            if subject_item.strip().isdigit():
                                ins_dict = gather_insurance_information(local_path)
                                result = update_insurance('DOT', subject_item.strip(), ins_dict)
                                # item.reply_all(subject=f'{item.subject}', body='Insurance updated and the carrier has been set to true; MG will update in a few minutes.')

                                # clean up
                                dir_cleanup()
                                # item.move(ins_upd_folder)
                    elif 'DOT ' in item.subject.upper():
                        for subject_item in item.subject.upper().split('DOT '):
                            if subject_item.strip().isdigit():
                                ins_dict = gather_insurance_information(local_path)
                                result = update_insurance('DOT', subject_item.strip(), ins_dict)
                                # item.reply_all(subject=f'{item.subject}', body='Insurance updated and the carrier has been set to true; MG will update in a few minutes.')

                                # clean up
                                dir_cleanup()
                                # item.move(ins_upd_folder)
                    elif 'DOT' in item.subject.upper():
                        for subject_item in item.subject.upper().split('DOT'):
                            if subject_item.strip().isdigit():
                                ins_dict = gather_insurance_information(local_path)
                                result = update_insurance('DOT', subject_item.strip(), ins_dict)
                                # item.reply_all(subject=f'{item.subject}', body='Insurance updated and the carrier has been set to true; MG will update in a few minutes.')

                                # clean up
                                dir_cleanup()
                                # item.move(ins_upd_folder)

                    # handle MC
                    if 'MC# ' in item.subject.upper():
                        for subject_item in item.subject.upper().split('MC# '):
                            if subject_item.strip().isdigit():
                                ins_dict = gather_insurance_information(local_path)
                                result = update_insurance('MC', subject_item.strip(), ins_dict)
                                # item.reply_all(subject=f'{item.subject}', body='Insurance updated and the carrier has been set to true; MG will update in a few minutes.')

                                # clean up
                                dir_cleanup()
                                # item.move(ins_upd_folder)
                    elif 'MC#' in item.subject.upper():
                        for subject_item in item.subject.upper().split('MC#'):
                            if subject_item.strip().isdigit():
                                ins_dict = gather_insurance_information(local_path)
                                result = update_insurance('MC', subject_item.strip(), ins_dict)
                                # item.reply_all(subject=f'{item.subject}', body='Insurance updated and the carrier has been set to true; MG will update in a few minutes.')

                                # clean up
                                dir_cleanup()
                                # item.move(ins_upd_folder)
                    elif 'MC: ' in item.subject.upper():
                        for subject_item in item.subject.upper().split('MC: '):
                            if subject_item.strip().isdigit():
                                ins_dict = gather_insurance_information(local_path)
                                result = update_insurance('MC', subject_item.strip(), ins_dict)
                                # item.reply_all(subject=f'{item.subject}', body='Insurance updated and the carrier has been set to true; MG will update in a few minutes.')

                                # clean up
                                dir_cleanup()
                                # item.move(ins_upd_folder)
                    elif 'MC:' in item.subject.upper():
                        for subject_item in item.subject.upper().split('MC:'):
                            if subject_item.strip().isdigit():
                                ins_dict = gather_insurance_information(local_path)
                                result = update_insurance('MC', subject_item.strip(), ins_dict)
                                # item.reply_all(subject=f'{item.subject}', body='Insurance updated and the carrier has been set to true; MG will update in a few minutes.')

                                # clean up
                                dir_cleanup()
                                # item.move(ins_upd_folder)
                    elif 'MC ' in item.subject.upper():
                        for subject_item in item.subject.upper().split('MC '):
                            if subject_item.strip().isdigit():
                                ins_dict = gather_insurance_information(local_path)
                                result = update_insurance('MC', subject_item.strip(), ins_dict)
                                # item.reply_all(subject=f'{item.subject}', body='Insurance updated and the carrier has been set to true; MG will update in a few minutes.')

                                # clean up
                                dir_cleanup()
                                # item.move(ins_upd_folder)
                    elif 'MC' in item.subject.upper():
                        for subject_item in item.subject.upper().split('MC'):
                            if subject_item.strip().isdigit():
                                ins_dict = gather_insurance_information(local_path)
                                result = update_insurance('MC', subject_item.strip(), ins_dict)
                                # item.reply_all(subject=f'{item.subject}', body='Insurance updated and the carrier has been set to true; MG will update in a few minutes.')

                                # clean up
                                dir_cleanup()
                                # item.move(ins_upd_folder)


if __name__ == '__main__':
    get_pdf_and_dot_mc_from_email()
