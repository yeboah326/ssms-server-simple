# Sophisticated School Management System
## Fees Endpoints

#

### Check fees blueprint endpoint
**Request**

`GET api/fees/hello`

**Authorized Users**

`all`

**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "Fees blueprint working"
}
</pre>

#

### Create new fee payment
**Request**

`POST api/fees/student/{student_id}`

**Authorized Users**

`super_user, admin, owner`


**Request Body**
<pre>
{
    "amount": Float
}
</pre>

**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "Fee payment created successfully"
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorizzed to create fee payment"
}
</pre>

#

### Modify fee payment
**Request**

`PUT api/fees/{fee_id}`

**Authorized Users**

`super_user, owner`


**Request Body**
<pre>
{
    "new_amount": Float
}
</pre>

**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "Fee payment update successfully"
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to modify fee payment"
}
</pre>

`ERROR: 404 NOT FOUND`

**Response Body**
<pre>
{
    "message": "Fee payment not found"
}
</pre>

#

### Delete fee payment
**Request**

`DELETE api/fees/{fee_id}`

**Authorized Users**

`super_user, owner`


**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "Fee payment deleted successfully"
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorizd to delete fee payment"
}
</pre>

`ERROR: 404 NOT FOUND`

**Response Body**
<pre>
{
    "message": "Fee payment not found"
}
</pre>



#

### Get all student fee payment
**Request**

`GET api/fees/student/{student_id}`

**Authorized Users**

`super_user, admin, owner`

**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "fees": List[Fees],
    "student_name": String
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to retrieve student fee payment"
}
</pre>
