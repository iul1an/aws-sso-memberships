# AWS SSO Memberships

## Overview
This script prints information about AWS SSO groups memberships

## Usage
```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python sso_memberships.py
```

## Sample output
```
{
    "AWSControlTowerAdmins": [
        "michael.scott@dundermifflin.com
    ],
    "Sales": [
        "dwight.schrute@dundermifflin.com,
        "jim.halpert@dundermifflin.com
    ]
}
```
