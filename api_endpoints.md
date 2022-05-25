# API endpoints

## GET
[/user/<:username>/](#user) <br/>
[/transactions/?username](#transactions) <br/>
[/transaction/?txn_id](#transaction) <br/>

## POST
[/sign-up](#sign-up/) <br/>
[/login](#/login/) <br/>
[/upload](#/upload/) <br/>
___
## Authorization Flow:

```
Authorization: Bearer JWT_Token
```

---
### <u> GET /user/<:username> </u>

Get User Data and Transaction information `under development`

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

### <u> POST /sign-up </u>
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
    "status": 200,
    "message": "Success
}

or any implemented error
{
    "status": 409,
    "message": "Credentials already exist." / "Invalid Credentials Submitted."
}
```
___

### <u> POST /login </u>
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