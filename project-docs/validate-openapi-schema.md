# OpenAPI结构数据验证技术文档

## 1. 接口概述

OpenAPI结构数据验证接口是LLMOps项目中用于验证用户提交的OpenAPI规范字符串是否符合项目要求的核心功能。该接口不仅用于独立的数据验证，还被集成到API工具创建和更新流程中，确保所有自定义API工具都符合统一的数据格式标准。

- **核心接口**：`POST:/api-tools/validate-openapi-schema`
- **主要功能**：验证OpenAPI-Schema字符串的格式正确性
- **集成场景**：创建API工具、更新API工具提供者

***

## 2. 功能说明

### 2.1 主要功能

1. **OpenAPI字符串验证**：检查传入的JSON字符串是否符合项目定义的OpenAPI规范
2. **格式校验**：验证JSON结构、必填字段、数据类型等
3. **逻辑校验**：验证operationId唯一性、参数合法性等
4. **数据标准化**：在验证过程中对有效数据进行标准化处理

### 2.2 相关接口

| 接口名称      | 接口路径                                      | 说明      |
| --------- | ----------------------------------------- | ------- |
| 校验OpenAPI | `POST:/api-tools/validate-openapi-schema` | 独立的验证接口 |
| 创建API工具   | `POST:/api-tools`                         | 集成验证功能  |

***

## 3. 实现原理

### 3.1 整体架构

```
请求 → FlaskForm验证 → JSON解析 → OpenAPISchema验证 → 响应
         ↓
    基础字段校验
         ↓
    api_tool_service.parse_openapi_schema()
         ↓
    OpenAPISchema(**data)
         ↓
    Pydantic字段验证器
         ↓
    成功/失败响应
```

### 3.2 核心类和模块

| 文件路径                                                       | 类/函数                                    | 说明          |
| ---------------------------------------------------------- | --------------------------------------- | ----------- |
| `internal/schema/api_tool_schema.py`                       | `ValidateOpenAPISchemaReq`              | 请求验证表单      |
| `internal/service/api_tool_service.py`                     | `ApiToolService.parse_openapi_schema()` | OpenAPI解析入口 |
| `internal/core/tools/api_tools/entities/openapi_schema.py` | `OpenAPISchema`                         | 核心验证模型      |
| `internal/core/tools/api_tools/entities/openapi_schema.py` | `ParameterType`                         | 参数类型枚举      |
| `internal/core/tools/api_tools/entities/openapi_schema.py` | `ParameterIn`                           | 参数位置枚举      |

***

## 4. 数据验证规则

### 4.1 OpenAPISchema顶层结构

| 字段            | 类型     | 必填 | 说明      | 验证规则    |
| ------------- | ------ | -- | ------- | ------- |
| `server`      | string | 是  | 服务基础地址  | 不能为空字符串 |
| `description` | string | 是  | 工具描述    | 不能为空字符串 |
| `paths`       | object | 是  | API路径定义 | 不能为空字典  |

### 4.2 paths结构

`paths`是一个字典，键为URL路径（如`/suggest`），值为方法字典。

**支持的HTTP方法**：`get`、`post`

### 4.3 方法对象结构

每个方法（如`get`、`post`）对应一个对象，包含以下字段：

| 字段            | 类型     | 必填 | 说明           |
| ------------- | ------ | -- | ------------ |
| `description` | string | 是  | 接口描述         |
| `operationId` | string | 是  | 唯一标识符（需全局唯一） |
| `parameters`  | array  | 否  | 参数列表         |

### 4.4 参数对象结构

| 字段            | 类型      | 必填 | 说明   | 可选值                                             |
| ------------- | ------- | -- | ---- | ----------------------------------------------- |
| `name`        | string  | 是  | 参数名称 | -                                               |
| `in`          | string  | 是  | 参数位置 | `path`/`query`/`header`/`cookie`/`request_body` |
| `description` | string  | 是  | 参数描述 | -                                               |
| `required`    | boolean | 是  | 是否必填 | `true`/`false`                                  |
| `type`        | string  | 是  | 参数类型 | `str`/`int`/`float`/`bool`                      |

***

## 5. 接口调用示例

### 5.1 验证OpenAPI Schema

**请求示例**：

