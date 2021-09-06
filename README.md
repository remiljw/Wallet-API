# Wallet-API

API built with DRF for simple transactional wallets(NGN).

### NOTE
- Data used in this documentations are just samples of response you would get when you query the API accordingly.
- THEY ARE NOT REAL DATA.

### Authentication
- All end points need authentication to access except `/signin/` and `/signup/`.
- Get your token from the `/signin/` endpoint, after you have signed up and add it to the request headers.
```python
    Authorization : 'Bearer ' + jwt_token
```
- You are good to go. 👍🏾
## Endpoints
### https://wallets-apii.herokuapp.com/wallets/signup
- Anyone can access this endpoint, it is meant to register new users into the system. 
```json
   payload =  { 
      "email" : "test@test.com",
      "password" : "iamapatient"
       } 
```
```json
    response = {
        "email" : "test@test.com",
        "wallet" : "7546589570"
    }
 ```
 ### https://wallets-apii.herokuapp.com/wallets/signin
 - All users sign in here and get JWT tokens, which are used to access the remaining endpoints.
 ```json
  payload = {
                "email" : "test@test.com",
                "password" : "iamapatient"
               }
```
```json              
  response = {
                "email" : "test@test.com",
                "token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiOTdlODk5OTYtNzJlZC00ZTk4LTkxZmUtNTliMTRmYjMwNjk1IiwidXNlcm5hbWUiOiJtaWNhamFAZ21haWwuY29tIiwiZXhwIjoxNjE0NDU3NTE4LCJlbWFpbCI6Im1pY2FqYUBnbWFpbC5jb20ifQ.Kzb3TUIipqgyVKCE4Szs8GT_ldnaeOlNigufjNjNSaUn"
             }
 ```
 
 ### https://wallets-apii.herokuapp.com/wallets/fund-wallet
 - User can fund wallets from here, just by stating the amount. 
 -  Example: For 100, input `100`, for 10,000 input `10000`, for 100,000 input `100000`, for 10,500 input `10500`
 - Payment is processed by Flutterwave API, with a test card stored in the system to serve as the user's saved card. 
 - User is charged 3.8% of amount as transaction fee.
 - End point may take longer to respond as it needs to process payments.
 
 ```json
   payload = { 
       "amount" :  1000
    }
```
```json
    response = {
        "message" : "Wallet Funded", 
        "balance" : "1000.00"
    }
 ```
 
 ### https://wallets-apii.herokuapp.com/wallets/transfer
 -  User can transfer to other users in the system, just by specifying the user, the amount and detail.
 ```json
    payload = {
        "recipient": "test18@test.com",
        "amount": 100,
        "detail": "eat spaghetti"
    }
```
```json

    response = {
        "message": "Transfer successful",
        "balance": "900.00"
    }
 ```
 
 ### https://wallets-apii.herokuapp.com/wallets/transactions
 - Returns all wallet transacrtion of the user.
```json
    response = {
        "results": [
            {
            "id": 2,
            "sender": "7546589570",
            "recipient": "7598797786",
            "reference_number": "a9745f02-af70-4fdf-a46d-9ad8d8dc87f4",
            "trans_type": "debit",
            "amount": "100.00",
            "time": "2021-02-10T15:10:17.001086Z",
            "details": "eat spaghetti"
        },
        {
          "id": 9,
          "sender": "7546589570",
          "recipient": "7546589570",
          "reference_number": "7937333c-8810-4aab-9583-1854a9840c97",
          "trans_type": "fund_wallet",
          "amount": "1000.00",
          "time": "2021-09-06T16:35:48.931767Z",
          "details": "Fund Wallet"
        }
        ]
    }
```
## Miscellaneous

You can also interact with endpoints via the browser by clicking on the links, and login after you have signed up.
