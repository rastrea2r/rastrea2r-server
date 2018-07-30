=======
Results
=======

  Results Resource is used to store the results from rastrea2r client

* **URL**

  /rastrea2r/api/v1.0/results

* **Method:**
  
  `POST`
  
*  **URL Params**

   **Required:**
 
   `NA`

* **Data Params**

  <Payload must be a Valid JSON> 
  `{"key1":"value1", "key2":"value2"}`

* **Success Response:**
  
  * **Code:** 200 
    **Content:** 
     `{
      "message": "Results Saved Successfully",
      "status": "200"
      }`
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED 
    **Content:** 
     `{
        "message": "Authentication Failed: http://localhost:5000/rastrea2r/api/v1.0/results", 
        "status": 401
      }`

  OR

  * **Code:** 400 BAD REQUEST 
    **Content:** 
      `{
        "message": "Bad Request: http://localhost:5000/rastrea2r/api/v1.0/results",
        "status": 400
       }`

   OR

    * **Code:** 405 METHOD NOT ALLOWED
      **Content:** 
      `{
        "message": "Method Not Allowed: http://localhost:5000/rastrea2r/api/v1.0/results", 
        "status": 405
      }`

* **Sample Call:**

.. code-block:: console

          curl -i -X POST \
          -H "Content-Type:application/json" \
          -H "Authorization:Basic [BASE64 String of (username:password)]" \
          -d \
          '{"Key1":"Value1", "Key2":"Value2"}' \
          'http://localhost:5000/rastrea2r/api/v1.0/results'

* **Notes:**

  Currently only basic Authentication is supported. Ensure that the user has been created in the server prior to accessing the API's.