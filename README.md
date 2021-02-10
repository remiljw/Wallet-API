# Wallet-API

API built with DRF for a telemedicine app to book hospital appointments.

## Authentication
- All end points need authentication to access except `/signin/` and `/signup/`.
- Get your token from the `/signin/` endpoint, after you have signed up and add it to the request headers.
```python
    Authorization : 'Bearer ' + jwt_token
```
- You are good to go. 👍🏾
## Endpoints

### https://wallets-apii.herokuapp.com/api/signup/
- Anyone can access this endpoint, it is meant to register new users into the system. 
```json
   payload =  { 
      "email" : "test@test.com" ,
      "password" : "iamapatient",
       } 

    response = {
        "email" : "test@test.com" ,
        "wallet" : "7598797786",
    }
 ```
 ### https://wallets-apii.herokuapp.com/api/signin/
 - All users sign in here and get JWT tokens, which are used to access the remaining endpoints.
 ```json
  payload = {
                "email" : "test@test.com",
                "password" : "iamapatient"
               }
  response = {
                "email" : "test@test.com",
                "token" : "jwt_token"
             }
 ```
 
 ### https://wallets-apii.herokuapp.com/api/fund-wallet/
 - User can fund wallets from here, just by stating the amount. 
 -  Example: For N100, type 100 
 -  For N100.50, type 100.50
 ```json
   payload = { 
       "amount" :  10000
    }

    response = {
        "message" : "Wallet Funded", 
        "balance" : 10000.00
    }
 ```
 
 ### https://wallets-apii.herokuapp.com/api/transfer/
 -  User can transfer to other users in the system, just by specifying the user, the amount and detail.
 ```json
    payload = {
        "receiver": "test18@test.com",
        "amount": 100,
        "detail": "eat spaghetti"
    }

    response = {
        "message": "Transfer successful",
        "balance": "900.00"
    }
 ```
 
 ### https://telemed-api.herokuapp.com/api/transactions/
 - Returns all wallet transacrtion of the user.
```json
    response = {
        "results": [
            {
            "id": 2,
            "source": "7598797786",
            "reference_number": "a9745f02-af70-4fdf-a46d-9ad8d8dc87f4",
            "trans_type": "debit",
            "amount": "100.00",
            "time": "2021-02-10T15:10:17.001086Z",
            "receiver_or_sender": "test18@test.com",
            "details": "eat spaghetti"
        },
        {
            "id": 1,
            "source": "7598797786",
            "reference_number": "4c18b277-9c8b-4747-a142-449cd9f1e3ea",
            "trans_type": "fund_wallet",
            "amount": "10000.00",
            "time": "2021-02-10T15:11:46.926753Z",
            "receiver_or_sender": "test@test.com",
            "details": "Fund Wallet"
        }
        ]
    }
```
## Miscellaneous

You can also test via the browsable apis by clicking on the links, and login where necessary.