```json
POST /api-tools/validate-openapi-schema
Content-Type: application/json

{
  "openapi_schema": "{\"description\":\"这是一个查询对应英文单词字典的工具\",\"server\":\"https://dict.youdao.com\",\"paths\":{\"/suggest\":{\"get\":{\"description\":\"根据传递的单词查询其字典信息\",\"operationId\":\"YoudaoSuggest\",\"parameters\":[{\"name\":\"q\",\"in\":\"query\",\"description\":\"要检索查询的单词，例如love/computer\",\"required\":true,\"type\":\"str\"},{\"name\":\"doctype\",\"in\":\"query\",\"description\":\"返回的数据类型，支持json和xml两种格式，默认情况下json数据\",\"required\":false,\"type\":\"str\"}]}}}}"
}
```

**成功响应示例**：

```json
{
  "code": "success",
  "data": {},
  "message": "openapi-schema数据格式无误"
}
```

**失败响应示例**：

```json
{
  "code": "validate_error",
  "data": {},
  "message": "openapi-schema校验失败，info不能为空"
}
```

### 5.2 创建API工具（集成验证）

```json
POST /api-tools
Content-Type: application/json

{
  "name": "有道词典",
  "icon": "https://example.com/icon.png",
  "openapi_schema": "{\"description\":\"这是一个查询对应英文单词字典的工具\",\"server\":\"https://dict.youdao.com\",\"paths\":{\"/suggest\":{\"get\":{\"description\":\"根据传递的单词查询其字典信息\",\"operationId\":\"YoudaoSuggest\",\"parameters\":[{\"name\":\"q\",\"in\":\"query\",\"description\":\"要检索查询的单词，例如love/computer\",\"required\":true,\"type\":\"str\"}]}}}}",
  "headers": []
}
```

***

## 6. 错误处理机制

### 6.1 错误类型

| 错误类型 | 异常类                      | 说明               |
| ---- | ------------------------ | ---------------- |
| 验证错误 | `ValidateErrorException` | 数据格式、类型、逻辑等验证失败  |
| 未找到  | `NotFoundException`      | 资源不存在（用于创建/更新流程） |

### 6.2 常见错误信息

| 错误信息                                                     | 原因                 |
| -------------------------------------------------------- | ------------------ |
| `传递数据必须符合OpenAPI规范的JSON字符串`                              | JSON解析失败           |
| `server不能为空且为字符串`                                        | server字段缺失或为空      |
| `description不能为空且为字符串`                                   | description字段缺失或为空 |
| `openapi_schema中的paths不能为空且必须为字典`                        | paths字段无效          |
| `operationId必须唯一，{id}出现重复`                               | operationId重复      |
| `parameter.in参数必须为path/query/header/cookie/request_body` | 参数位置无效             |
| `parameter.type参数必须为str/int/float/bool`                  | 参数类型无效             |

***

## 7. 相关代码说明

### 7.1 OpenAPISchema 核心验证类

