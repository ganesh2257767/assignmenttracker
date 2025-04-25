```toml
name = 'Login User'
method = 'POST'
url = 'http://127.0.0.1:8000/login'
sortWeight = 1000000
id = '04b13435-fc18-40f0-975e-f19418c2c1be'

[auth]
type = 'OAUTH2'

[[body.formData]]
key = 'username'
value = 'ganesh@kutty.com'

[[body.formData]]
key = 'password'
value = 'Password123'
```
