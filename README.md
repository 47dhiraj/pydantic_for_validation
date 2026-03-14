<div align="center" style="display: flex; justify-content: center; align-items: center;">
  <img src="https://cdn.simpleicons.org/pydantic/E92063" width="120" alt="Pydantic Logo" /><br/>
  <span style="padding-left: 1rem; font-size:3.7em; color:#E92063;">pydantic</span>
</div>

### [***Pydantic version: v2.12.5***](https://docs.pydantic.dev/latest/)

<br>

### Pydantic is a Python data validation library that uses type hints to:

- `1. Validate data at runtime`

- `2. Data conversion (serialization / deserialization)`

-----------------------------------------------------------
<br>

## Serialization (occurs when server send api response to client)
* Python object (int, str, float, list, tuple, dict, set, frozenset, class object)  ➥  JSON string / yaml / toml / pickle ... 

### Serialization METHODS

| Operation | pydantic v2 | Description |
|-----------|-----------|-------------|
| Model to Dict | `.model_dump()` | convert to Python dict |
| Model to JSON | `.model_dump_json()` | convert to JSON string |
| Model to pretty JSON | `.model_dump_json(indent=2)` | convert to formatted JSON |


-----------------------------------------------------------
<br>

## Deserialization (occurs when client send api request to server)
* JSON string / yaml / toml / pickle ...  ➥  Python object (int, str, float, list, tuple, dict, set, frozenset, class object)

### Deserialization METHODS

| Operation | pydantic v2 | Description |
|-----------|-----------|-------------|
| Dictionary validation | `.model_validate()` | validate a python dictionary |
| JSON validation | `.model_validate_json()` | validate a JSON string |

-----------------------------------------------------------
