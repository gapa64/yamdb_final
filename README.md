![yamdb workflow](https://github.com/gapa64/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
# Quick Start

The Project **Yamdb Final** implements CI\CD model for the API YAMDB.

API YAMDB is [Sergey K](https://github.com/gapa64)  student project, of the Django Rest Framework course, which is a part of Yandex Practicum Backend specialization.  
The project provides REST API and a whole backend infrastructure for the simple social network YamDB, where users may write their reviews for the different titles, comment and rate them.  

**Yamdb Final**  Deployed by github Actions toolset and Docker Compose.

The solution includes 3 docker containers
- backend 
- postgres Database
- Nginx Web Server

### Currently the project deployed at 
### [http:/yamdb-final.hopto.org/api/v1/](http:/yamdb-final.hopto.org/api/v1/)
### Try [base api url](http:/yamdb-final.hopto.org/api/v1/titles/)
### [Entire API specification](http:/yamdb-final.hopto.org/redoc)  


## Install
There several ways to deploy yamdb_final sloution
### Traditional way
```bash
git clone https://github.com/gapa64/yamdb_final
cd yamdb_final/infra
docker-compose -d up
```
### CI\CD way
Github Actions provides an extensive toolset for a CI\CD  model impplementation.
#### Prerequisites:
- Deploy VM in any public cloud provider
- Create [DockerHub](https://hub.docker.com/) Account
- [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) Yamdb final project, or [create a new repository from yamdb template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
- Generate RSA key for Github-Actions - VM communication. [How to example for Ubuntu](https://phoenixnap.com/kb/generate-setup-ssh-key-ubuntu)
- propagate public key to VM. Normally it's done during VM creation. If it's not done use the [following utility](https://www.ssh.com/academy/ssh/copy-id)
- [Create telegram bot](https://core.telegram.org/bots), and [telegram](https://telegram.org/) account If you need notifications of deployment process, otherwise remove send_message from github workflow.
- Figure out your chat id. E.g. use [get my id bot](https://t.me/getmyid_bot) 

Configure the following Github Actions [Secrets](https://docs.github.com/en/rest/actions/secrets)

Parameter | Description
--- | --- 
HOST | Remote server where the project should be deployed
USER | User used by Github actions to deploy the project on a remote server
SSH_KEY | Copy private key of the USER
DB_ENGINE | django.db.backends.postgresql
DB_HOST | 127.0.0.1 by default 
DB_NAME | postgres by default 
DB_PORT | 5432 by default 
POSTGRES_PASSWORD | postgres by default 
POSTGRES_USER | postgres by default 
DOCKER_IMAGE | Custom name of YamdB docker image
DOCKER_USERNAME | username for an account at docker hub
DOCKER_PASSWORD | password for an account at docker hub
EMAIL_HOST | remote smtp server e.g. smtp.gmail.com
EMAIL_HOST_USER | username to access smtp server
EMAIL_HOST_PASSWORD | password to access smtp server
EMAIL_ADMIN | main email address  to send mails with confirmation code
EMAIL_USE_TLS | Boolean value True or False, set True TLS required by remote server. False if not specified by default.
EMAIL_USE_SSL | Boolean value True or False, set True if SSL required by remote server. False if not specified by default. Mutually exclusive with EMAIL_USE_TLS
TELEGRAM_TO | Chat id to send notification
TELEGRAM_TOKEN | token of the bot which sends notifications


Upon commit to master, the Github Actions run the following jobs:

#### Jobs
- tests. Autotests
- build_and_push_to_docker_hub. Auto rebuild of yamdb-final docker image and pushing it to Docker Hub.
- deploy. Deploys project on a server.
- send_message. Sends notification

## YAMDB Documentation

### Try [base api url](http:/yamdb-final.hopto.org/api/v1/titles/)
### [Entire API specification](http:/yamdb-final.hopto.org/redoc)
### API examples
There are several examples of API calls
- [Get list of titles](#get-list-of-titles)
- [Get single title](#get-single-title)
- [Get list of reviews for particular title](#get-list-of-reviews-for-particular-title)
- [Post a review](#post-review)
- [Comment a review](#comment-a-review)
- [Create a new user](#create-a-new-user)
- [Retrieve Authorization Token](#retrieve-token)

#### Get list of Titles
`GET /api/v1/titles/`

Response
```bash
HTTP/1.1 200 OK
Server: nginx
Date: Sat, 06 Aug 2022 15:54:36 GMT
Content-Type: application/json
Content-Length: 4219
Connection: keep-alive
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
```
Body
```json
{
  "count": 7,
    "next": "http://web:8000/api/v1/titles/?page=2",
    "previous": null,
    "results": [
      {
        "id": 7,
        "category": {
          "name": "Music",
        "slug": "music"
        },
        "genre": [
          {
            "name": "Heavy Metal",
            "slug": "heavymetal"
          }
        ],
        "rating": null,
        "name": "Ride the Lightning",
        "year": 1991,
        "description": "Generic Description"
      }
   ]
}
```
#### Get single title
`GET /api/v1/titles/6/`

Body
```json
{
    "id": 6,
    "category": {
        "name": "Music",
        "slug": "music"
    },
    "genre": [
        {
            "name": "alternative",
            "slug": "alternative"
        },
        {
            "name": "Rock",
            "slug": "rock"
        },
        {
            "name": "Nu Metal",
            "slug": "numetal"
        }
    ],
    "rating": 8.5,
    "name": "Untouchables",
    "year": 2002,
    "description": "Generic Example"
}
```
#### Get list of reviews for particular title
`GET /api/v1/titles/6/reviews`

Response
```bash
HTTP/1.1 200 OK
Server: nginx
Date: Sat, 06 Aug 2022 17:07:34 GMT
Content-Type: application/json
Content-Length: 534
Connection: keep-alive
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
```
Body
```json
{
  "count": 2, 
  "next": null, 
  "previous": null, 
  "results": [
    {
      "id": 2,
      "author": "gapa",
      "title": 6,
      "pub_date": "2022-08-06T17:04:41.430325Z",
      "score": 9,
      "text": "Generic text"
    },
    {
      "id": 1,
      "author": "panda",
      "title": 6,
      "pub_date": "2022-08-06T16:09:52.043352Z",
      "score": 8,
      "text": "Generic text"
    }
  ]
}
```
#### Post review
To post a review for a particular title, the title_id is needed.

`POST /api/v1/titles/{title_id}/reviews/`
```bash
content type: application/json
Authorization: Bearer <token>
```
```json
{
  "text": "Very food title, real masterpiece", 
  "score": 9
}
```
Response
```bash
HTTP/1.1 201 Created
Server: nginx
Date: Tue, 09 Aug 2022 21:01:07 GMT

Content-Type: application/json
Content-Length: 130
Connection: keep-alive
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
```
Body
```json
{
  "id":4, 
  "author":"sergey",
  "title":6,
  "pub_date":"2022-08-09T21:01:07.145618Z",
  "score":9,
  "text":"Very food title, real masterpiece"
}
```
#### Comment a review
To post c comment for a particular review the title-id and review-id required

`POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/`
```bash
content type: application/json
Authorization: Bearer <token>
```
Body
```json
{
  "text": "Fully agree with review!"
}
```
Response
```bash
HTTP/1.1 201 Created
Server: nginx
Date: Tue, 09 Aug 2022 21:09:44 GMT
Content-Type: application/json
Content-Length: 112
Connection: keep-alive
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
```
Body
```json
{
  "id":3,
  "author":"sergey",
  "review":4,
  "pub_date":"2022-08-09T21:09:44.886943Z",
  "text":"Fully agree with review!"
}
```
#### Create a new user
User Creation and authorisation is a two factor process.
Register New User

`POST /api/v1/auth/signup/`
```bash
content type: application/json
```
Body
```json
{
  "username": "testuser", 
  "email": "testuser@mail.com"
}
```
Response
```bash
HTTP/1.1 200 OK
Server: nginx
Date: Tue, 09 Aug 2022 20:46:47 GMT
Content-Type: application/json
Content-Length: 53
Connection: keep-alive
Vary: Accept
Allow: POST, OPTIONS
X-Frame-Options: SAMEORIGIN
```
Body
```json
{
  "username": "testuser", 
  "email": "testuser@mail.com"
}
```
#### Retrieve Token
The server will send an email with confirmation Code.  
Confirm your username with the confirmation code.
`POST /api/v1/auth/token/`
```bash
content type: application/json
```
Body
```json
{
  "username": "testuser",
  "confirmation_code":"confirmation code from email"
}
```
Response
```bash
HTTP/1.1 200 OK
Server: nginx
Date: Tue, 09 Aug 2022 20:49:46 GMT
Content-Type: application/json
Content-Length: 133
Connection: keep-alive
Vary: Accept
Allow: POST, OPTIONS
X-Frame-Options: SAMEORIGIN
```
Body
```json
{
  "token":"Token_data"
}
```
### Usefull links:
[Models Diagram](https://drive.google.com/file/d/1T9OHj-UAWXTzzAm7cWSml5KN8PDwlQUf/view?usp=sharing)
```bash
actual Docker api_yamdb image gaps64/api_yamdb:latest
```
## Author
- [Sergey K](https://github.com/gapa64)
