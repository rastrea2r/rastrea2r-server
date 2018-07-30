====
Rule
====

  Rule resource is used to serve the Yara rules to rastrea2r client

* **URL**

  /rastrea2r/api/v1.0/rule

* **Method:**
  
  `GET`
  
*  **URL Params**

   **Required:**
 
   `rulename=[YARARULENAME.yara]`

* **Data Params**

  `NA`

* **Success Response:**
  
  * **Code:** 200
    **Content:** `Contents of the YARA file requested`
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED
    **Content:** 
    `{
      "message": "Authentication Failed: http://localhost:5000/rastrea2r/api/v1.0/rule?rulename=example.yara", 
      "status": 401
      }`

  OR

  * **Code:** 405 METHOD NOT ALLOWED
    **Content:** 
    `{
        "message": "Method Not Allowed: http://localhost:5000/rastrea2r/api/v1.0/rule?rulename=example.yara", 
        "status": 405
      }`

* **Sample Call:**

.. code-block:: console

      curl -i -X GET \
        -H "Authorization:Basic [BASE64 String of (username:password)]" \
        'http://localhost:5000/rastrea2r/api/v1.0/rule?rulename=example.yara'

* **Notes:**

  Currently only basic Authentication is supported. Ensure that the user has been created in the server prior to accessing the API's.