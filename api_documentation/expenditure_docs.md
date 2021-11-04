# Sophisticated School Management System
## Expenditure Endpoints

#

### Create expenditure
**Request**

`POST api/expenditure/academic_year/{academic_year_id}`

**Authorized Users**

`super_user, admin, owner`


**Request Body**
<pre>
{
    "description": String,
    "amount": Float
}
</pre>

**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "Expenditure created successfully"
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to create expenditure"
}
</pre>

#

### Modify expenditure
**Request**

`PUT api/expenditure/{expenditure_id}`

**Authorized Users**

`super_user, owner`


**Request Body**
<pre>
{
    "new_description": String,
    "new_amount": Float
}
</pre>

**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "Expenditure updated successfully"
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to creat
}
</pre>

`ERROR: 404 NOT FOUND`

**Response Body**
<pre>
{
    "message": "Expenditure not found"
}
</pre>

#

### Delete expenditure
**Request**

`DELETE api/expenditure/{expenditure_id}`

**Authorized Users**

`super_user, owner`


**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "Expenditure deleted successfully"
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to delete expenditure"
}
</pre>

`ERROR: 404 NOT FOUND`

**Response Body**
<pre>
{
    "message": "Expenditure not found"
}
</pre>

#

### Get all expenditure for academic year
**Request**

`GET api/expenditure/academic_year/{academic_year_id}?page={current_page}&per_page={items_per_page}&month={month_number}`

**Authorized Users**

`super_user, admin, owner`


**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "expenditures": List[Expenditure],
    "toal_month_expenditure": Float,
    "total_page": Integer,
    "prev_page": Integer,
    "next_page": Integer
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to retrieve expenditure"
}
</pre>

#

### Get expenditure
**Request**

`GET api/expenditure/{expenditure_id}`

**Authorized Users**

`super_user, admin, owner`


**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "expenditure": Expenditure
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to view an expenditure"
}
</pre>

`ERROR: 404 NOT FOUND`

**Response Body**
<pre>
{
    "message": "Expenditure not found"
}
</pre>


#

### Request Template
**Request**

``

**Authorized Users**

``


**Request Body**
<pre></pre>

**Response**

``

**Response Body**
<pre></pre>
