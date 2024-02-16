# Curl examples

```bash

# Add feedback to chat session with id 1 and query with id 3
curl 'http://localhost:5173/api/feedback/1/3' \
 -H 'Accept: _/_' \
 -H 'Authorization: Basic YXNkZjphc2Rm' \
 -H 'Content-Type: application/json'

# Get all users
curl 'http://localhost:5173/api/users' \
 -H 'Accept: _/_' \
 -H 'Authorization: Basic YXNkZjphc2Rm' \
 -H 'Content-Type: application/json'

# Add user
curl 'http://localhost:5173/api/users' \
 -H 'Accept: _/_' \
 -H 'Authorization: Basic YXNkZjphc2Rm' \
 -H 'Content-Type: application/json' \
 --data-raw '{"username":"asdf1", "password": "asdf", "roles": "admin,user"}'

# Add user but user in request has note enough permission -> should fail
curl 'http://localhost:5173/api/users' \
 -H 'Accept: _/_' \
 -H 'Authorization: Basic aGFuczphc2Rm' \
 -H 'Content-Type: application/json' \
 --data-raw '{"username":"asdf1", "password": "asdf", "roles": "admin,user"}'

# Delete user with id 4
curl -XDELETE 'http://localhost:5173/api/users/4' \
 -H 'Accept: _/_' \
 -H 'Authorization: Basic YXNkZjphc2Rm' \
 -H 'Content-Type: application/json'

# Create chat session
curl -XPOST 'http://localhost:5173/api/chat-sessions' \
 -H 'Accept: _/_' \
 -H 'Authorization: Basic YXNkZjphc2Rm' \
 -H 'Content-Type: application/json'

# Get all chat sessions
curl 'http://localhost:5173/api/chat-sessions' \
 -H 'Accept: _/_' \
 -H 'Authorization: Basic YXNkZjphc2Rm' \
 -H 'Content-Type: application/json'

# Get chat session with id 1
curl 'http://localhost:5173/api/chat-sessions/1' \
 -H 'Accept: _/_' \
 -H 'Authorization: Basic YXNkZjphc2Rm' \
 -H 'Content-Type: application/json'
```
