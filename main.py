import os
import sys
import mailchimp_marketing as Mailchimp
from mailchimp_marketing.api_client import ApiClientError

mailchimp_list_id = os.environ.get('MAILCHIMP_LIST_ID')
mailchimp_token = os.environ.get('MAILCHIMP_TOKEN')
mailchimp_segment_id = os.environ.get('MAILCHIMP_SEGMENT_ID')
mailchimp_server_prefix = os.environ.get('MAILCHIMP_SERVER_PREFIX')

if not mailchimp_list_id or not mailchimp_token or not mailchimp_segment_id or not mailchimp_server_prefix:
    print('Missing environment variable(s). Requires MAILCHIMP_LIST_ID, MAILCHIMP_TOKEN, MAILCHIMP_SEGMENT_ID, MAILCHIMP_SERVER_PREFIX')
    sys.exit(1)

try:
    mailchimp = Mailchimp.Client()
    mailchimp.set_config({
        "api_key": mailchimp_token,
        "server": mailchimp_server_prefix
    })

    response = mailchimp.lists.get_segment_members_list(mailchimp_list_id, mailchimp_segment_id, count=1000, include_unsubscribed=True)
    if not response or 'members' not in response:
        print(f'No member data returned for list {mailchimp_list_id} and segment {mailchimp_segment_id}')
        sys.exit(1)
except ApiClientError as error:
    print("Error: {0}".format(error.text))

try:
    members = response['members']

    donors = [member['merge_fields'] for member in members]
    donor_list = [{
        'name': member.get('DONORNAME', f"{member.get('FNAME', '')} {member.get('LNAME', '')}"),
        'level': member.get('DONORLEVEL', ''),
        'lastname': member.get('LNAME', '')
    } for member in donors]

    # remove duplicates
    donor_list = [dict(t) for t in {tuple(d.items()) for d in donor_list}]

    # sort by lastname
    donor_list = sorted(donor_list, key=lambda x: x.get('lastname', ''))

    # group donors by level
    # these strings must match what Mailchimp returns in DONORLEVEL field
    donor_levels = ['Patrons', 'Artists Circle', 'Sustainers', 'Friends', 'Benefactors', 'Composers Society']
    filenames = ['patrons.yml', 'artistscircle.yml', 'sustainers.yml', 'friends.yml', 'benefactors.yml', 'composerssociety.yml']
    datapath = '_data/benefactors/'
    grouped_donors = {level: [] for level in donor_levels}

    for donor in donor_list:
        level = donor.get('level')
        if level in grouped_donors:
            grouped_donors[level].append(donor)

    # write to files
    for i, level in enumerate(donor_levels):
        try:
            os.makedirs(datapath, exist_ok=True)
            filepath = os.path.join(datapath, filenames[i])
        
            with open(filepath, 'w') as f:
                for donor in grouped_donors[level]:
                    f.write(f'- name: {donor.get("name")}\n')
        except Exception as e:
            print(f'Error writing to file: {e}')
            
except Exception as e:
    print(f"Error: {e}")