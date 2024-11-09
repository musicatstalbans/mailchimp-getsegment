# mailchimp-getsegment
Retrieves an audience segment from MailChimp

## Merge Fields
In Mailchimp, custom merge fields were defined for listing donor names on website. The merge fields are defined as follows:
- `FNAME` - First Name
- `LNAME` - Last Name
- `FULLNAME` - Full Name
- `DONORLEVEL` - Donor Level

The FULLNAME is used when the donor requests a specific name to be displayed on the website. If the FULLNAME is not provided, the FIRSTNAME and LASTNAME are used.

## GitHub Actions Configuration

GitHub Actions secrets are required for the following:

- `MAILCHIMP_TOKEN`
- `MAILCHIMP_SERVER_PREFIX`
- `MAILCHIMP_LIST_ID`
- `MAILCHIMP_SEGMENT_ID`

## Output

This action outputs a YML file for each donor level. The path is hard-coded to `_data/benefactors/`.

Format is simply:

```yml
- John Doe
- Issac Newton
- Keanu Reeves
```

## Notes

This will read up to 1,000 donors from the segment. If there are more than 1,000 donors, the action will need to be updated to handle pagination.

People who have unsubscribed from the list will be included in the results. This resulted in duplication of some names, so a de-duplication process is also included in the action.