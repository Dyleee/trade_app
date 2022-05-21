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

### <u> GET /user/<:username> </u>

Get User Data and Transaction information `under development`

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `username` | required | string  | <br/>The username for which to fetch information. <br/><br/>
|

**Response**

```
{
   
}

or any implemented error

{
    "code": 1000,
    "error": "An error message"
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
|       `password` | required | string  | 
**Response**

```
{
    "success": true
}

or any implemented error
{
    "code": 1000,
    "error": "An error message"
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


**Response**

```
{
    "success": true
    "access_token": OAUTH_token
}

or any implemented error
{
    "code": 1000,
    "error": "An error message"
}
```
___