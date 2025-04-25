```toml
name = 'Create A Task'
method = 'POST'
url = 'http://127.0.0.1:8000/tasks'
sortWeight = 3000000
id = 'd5ee7630-4eee-4454-b062-5e84c8f270f7'

[body]
type = 'JSON'
raw = '''
{
   task_name: "New Test",
    task_type: "New Test",
    deadline: "2026-05-31"
}'''
```
