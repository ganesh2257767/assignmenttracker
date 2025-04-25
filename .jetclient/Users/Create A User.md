```toml
name = 'Create A User'
method = 'POST'
url = 'http://127.0.0.1:8000/users'
sortWeight = 1000000
id = 'f27eeef9-b16d-463b-a195-f0060ac68942'

[body]
type = 'JSON'
raw = '''
{
  email: "ganesh@kutty.com",
  password: "Password123"
}'''
```
