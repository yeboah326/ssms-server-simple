# Sophisticated School Management System
## Student Endpoints

#

### Check student blueprint route
**Request**

`GET api/student/hello`

**Authorized Users**

`all`


**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "Student blueprint working
}
</pre>

#

### Create student
**Request**

`api/student/class/{class_id}`

**Authorized Users**

`super_user, admin, owner`


**Request Body**
<pre>
{
    "name": String,
    "date_of_birth" "YYYY-MM-DD" [Optional]
}
</pre>

**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "Student created successfully"
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User does not have the right privelegess to perform specified activities"
}
</pre>

#

### Modify student
**Request**

`PUT api/student/{student_id}`

**Authorized Users**

`super_user, admin, owner`


**Request Body**
<pre>
{
    "new_name": String,
    "new_date_of_birth: "YYYY-MM-DD"
}
</pre>

**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "Student does not exist"
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User does not have the right priveleges to perform specified actions"
}
</pre>

`ERROR: 404 NOT FOUND`

**Response Body**
<pre>
{
    "message": "Student does not exist"
}
</pre>
#

### Delete student
**Request**

`DELETE api/student/{student_id}`

**Authorized Users**

`super_user, owner`


**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "message": "Student deleted successfully"
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to delete student"
}
</pre>

`ERROR: 404 NOT FOUND`

**Response Body**
<pre>
{
    "message": "Student does not exist"
}
</pre>

#

### Get all students in a class
**Request**

`GET api/student/class/{class_id}`

**Authorized Users**

`super_user, owner, admin`

**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "students": List[Student]
}
</pre>

`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to get all students in a class"
}
</pre>

#

### Search for student by name
**Request**

`GET api/student/class/{class_id}/search?name={student_name}`

**Authorized Users**

`super_user, owner, admin`

**Response**

`SUCCESS: 200 OK`

**Response Body**
<pre>
{
    "students": List[Student]
}
</pre>


`ERROR: 401 UNAUTHORIZED`

**Response Body**
<pre>
{
    "message": "User is not authorized to perform this search"
}
</pre>
