# Sophisticated School Management System
## Auth Endpoints

#

### Create new token
**Request**

`POST api/auth/token`

**Authorized Users**

`all`

**Request Body**
<pre>
{
    "username": "name",
    "password": "password"
}
</pre>

**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
For SuperUser
{
    "token": token,
    "user": {
        "name": user_name,
        "public_id": user_public_id,
        "role": user_role,
        "username": user_username
    }
}

For SchoolUser
{
    "token": token,
    "user": {
        "name": user_name,
        "public_id": user_public_id,
        "role": user_role,
        "school_id": user_school_id,
        "username": user_username
    }
}

</pre>

`ERROR: 400 BAD REQUEST`

**Response Body**
<pre>
{
    "message": "Username or password is invalid"
}
</pre>

### Create new user account
**Request**

`api/auth/register`

**Authorized Users**

`super_user`


**Request Body**
<pre>
{
    "user_type": String Options["super_user", "admin", "auditor", "teacher", "owner"},
    "username": String,
    "password": String,
    "email": String,
    "school_id": String
}
</pre>

**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "User created successfully",
    "user": New user name
}
</pre>

`ERROR: 400 BAD REQUEST`

**Response Body**
<pre>
{
    "message": "A user with this email already exists",
}
</pre>