**文件路径**：[openapi\_schema.py](file:///home/wissfi/projects/LLMOps/llmops-api/internal/core/tools/api_tools/entities/openapi_schema.py)

```python
class OpenAPISchema(BaseModel):
    """OpenAPI规范的数据结构"""
    server: str = Field(...)
    description: str = Field(...)
    paths: dict[str, dict] = Field(...)
    
    @field_validator("server", mode="before")
    def validate_server(cls, server: str) -> str:
        """校验server数据"""
        if server is None or server == "":
            raise ValidateErrorException("server不能为空且为字符串")
        return server
    
    @field_validator("paths", mode="before")
    def validate_paths(cls, paths: dict[str, dict]) -> dict[str, dict]:
        """校验paths信息，涵盖：方法提取、operationId唯一标识，parameters校验"""
        # 1. 验证paths非空且为字典
        # 2. 提取get/post方法
        # 3. 验证operationId唯一性
        # 4. 验证每个参数的格式
        # 5. 返回标准化后的数据
        ...
```

**关键特性**：

- 使用Pydantic `BaseModel` 进行数据验证
- 使用 `@field_validator` 装饰器实现自定义验证逻辑
- `validate_paths` 不仅验证数据，还会对数据进行标准化处理

### 7.2 ApiToolService.parse\_openapi\_schema()

**文件路径**：[api\_tool\_service.py](file:///home/wissfi/projects/LLMOps/llmops-api/internal/service/api_tool_service.py#L203-L212)

```python
@classmethod
def parse_openapi_schema(cls, openapi_schema_str: str) -> OpenAPISchema:
    """解析传递的openapi_schema字符串，如果出错则抛出错误"""
    try:
        data = json.loads(openapi_schema_str.strip())
        if not isinstance(data, dict):
            raise
    except Exception as e:
        raise ValidateErrorException("传递数据必须符合OpenAPI规范的JSON字符串")

    return OpenAPISchema(**data)
```

**执行流程**：

1. 去除字符串首尾空白
2. 尝试解析JSON
3. 验证解析结果为字典类型
4. 将字典传递给 `OpenAPISchema` 进行进一步验证
5. 返回验证通过的 `OpenAPISchema` 对象

### 7.3 ValidateOpenAPISchemaReq 请求表单

**文件路径**：[api\_tool\_schema.py](file:///home/wissfi/projects/LLMOps/llmops-api/internal/schema/api_tool_schema.py#L16-L20)

```python
class ValidateOpenAPISchemaReq(FlaskForm):
    """校验OpenAPI规范字符串请求"""
    openapi_schema = StringField("openapi_schema", validators=[
        DataRequired(message="openapi_schema字符串不能为空")
    ])
```

### 7.4 ParameterType 和 ParameterIn 枚举

**文件路径**：[openapi\_schema.py](file:///home/wissfi/projects/LLMOps/llmops-api/internal/core/tools/api_tools/entities/openapi_schema.py#L13-L35)

```python
class ParameterType(str, Enum):
    """参数支持的类型"""
    STR: str = "str"
    INT: str = "int"
    FLOAT: str = "float"
    BOOL: str = "bool"

class ParameterIn(str, Enum):
    """参数支持存放的位置"""
    PATH: str = "path"
    QUERY: str = "query"
    HEADER: str = "header"
    COOKIE: str = "cookie"
    REQUEST_BODY: str = "request_body"
```

***

## 8. 完整数据格式示例

### 8.1 最小有效示例

```json
{
  "description": "测试工具",
  "server": "https://api.example.com",
  "paths": {
    "/test": {
      "get": {
        "description": "测试接口",
        "operationId": "TestApi"
      }
    }
  }
}
```

### 8.2 完整示例（带参数）

```json
{
  "description": "这是一个查询对应英文单词字典的工具",
  "server": "https://dict.youdao.com",
  "paths": {
    "/suggest": {
      "get": {
        "description": "根据传递的单词查询其字典信息",
        "operationId": "YoudaoSuggest",
        "parameters": [
          {
            "name": "q",
            "in": "query",
            "description": "要检索查询的单词，例如love/computer",
            "required": true,
            "type": "str"
          },
          {
            "name": "doctype",
            "in": "query",
            "description": "返回的数据类型，支持json和xml两种格式，默认情况下json数据",
            "required": false,
            "type": "str"
          }
        ]
      }
    },
    "/translate": {
      "post": {
        "description": "翻译文本",
        "operationId": "TranslateText",
        "parameters": [
          {
            "name": "text",
            "in": "request_body",
            "description": "待翻译的文本",
            "required": true,
            "type": "str"
          },
          {
            "name": "from",
            "in": "query",
            "description": "源语言",
            "required": false,
            "type": "str"
          }
        ]
      }
    }
  }
}
```

***

## 附录

### 相关文件索引

| 文件                                                                                                                                          | 说明                |
| ------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| [api\_tool\_schema.py](file:///home/wissfi/projects/LLMOps/llmops-api/internal/schema/api_tool_schema.py)                                   | 请求/响应Schema定义     |
| [api\_tool\_service.py](file:///home/wissfi/projects/LLMOps/llmops-api/internal/service/api_tool_service.py)                                | 业务逻辑服务            |
| [openapi\_schema.py](file:///home/wissfi/projects/LLMOps/llmops-api/internal/core/tools/api_tools/entities/openapi_schema.py)               | OpenAPISchema验证模型 |
| [tool\_entity.py](file:///home/wissfi/projects/LLMOps/llmops-api/internal/core/tools/api_tools/entities/tool_entity.py)                     | 工具实体定义            |
| [api\_provider\_manager.py](file:///home/wissfi/projects/LLMOps/llmops-api/internal/core/tools/api_tools/providers/api_provider_manager.py) | API工具管理器          |

