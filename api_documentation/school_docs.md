# Sophisticated School Management System
## School Endpoints
#
### Check school blueprint route
**Request**

`GET api/school/hello`

**Authorized Users**

`all`


**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "School hello route"
}
</pre>

#

### Create school
**Request**

`POST api/school`

**Authorized Users**

`super_user`


**Request Body**
<pre>
{
    "name: String,
    "location": String
}
</pre>

**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "{school_name} created successfully"
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to create a school"
}
</pre>

`ERROR: 400 BAD REQUEST`

**Response Body**
<pre>
{
    "message": "A school wth that name already exists"
}
</pre>
#

### Modify school
**Request**

`PUT api/school/{school_id}`

**Authorized Users**

`super_user`


**Request Body**
<pre>
{
    "new_name": String,
    "new_location: String
}
</pre>

**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "School updated successfully"
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to modify school"
}
</pre>

`ERROR: 404 NOT FOUND`

**Response Body**
<pre>
{
    "message": "A school with the given ID does not exist"
}
</pre>

`ERROR: 400 BAD REQUEST`

**Response Body**
<pre>
{
    "message": "A school with that name already exists"
}
</pre>

#

### Delete school
**Request**

`DELETE api/school/{school_id}`

**Authorized Users**

`super_user`


**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "School deleted successfully"
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to delete a school"
}
</pre>

`ERROR: 404 NOT FOUND`

**Response Body**
<pre>
{
    "message": "A school with the given ID does not exist"
}
</pre>

#

### Get school by id
**Request**

`GET api/school/{school_id}`

**Authorized Users**

`super_user, owner, admin, teacher, auditor`


**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "school": {
        "id": school_id,
        "name": school_name,
        "location": school_location
    }
}
</pre>

`ERROR: 404 NOT FOUND`

**Response Body**
<pre>
{
    "message": "School not found"
}
</pre>

#

### Get all schools
**Request**

`GET api/school/`

**Authorized Users**

`super_user`


**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "schools":
    [
        {
            "id": school_id,
            "name": school_name,
            "location": school_location
        },
        {
            "id": school_id,
            "name": school_name,
            "location": school_location
        },
        {
            "id": school_id,
            "name": school_name,
            "location": school_location
        },

    ]
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to retrieve all schools"
}
</pre>#

### Create academic year
**Request**

`POST api/school/academic_year`

**Authorized Users**

`super_user, owner`


**Request Body**
<pre>
{
    "name: String,
    "school_id: Integer
}
</pre>

**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "Academic year created successfully"
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to create an academic year"
}
</pre>

#

### Delete academic year
**Request**

`DELETE api/school/academic_year/{academic_year_id}`

**Authorized Users**

`super_user, owner`


**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "Academic year deleted successfully"
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to delete academic year"
}
</pre>

`ERROR: 404 NOT FOUND`

**Response Body**
<pre>
{
    "message": "Academic year does not exist"
}
</pre>

#

### Modify academic year
**Request**

`PUT api/school/academic_year/{academic_year_id}`

**Authorized Users**

`super_user, owner`


**Request Body**
<pre>
{
    "academic_year_id": Integer,
    "new_academic_year_name" : String
}
</pre>

**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "Academic year updated successfully"
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to modify an academic year"
}
</pre>

`ERROR: 404 NOT FOUND`

**Response Body**
<pre>
{
    "message": "Academic year does not exist"
}
</pre>

#

### Get all academic years
**Request**

`GET api/school/{school_id}/academic_year`

**Authorized Users**

`super_user, owner`


**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "academic_years": List[AcademicYear]
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to retriev all academic years"
}
</pre>

#

### Create class
**Request**

`POST api/school/academic_year/{academic_year_id}/class`

**Authorized Users**

`super_user, owner`


**Request Body**
<pre>
{
    "class_name": String
}
</pre>

**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "Class created successfully"
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to create a class"
}
</pre>

#

### Delete a class
**Request**

`DELETE api/school/class/{class_id}`

**Authorized Users**

`super_user, owner`


**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "Class deleted successfully"
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to delete a class"
}
</pre>

`ERROR: 404 NOT FOUND`

**Response Body**
<pre>
{
    "message": "Class does not exist"
}
</pre>

#

### Modify class
**Request**

`PUT api/school/class/{class_id}`

**Authorized Users**

`super_user, owner`


**Request Body**
<pre>
{
    "new_data_format": String
}
</pre>

**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "Class modified successfully"
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to modify a class"
}
</pre>

`ERROR: 404 NOT FOUND`

**Response Body**
<pre>
{
    "message": "Class does not exist"
}
</pre>

#

### Get all academic years
**Request**

`GET api/school/academic_year/{academic_year_id}/class`

**Authorized Users**

`super_user, owner, admin`


**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "academic_year": String,
    "classes": List[Class]
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to retrieve all classes"
}
</pre>

`ERROR: 404 NOT FOUND`

**Response Body**
<pre>
{
    "message": "Academic year not found"
}
</pre>
