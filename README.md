# Dummy data

## What is it?

First of all, I want to explain what this code does and a bit of what it does not.

on this current Iteration, this code is capable to CREATE courses and users, not at the same time, but making separate calls within the code.

We don't have an interface yet for this, however we are planning for it.

Dummy data does have 2 files called "dummy_courses.json" and "dummy_users.json" which each one respectively, have 200 records with dummy (non-existing or not based on existing people) data.

Dummy data code will take that data and ingest it, generate random groups of values based on the requested data.

Then, it, based on parameters, will post (Currently it only posts) the data to a Learn instance and return a message based on the data that was correctly posted and store it to avoid creating new data based on that.

## The dummy data process

1. We start by generating a global utilities object that allows us to have general purpose functions and specific paths.
2. Then we evaluate the current device. We look for:
   a. The device has internet
   b. If the instance registered is available. We make a health check on it.
   c. If the folder where the dummy data folder is stored has permissions to create files, since it requires to create several files.
   d. We check if the config file exists.
   e. If the config file has data on it, we do not validate the content, only if there are strings there.
   f. If everything is checked, we continue. If not, the script will tell you what problems it found and kill the process.
3. Then, a script comes over and calls the developers.anthology.com page's s3 bucket that hosts the swagger. It will download it once a day, and conver it in a way where the keys will no longer be the endpoints such as /learn/api/v1... but instead, we use the summary, like: Create Courses (case sensitive). This helps us to avoid using versions of the api that outdated automatically and simplifies the calls to a small string (in many cases).
4. Then, we create a token, making a simple call to the learn instance requesting it.
5. Then we connect with the data_handler process to obtain the data_handler object and methods.
6. Same as #5 but with caller_handler to obtain the caller object and methods.
7. Then we jump to dsk since all the data should be wrapped around the same dsk for control purposes, however, it is not required for ALL endpoints, but on the current scope, all data must have it.
8. At the end we have course and users handlers which each one create the data accordingly.

## Configuring Dummy Data

1. Make sure to have already followed our process on docs.anthology.com to:
   a. Register a new application and obtain the key and secret and application id
   b. Register the application on your Learn instance and associate the integration user with the permissions to create users and create courses.
2. On your local version fo dummy data open the file called config.json and enter your:
   a. application_key
   b. secret
   c. url
   When entering your url, please make sure it does not have a / at the end. just a .com with no / at the end.

And that should be it!

## Creating users or courses

In order to create either, open the files course_handler.py or user_handler.py accordingly.

### Course Handler

At the end of the file you will see the main, (line 66 approx), and it calls the create_dummy_courses_main function after instatiating the object, now, it expects 2 mandatory arguments:
a. type_of_course_view: expects a string, but can only have any one of these values: ["random_all","random","original","ultra"]

- When entering "random_all" the course view will be randomized between ["Classic", "Ultra", "Undecided", "UltraPreview"]
- When entering "random" the course view will be randomized between ["Classic", "Ultra"]
- When entering "original" all courses view will be created as ["Classic"]
- When entering "ultra" all courses will be created as ["Ultra"]

b. requested_data is an integer and expects a number between 1 and 200. This will be the ammount of data that will be generated.

-> You need to be mindful of the data that has already been written under dummy_data_stored.json, since any data that has already been written here will no longer be used when creating new data sets. This applies for everything.

### User Handler

When creating users, the main function expects 2 mandatory arguments and 1 situational argument:
a. requested_data is an integer and expects a number between 1 and 200. This will be the ammount of data that will be generated.
b. type_of_password is a string and must be between these values: ['one_for_all','random_for_all','custom'] and this is what each one does:

- one_for_all: Will generate one uuid that will be used for all users requested.
- random_for_all: Will generate one uuid per user based on the requested data
- custom: You can setup your own password and it needs to be provided on the custom_password parameter.

c. custom_password is an optional string and here you should enter the value of your custom password for each user.

## Stored values

Whenever a new value is generated and sent to learn and a 200 or 201 is returned by the api, its id will be stored on dummy_data_stored.json.

## More dummy data.

So... the idea of this is to allow more dummy data to come over, I am not 100% sure it works but it may may work since the framework was designed to just function.

### Json dummy format

#### File name

Let's use dummy\_(type_of_dummy).json, for example, we want to start creating dummy terms, so, we can use: dummy_terms.json file.

#### Content of the file

there is a specific format we are using which starts with an id starting on 0 until 199.

All data must be wrapped with two keys:

- id
- values

like this

```json
{
"id": 182,
"values": {
   "key":"ACTUAL ENDPOINT EXPECTED PAYLOAD"
   }
}
```

#### Custom .py file

After the custom json file has been created, one of the first things that need to be created on the object are the endpoint summary name.
Then you need to create the metadata and should have the following information:
```json
{
"type": "could be term, could be content etc",
"location": "self.curr_path + actual file name",
"fields_to_update": "['dataSourceId', 'other_value']"
}
```
We need then to call self.dsk = return_dsk() to retrieve the dsk IF REQUIRED!
and a general dummy_data variable empty list.

On data_handler, there is a validator that needs to also be updated when creating new types of dummy data and the meta data type value should be included on that list.

Then we:

1. Create the payload
2. Create the custom values
3. Post the data
4. Wrap the logic on a main function.

### More documentation
https://miro.com/app/board/uXjVNqwycJs=/?share_link_id=495599097475
