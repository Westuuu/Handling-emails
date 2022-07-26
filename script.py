import collections
import os
import re
import itertools
import pandas as pd
import argparse
import pathlib


def read_files():
    lists_with_emails = []
    logs = []
    # Setting path to folder with emails
    try:
        __path__ = pathlib.Path(__file__).parent.resolve()
    except NameError:
        __path__ = pathlib.Path('.').resolve()
    
    path = __path__ / "emails"
    os.chdir(path)
    
    # Reading emails from .txt files
    def read_text_files(file_path):
        with open(file_path, "r") as f:
            data = f.read()
            data_into_list = data.split("\n")
        return data_into_list

    # Reading emails from .csv file
    def read_csv_files(file_path):
        data = pd.read_csv(file_path, delimiter=';')
        email_data = data.email
        list_of_emails_from_csv = list(email_data)
        return list_of_emails_from_csv

    # Reading emails from .logs file
    def read_logs(file_path):
        with open(file_path, 'r') as log_file:
            logs = log_file.read()
            log_emails = logs.split("'")[1::2]
        return log_emails
   
    # Looping for number of files in "emails" folder containing data and calling functions depending on the extension of the file
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = path / file
            lists_with_emails.append(read_text_files(file_path))
        elif file.endswith(".csv"):
            file_path = path / file
            lists_with_emails.append(read_csv_files(file_path))
        elif file.endswith(".logs"):
            file_path = path / file
            logs.append(read_logs(file_path))

    
    # Merging lists created from all files into one list
    emails = list(itertools.chain(*lists_with_emails))
    emails_from_logs = list(itertools.chain(*logs))
    return emails, emails_from_logs


# Excluding duplicates        
def without_duplicates():
    emails_with_duplicates = read_files()[0]
    emails_without_duplicates = list(set(emails_with_duplicates)) 
    return emails_without_duplicates


# Validating whether an email is correct or not             
def validate_emails():
    # Creating lists to store all emails
    valid_emails = []
    invalid_emails = []
    all_emails = read_files()[0]

    # Creating lists to store unique emails without duplicates
    unique_emails = without_duplicates()
    unique_valid_emails = []
    unique_invalid_emails = []

    pat = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z0-9|a-z0-9]{1,4})+')

    # Looping over all emails and dividing them into correct and incorrect 
    for email in all_emails:
        if re.fullmatch(pat, email):
            valid_emails.append(email)
        else:
            invalid_emails.append(email)

    # Looping over unique emails and dividing them into correct and incorrect
    for email in unique_emails:
        if re.fullmatch(pat, email):
            unique_valid_emails.append(email)
        else:
            unique_invalid_emails.append(email)
    return valid_emails, invalid_emails, unique_valid_emails, unique_invalid_emails


# This function allows to search emails that contain a certain phrase given by the user
def search_by():
    search = input("Type a word you would like to search for: ")
    matches = [match for match in validate_emails()[2] if search in match]
    print(f"Found emails with '{search}' in email ({len(matches)}):")
    print(*matches, sep='\n')

# Grouping emails by their domain and printing all emails with the same domain
def group_domains():

    ungrouped_emails = validate_emails()[2]
    email_addresses_by_domain = collections.defaultdict(list)
    
    def extract_domain(email_address):
        name, domain = email_address.split("@")
        return domain

    for email in ungrouped_emails:
        domain = extract_domain(email)
        email_addresses_by_domain[domain].append(email)

    for mails in email_addresses_by_domain.values():
        mails.sort()

    for domain, addresses in sorted(email_addresses_by_domain.items()):
        print(f"Domain {domain} ({len(addresses)}):")
        for a in addresses:
            print("      ", a)

# Function checks which emails are not present in logs
def compare_emails():
    emails = validate_emails()[2]
    emails_from_logs = read_files()[1]

    emails_not_sent = []
    for email in emails:
        if email not in emails_from_logs:
            emails_not_sent.append(email)
    
    
    print(f"Emails not sent ({len(emails_not_sent)}):")
    for email in sorted(emails_not_sent):
        print(email)
    
# Commands to run to get answers to tasks untill interface is done:
# Task number 1:
def task_1():
    invalid_emails = validate_emails()[1]
    print('Invalid emails (' + str(len(invalid_emails)) + ')', *invalid_emails, sep='\n')

# task_1()

# Task number 2:
# search_by()

# Task number 3:
# group_domains()

# Task number 4:
# compare_emails()


#####



# Everything below needs to be finished, all the functions are working but interface is not ready yet


#start = input("Please, choose what do you want to see, possible commands: \n--incorrect-emails (-ic)\n\
#--search-str (-s str)\n--group-by-domain (-gbd)\n--find-emails-not-in-logs path_to_logs_file (-feil path_to_logs_file)\n\n")

#def ic():
#    if start == "--incorrect-emails" or start == '-ic':
#        ic = validate_emails()[1]
#        print("\n")
#        for email in ic:
#            print(email)


# def Main():
#     #os.chdir()
#     parser = argparse.ArgumentParser(description="Choose your action")
#     parser.add_argument("-ic", "--incorrect-emails", help = "Shows incorrect emails")

#     args = parser.parse_args()

#     if args.incorrect_emails:
#         print(validate_emails()[1])

# if __name__ == "__main__":
#     Main()






