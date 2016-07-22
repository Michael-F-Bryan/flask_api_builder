blueprint-name: api
prepend-with: /todo/api/v1
#Method    URL                       Description
GET       /tasks                     Retrieve list of tasks
GET       /tasks/<int:task_id>       Retrieve task number <task_id>
POST      /tasks                     Create a new task 
PUT       /tasks/<int:task_id>       Update an existing task 
DELETE    /tasks/<int:task_id>       Delete an existing task 
