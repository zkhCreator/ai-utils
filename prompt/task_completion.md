here is my new task, the main aim is: 
convert an openapi json to swift service with Moya and create the request and response model;

there a some step:

1. create all of the request model in the openapi, and create all of these model to one swift File, all of the id property in the model should be type of `UUID`
2. create a request service based on Moya Service. if there are any login api in the openapi json, the request service should be extend to `AccessTokenAuthorizable`, and you should setup the impletion authorizationType in the service file with it's request type.
3. create all of the response model in the openApi, and create all of these model to one swift File, all of the id property in the model should be type of `UUID`.

after create all of these file, maybe you should give the covert python code, it will help me create other times.
