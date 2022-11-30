# API endpoints

## GET
[/user/<:username>/](#u-get-userusername-u) <br/>
[/transactions/?username](#u-get-transactionsusername-u) `WIP` <br/>

## POST
[/sign-up](#u-post-sign-up-u) <br/>
[/login](#u-post-login-u) <br/>
[/transactions/create](#u-post-transactionscreate-u) <br/>
[/transactions/trade](#u-post-transactionstrade-u)<br/>
[/transactions/untrade](#u-post-transactionsuntrade-u)<br/>
[/upload](#/upload/) `WIP` <br/>
___
## Authorization Flow:

```
Authorization: Bearer JWT_Token
```

---
### <u> GET: /user/<:username> </u> ###

Get User Data and information `under development`

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `username` | required | string  | <br/>The username for which to fetch information. <br/><br/>

---

**Response**

```
{

   
}

or any implemented error

{
    "status": 404,
    "message": "No Transactions Found."
}
```
___

### <u> POST: /sign-up </u>
Creates a New User Entry. 

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `username` | required | string  |Username being created (4-10 chars).<br/>|
|        `name` | required | string  |  Users' full name. <br/> |
| `email` | required | email | User Email. 
|       `password` | required | string
---
**Response**

```
{
    "status": 201,
    "message": "Created."
}

or any implemented error
{
    "status": 409,
    "message": "Credentials already exist." / "Invalid Credentials Submitted."
}
```
___

### <u> POST: /login </u>
Initiates Handshake flow for login.

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                         |
| -------------:|:--------:|:-------:| ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `username` | required | string  |  <br/><br/>|
|       `password` | required | string  | 

---
**Response**

```
{
    "status": 200
    "message": JWT_token
}

or any implemented error
{
    "status": 401,
    "message": "Non-existent or invalid credentials."
}
```
___
# /transactions/ #
### <u> POST: /transactions/create </u>
Create a Transaction and Get an Address & QR code for payment (for deposit) or Initiate a withdrawal request (for withdrawal).

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                         |
| -------------:|:--------:|:-------:| ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `username` | required | string  |  <br/><br/> |
|       `amount` | required | integer  |  <br/><br/> |
|       `type` | required | string  | <br/> must be one of  ["withdrawal", "deposit"] <br/><br/> |

---
**Response**

```

- type: deposit
{
    "status": 201,
    "message": {
        "address": USDT-TRC20 Address to be paid,
        "qr_code": base64-encoded image.
    }
}

- type: withdrawal
{
    "status": 201,
    "message": "Created Withdrawal Request for {amount} USDT."
}

or any implemented error
{
    "status": 401,
    "message": "Non-existent or invalid credentials."
}
```
___
### <u> POST: /transactions/trade </u>
Trades an amount of money to the trade pool for a specific time period.

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                         |
| -------------:|:--------:|:-------:| ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `username` | required | string  |  <br/><br/> |
|       `amount` | required | int  |  <br/><br/> |
| `days` | required | int | <br><br>

---
**Response**

```
{
    "status": 201,
    "message": "Staked {amount} for {x} days"
}

or any implemented error
{
    "status": 401,
    "message": "Non-existent or invalid credentials."
}
```
___

### <u> POST: /transactions/untrade </u>
Removes an amount of money from the Pool.

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                         |
| -------------:|:--------:|:-------:| ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `username` | required | string  |  <br/><br/> |
|       `amount` | required | int  |  <br/>

---
**Response**

```
{
    "status": 201,
    "message": "Removed {amount}."
}

or any implemented error
{
    "status": 401,
    "message": "Non-existent or invalid credentials."
}
```
___
### <u> GET: /transactions/username </u>
Get all Transactions associated with a user.

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                         |
| -------------:|:--------:|:-------:| ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `username` | required | string  |  <br/><br/> |


---
**Response**

```
{
    "status": 200,
    "message": [
        {
            "_id": transaction_id,
            "username": username,
            "txn_type": One of ["deposit", "withdrawal", "trade"],
            "balance": wallet balance,
            "datetime": datetime,
        }
    ]
}

or any implemented error
{
    "status": 404/401,
    "message": "Resource not found" / "Non-existent or invalid credentials."
}
```