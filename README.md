# Jambo - JSON Schema to Pydantic Converter

**Jambo** is a Python package that automatically converts [JSON Schema](https://json-schema.org/) definitions into [Pydantic](https://docs.pydantic.dev/) models. 
It's designed to streamline schema validation and enforce type safety using Pydantic's powerful validation features.

Created to simplifying the process of dynamically generating Pydantic models for AI frameworks like [LangChain](https://www.langchain.com/), [CrewAI](https://www.crewai.com/), and others.

---

## ✨ Features

- ✅ Convert JSON Schema into Pydantic models dynamically
- 🔒 Supports validation for strings, integers, floats, booleans, arrays, and nested objects
- ⚙️ Enforces constraints like `minLength`, `maxLength`, `pattern`, `minimum`, `maximum`, `uniqueItems`, and more
- 📦 Zero config — just pass your schema and get a model

---

## 📦 Installation

```bash
pip install jambo
```

---

## 🚀 Usage

```python
from jambo.schema_converter import SchemaConverter

schema = {
    "title": "Person",
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
    },
    "required": ["name"],
}

Person = SchemaConverter.build(schema)

obj = Person(name="Alice", age=30)
print(obj)
```

---

## ✅ Example Validations

### Strings with constraints

```python
schema = {
    "title": "EmailExample",
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "minLength": 5,
            "maxLength": 50,
            "pattern": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        },
    },
    "required": ["email"],
}

Model = SchemaConverter.build(schema)
obj = Model(email="user@example.com")
print(obj)
```

### Integers with bounds

```python
schema = {
    "title": "AgeExample",
    "type": "object",
    "properties": {
        "age": {"type": "integer", "minimum": 0, "maximum": 120}
    },
    "required": ["age"],
}

Model = SchemaConverter.build(schema)
obj = Model(age=25)
print(obj)
```

### Nested Objects

```python
schema = {
    "title": "NestedObjectExample",
    "type": "object",
    "properties": {
        "address": {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "city": {"type": "string"},
            },
            "required": ["street", "city"],
        }
    },
    "required": ["address"],
}

Model = SchemaConverter.build(schema)
obj = Model(address={"street": "Main St", "city": "Gotham"})
print(obj)
```

---

## 🧪 Running Tests

To run the test suite:

```bash
poe tests
```

Or manually:

```bash
python -m unittest discover -s tests -v
```

---

## 🛠 Development Setup

To set up the project locally:

1. Clone the repository
2. Install [uv](https://github.com/astral-sh/uv) (if not already installed)
3. Install dependencies:

```bash
uv sync
```

4. Set up git hooks:

```bash
poe create-hooks
```

---

## 📌 Roadmap / TODO

- [ ] Support for `enum` and `const`
- [ ] Support for `anyOf`, `allOf`, `oneOf`
- [ ] Schema ref (`$ref`) resolution
- [ ] Better error reporting for unsupported schema types

---

## 🤝 Contributing

PRs are welcome! This project uses MIT for licensing, so feel free to fork and modify as you see fit.

---

## 🧾 License

MIT License.