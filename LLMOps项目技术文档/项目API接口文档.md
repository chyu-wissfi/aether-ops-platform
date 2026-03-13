# LLMOps 项目 API 文档

应用 API 接口统一以 JSON 格式返回，并且包含 3 个字段：`code`、`data` 和 `message`，分别代表`业务状态码`、`业务数据`和`接口附加信息`。

`业务状态码`共有 6 种，其中只有 `success(成功)` 代表业务操作成功，其他 5 种状态均代表失败，并且失败时会附加相关的信息：`fail(通用失败)`、`not_found(未找到)`、`unauthorized(未授权)`、`forbidden(无权限)`和`validate_error(数据验证失败)`。

接口示例：

```json
{
    "code": "success",
    "data": {
        "redirect_url": "https://github.com/login/oauth/authorize?client_id=f69102c6b97d90d69768&redirect_uri=http%3A%2F%2Flocalhost%3A5001%2Foauth%2Fauthorize%2Fgithub&scope=user%3Aemail"
    },
    "message": ""
}
```

带有分页数据的接口会在 `data` 内固定传递 `list` 和 `paginator` 字段，其中 `list` 代表分页后的列表数据，`paginator` 代表分页的数据。

`paginator` 内存在 4 个字段：`current_page(当前页数)` 、`page_size(每页数据条数)`、`total_page(总页数)`、`total_record(总记录条数)`，示例数据如下：

```json
{
    "code": "success",
    "data": {
        "list": [
            {
                "app_count": 0,
                "created_at": 1713105994,
                "description": "这是专门用来存储LLMOps信息的知识库",
                "document_count": 13,
                "icon": "https://wissfi-llmops-1257184990.cos.ap-guangzhou.myqcloud.com/2025/12/07/96b5e270-c54a-4424-aece-ff8a2b7e4331.png",
                "id": "c0759ca8-2d35-4480-83a8-1f41f29d1401",
                "name": "LLMOps知识库",
                "updated_at": 1713106758,
                "word_count": 8850
            }
        ],
        "paginator": {
            "current_page": 1,
            "page_size": 20,
            "total_page": 1,
            "total_record": 2
        }
    },
    "message": ""
}
```

如果接口需要授权，需要在 `headers` 中添加 `Authorization` ，并附加 `access_token` 即可完成授权登录，示例：

```json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTY0NTY3OTgsImlzcyI6ImxsbW9wcyIsInN1YiI6ImM5MDljMWRiLWIyMmUtNGZlNi04OGIyLWIyZTkxZWFiMWE3YiJ9.JDAtWDBBGiXa_XFihfopRe4Cz-RQ9_TAcno9w81tNbE
```

## 01. 应用模块

### 1.1 [todo]获取应用基础信息

- **接口说明**：传递对应的应用 id，获取当前应用的基础信息。

- **接口信息**：`授权`+`GET:/apps/:app_id`

- **接口参数**：

  - 请求参数：
    - `app_id -> uuid`：路由参数，必填，需要获取的应用 id。
  - 响应参数：
    - `id -> uuid`：应用 id，类型为 uuid。
    - `debug_conversation_id -> uuid`：调试会话 id，类型为 uuid，如果没有则为空。
    - `name -> string`：应用名称。
    - `icon -> string`：应用图标。
    - `description -> string`：应用描述。
    - `status -> string`：应用的状态，支持 `published(已发布)` 和 `draft(草稿)`。
    - `draft_updated_at -> int`：应用草稿的更新时间，类型为时间戳，单位为秒。
    - `updated_at -> int`：应用的更新时间，类型为时间戳，单位为秒。
    - `created_at -> int`：应用的创建时间，类型为时间戳，单位为秒。

- **响应示例**：

  ```json
  {
      "code": "success",
      "data": {
          "id": "5e7834dc-bbca-4ee5-9591-8f297f5acded",
          "debug_conversation_id": "46db30d1-3199-4e79-a0cd-abf12fa6858f",
          "name": "LLMOps聊天机器人",
          "icon": "https://wissfi-llmops-1257184990.cos.ap-guangzhou.myqcloud.com/2025/12/23/e4422149-4cf7-41b3-ad55-ca8d2caa8f13.png",
          "description": "这是一个LLMOps的Agent应用",
          "status": "published",
          "draft_updated_at": 1714053834,
          "updated_at": 1714053834,
          "created_at": 1714053834
      },
      "message": ""
  }
  ```

### 1.2 [todo]在个人空间下新增应用

- **接口说明**：该接口用于在个人空间下新增 Agent 应用，创建的 Agent 应用会添加一个默认的草稿配置信息，默认使用 `openai` 下的 `gpt-4o-mini` 模型，模型的默认参数为：`temperature=0.5`、`top_p=0.85`、`frequency_penalty=0.2`、`presence_penalty=0.2`、`max_tokens=8192`，该参数为相对 `平衡` 的状态。

- **接口信息**：`授权`+`POST:/apps`

- **接口参数**：

  - 请求参数：
    - `name -> str`：Agent 应用的名称，类型为字符串，长度不超过 40 个字符。
    - `icon -> str`：Agent 应用的图标 URL 地址，类型为字符串。
    - `description -> str`：可选参数，Agent 应用的描述信息，类型为字符串，长度不超过 800 个字符。
  - 响应参数：
    - `id -> uuid`：创建的 Agent 应用 id，类型为 uuid。

- **请求示例**：

  ```bash
  POST:/apps
  
  {
  	"name": "LLM应用产品经理",
  	"icon": "https://wissfi.com/2025/12/14/218e5217-ab10-4634-9681-022867955f1b.png",
  	"description": "一个能帮你解答关于LLM应用产品开发的Agent智能体。"
  }
  ```

- **响应示例**：

  ```json
  {
      "code": "success",
      "data": {
          "id": "1550b71a-1444-47ed-a59d-c2f080fbae94"
      },
      "message": "创建Agent应用成功"
  }
  ```

### 1.3 [todo]删除指定的应用

- **接口说明**：该接口用于删除指定的 Agent 智能体应用，删除之后，应用无法进行复原与调试，也无法使用开放 API 进行调试、用户无法访问该应用产生的所有会话信息等内容。

- **接口信息**：`授权`+`POST:/apps/:app_id/delete`

- **接口参数**：

  - 请求参数：
    - `app_id -> uuid`：需要删除的应用 id，类型为 uuid。

- **请求示例**：

  ```bash
  POST:/apps/1550b71a-1444-47ed-a59d-c2f080fbae94/delete
  ```

- **响应示例**：

  ```json
  {
      "code": "success",
      "data": {},
      "message": "删除Agent智能体应用成功"
  }
  ```

### 1.4 [todo]获取应用分页列表

- **接口说明**：该接口用于获取当前登录账号下创建的应用分页列表数据，该接口支持分页+搜索。

- **接口信息**：`授权`+`GET:/apps`

- **接口参数**：

  - 请求参数：
    - `current_page -> int`：可选参数，当前页数，默认为 1，类型为整型。
    - `page_size -> int`：可选参数，每页数据条数，默认为 20，范围为 10-50。
    - `search_word -> string`：可选参数，搜索词，在后端会使用应用的名称进行模糊匹配。
  - 响应参数：
    - `list -> list[dict]`：分页后的列表数据，类型为字典列表。
      - `id -> uuid`：Agent 智能体应用的 id，类型为 uuid。
      - `name -> str`：Agent 智能体应用的名字，类型为字符串。
      - `icon -> str`：Agent 智能体应用的图标，类型为字符串。
      - `description -> str`：Agent 智能体应用的描述信息，类型为字符串。
      - `preset_prompt -> str`：Agent 智能体应用的预设提示词，类型为字符串，应用如果已发布则从 `运行配置` 中获取，否则从 `草稿配置` 中获取。
      - `model_config -> dict`：Agent 智能体的模型配置，类型为字典。
        - `provider -> str`：模型提供商的名字，类型为字符串，例如：`openai`，应用如果已发布则从 `运行配置` 中获取，否则从 `草稿配置` 中获取。
        - `model -> str`：模型名字，类型为字符串，例如 `gpt-4o-mini`，应用如果已发布则从 `运行配置` 中获取，否则从 `草稿配置` 中获取。
      - `status -> str`：Agent 智能体应用的状态，支持 `published` 和 `draft`，分别代表已发布和草稿。
      - `updated_at -> int`：Agent 智能体的更新时间，类型为时间戳。
      - `created_at -> int`：Agent 智能体的创建时间，类型为时间戳。
    - `paginator -> dict`：分页器信息，类型为字典。
      - `current_page -> int`：当前页数，类型为整型。
      - `page_size -> int`：每页的条数，类型为整型。
      - `total_page -> int`：数据的总页数，类型为整型。
      - `total_record -> int`：数据的总记录条数，类型为整型。

- **请求示例**：

  ```bash
  GET:/apps?current_page=1&page_size=20&search_word=测试
  ```

- **响应示例**：

  ```json
  {
      "code": "success",
      "data": {
          "list": [
              {
                  "id": "1550b71a-1444-47ed-a59d-c2f080fbae94",
                  "name": "电商智能客服",
                  "icon": "https://wissfi.com/2025/12/14/218e5217-ab10-4634-9681-022867955f1b.png",
                  "description": "## 任务 您的主要使命是通过“DALLE”工具赋能用户，激发他们的创造力。通过询问“您希望设计传达什么信息？”或“这个设计是为了什么场合？”等问题，引导用户分享他们想要创造的设计的核心。不要询问...",
                  "preset_prompt": "",
                  "model_config": {
                      "provider": "openai",
                      "model": "gpt-4o-mini"
                  },
                  "status": "published",
                  "updated_at": "1714053834",
                  "created_at": "1714053834"
              }
          ],
          "paginator": {
              "current_page": 1,
              "page_size": 20,
              "total_page": 1,
              "total_record": 10
          }
      },
      "message": ""
  }
  ```

### 1.5 [todo]创建应用副本 API 接口

- **接口说明**：该接口用于快速复制指定 Agent 应用，涵盖 Agent 应用的基础信息、草稿配置等内容，同时在复制配置的时候，也会检测对应的草稿配置。

- **接口信息**：`授权`+`POST:/apps/:app_id/copy`

- **接口参数**：

  - 请求参数：
    - `app_id -> uuid`：需要复制的 Agent 应用 id，类型为 uuid。
  - 响应参数：
    - `id -> uuid`：拷贝后的 Agent 应用 id，类型为 uuid。

- **请求示例**：

  ```bash
  POST:/apps/1550b71a-1444-47ed-a59d-c2f080fbae94
  ```

- **响应示例**：

  ```json
  {
      "code": "success",
      "data": {
          "app_id": "46db30d1-3199-4e79-a0cd-abf12fa6858f"
      },
      "message": ""
  }
  ```

### 1.6 [todo]修改应用基础信息 API 接口

- **接口说明**：该接口用于修改指定应用的基础信息 API 接口，该接口只能修改 Agent 应用的名字、icon、描述信息。

- **接口信息**：`授权`+`POST:/apps/:app_id`

- **接口参数**：

  - 请求参数：
    - `app_id -> uuid`：路由参数，需要修改的 Agent 智能体应用 id，类型为 uuid。
    - `name -> str`：Agent 应用的名称，类型为字符串，长度不超过 40 个字符。
    - `icon -> str`：Agent 应用的图标 URL 地址，类型为字符串。
    - `description -> str`：可选参数，Agent 应用的描述信息，类型为字符串，长度不超过 800 个字符。

- **请求示例**：

  ```bash
  POST:/apps/46db30d1-3199-4e79-a0cd-abf12fa6858f
  
  {
  	"name": "LLM应用产品经理",
  	"icon": "https://wissfi.com/2025/12/14/218e5217-ab10-4634-9681-022867955f1b.png",
  	"description": "一个能帮你解答关于LLM应用产品开发的Agent智能体。"
  }
  ```

- **响应示例**：

  ```json
  {
      "code": "success",
      "data": "",
      "message": "修改Agent智能体应用成功"
  }
  ```

### 1.7 [todo]获取特定应用的草稿配置信息

- **接口说明**：该接口用于获取指定应用的配置信息，并且永远只获取草稿配置，在创建应用的时候会同步创建草稿信息，并且在应用发布亦或者更新的时候，均会同步配置信息到草稿配置中，并且每次获取草稿配置的时候，都会检测关联的 `知识库`、`工具`、`工作流` 是否存在，如果不存在，则会清除对应数据后返回。

- **接口信息**：`授权`+`GET:/apps/:app_id/draft-app-config`

- **接口参数**：

  - 请求参数：
    - `app_id -> uuid`：路由参数，应用 id，类型为 uuid。
  - 响应参数：
    - `id -> uuid`：应用配置 id，类型为 uuid。
    - `model_config -> dict`：大语言模型配置，类型为字典，存储了 LLM 相关的配置信息。
      - `provider -> str`：模型提供者名字，类型为字符串，例如 `openai`、`moonshot`，后端会根据不同的提供商名字获取不同的服务。
      - `model ->str`：模型名字，类型为字符串，例如 `gpt-4o-mini` 等。
      - `parameters -> dict`：大模型运行参数信息，每个 LLM 均有差异，一般都携带 `temperature`、`top_p`、`presence_penalty`、`frequency_penalty`、`max_tokens` 等内容。
    - `dialog_round -> int`：携带上下上下文轮数，类型为整型，最小为 0，最大为 100，设置该数值后，后端会同时计算不同 LLM 的上下文长度进行取舍。
    - `preset_prompt -> str`：人设与回复逻辑预设 prompt，类型为字符串。
    - `tools -> list[dict]`：应用绑定的工具列表，类型为字典列表。
      - `type -> str`：关联工具的类型，类型为字符串，值可能为 `builtin_tool(内置工具)` 或者 `api_tool(API工具)`。
      - `provider -> dict`：工具提供者信息，类型为字典。
        - `id -> uuid/str`：提供者标识，当类型为内置工具时，id 为名字，当为 API 工具时，id 为 uuid 标识。
        - `name -> str`：提供者名字，类型为字符串。
        - `label -> str`：提供者标签，类型为字符串，如果为 API 工具，则 label 为 name。
        - `icon -> str`：提供者对应的图标 URL 地址，类型为字符串。
        - `description -> str`：提供者描述信息，类型为字符串
      - `tool -> dict`：工具信息，类型为字典。
        - `id -> uuid`：工具 uuid，当类型为内置工具时，id 为工具名字，当为 API 工具时，id 为 uuid 标识。
        - `name -> str`：工具名字，类型为字符串。
        - `label -> str`：工具的标签，类型为字符串，如果为 API 工具，则 label 为 name。
        - `description -> str`：工具描述，类型为字符串。
        - `params -> dict`：可选参数，内置工具的 `自定义设置` 参数，用于初始化对应的工具，如果没有参数时输入为空字典即可。
    - `workflows -> list[dict]`：应用绑定的工作流列表，类型为字典列表。
      - `id -> uuid`：关联的工作流 id，类型为 uuid。
      - `name -> str`：关联的工作流名字，类型为字符串。
      - `icon -> str`：关联的工作流图标 URL，类型为字符串。
      - `description -> str`：关联的工作流描述，类型为字符串。
    - `datasets -> list[dict]`：应用关联的知识库列表，类型为字典列表，一个应用最多不能关联超过 5 个知识库。
      - `id -> uuid`：关联的知识库 id，类型为 uuid。
      - `name -> str`：关联知识库的名称，类型为字符串。
      - `icon -> str`：关联知识库的图标 URL 地址，类型为字符串。
      - `description -> str`：关联的知识库描述信息，类型为字符串。
    - `retrieval_config -> dict`：检索配置，类型为字典，记录检索策略、最大召回数量、得分阈值。
      - `retrieval_strategy -> str`：检索策略，类型为字符串，支持的值为 `full_text(全文/关键词检索)`、`semantic(向量/相似性检索)`、`hybrid(混合检索)`。
      - `k -> int`：最大召回数量，类型为整型，数据范围为 0-10，必填参数。
      - `score -> float`：最小匹配度，类型为浮点型，范围从 0-1，保留 2 位小数，数字越大表示相似度越高。
    - `long_term_memory -> dict`：长期记忆配置，类型为字典。
      - `enable -> boolean`：是否启用，类型为布尔值，true 代表启用，false 代表未启用。
    - `opening_statement -> str`：对话开场白，在初次对话时 Agent 会发送的消息，类型为字符串，最大长度不超过 2000。
    - `opening_questions -> list[str]`：对话建议问题列表，在初次对话时 Agent 会推送的建议问题，类型为字符串列表，问题数量不超过 3 个。
    - `speech_to_text -> dict`：语音输入配置，类型为字典。
      - `enable -> boolean`：是否启用语音输入，类型为布尔值，true 代表启用，false 代表未启用。
    - `text_to_speech -> dict`：语音输出配置，类型为字典。
      - `enable -> boolean`：是否启用语音输出，类型为布尔值，true 代表启用，false 代表未启用。
      - `voice -> str`：语音输出音色，数据值参考 OpenAI 提供的 TTS 接口提供的音色配置，例如：echo 等。
      - `auto_play -> boolean`：是否自动播放，类型为布尔值，true 代表自动播放，当值为 true 时，WebApp 会在生成完毕时自动调用并获取音频信息随后自动播放（流式播放）。
    - `review_config -> dict`：审核配置信息，类型为字典。
      - `enable -> boolean`：是否启用审核，类型为布尔值，true 代表启用，false 代表未启用，只有当 `enable` 为 True 时，`inputs_config` 和 `outputs_config` 开启才有意义。
      - `keywords -> list[str]`：审核关键词列表，类型为字符串列表，最多不超过 100 个关键词。
      - `inputs_config -> dict`：输入审核配置信息，类型为字典。
        - `enable -> boolean`：是否启用输入审核，类型为布尔值，true 代表启用，false 代表未启用。
        - `preset_response -> str`：触发输入敏感词时的预设回复，对于输入审核的逻辑，如果存在敏感词，则直接使用预设回复进行相应。
      - `outputs_config -> dict`：输出审核配置信息，类型为字典。
        - `enable -> boolean`：是否启用输出审核，类型为布尔值，true 代表启用，false 代表未启用，当值为 true 时，触发敏感词时，会使用 ** 代替特定的敏感词进行输出。
    - `updated_at -> int`：草稿配置的更新时间，类型为时间戳。
    - `created_at -> int`：草稿配置的创建时间，类型为时间戳。

- **请求示例**：

  ```bash
  GET:/apps/46db30d1-3199-4e79-a0cd-abf12fa6858f/draft-config
  ```

- **响应示例**：

  ```json
  {
      "code": "success",
      "data": {
          "id": "1550b71a-1444-47ed-a59d-c2f080fbae94",
          "model_config": {
              "provider": "openai",
              "model": "gpt-4o-mini",
              "parameters": {
                  "temperature": 0.5,
                  "top_p": 0.5,
                  "presence_penalty": 0.2,
                  "frequency_penalty": 0.3,
                  "max_tokens": 4500
              }
          },
          "dialog_round": 3,
          "preset_prompt": "你是一个拥有10年经验的翻译官，请帮助用户解决问题。",
          "tools": [],
          "workflows": [],
          "datasets": [
              {
                  "id": "1cbb6449-5463-49a4-b0ef-1b94cdf747d7",
                  "name": "Prompt提示词大全",
                  "icon": "https://wissfi-llmops-1304251364.cos.ap-guangzhou.myqcloud.com/2024/10/27/67c94d7b-c503-4528-87c4-1810c17689b1.jpg"
              },
              {
                  "id": "f3f28f75-8e60-4eba-b6df-4d1b390bbd89",
                  "name": "LLMOps项目",
                  "icon": "https://wissfi-llmops-1304251364.cos.ap-guangzhou.myqcloud.com/2024/09/29/9f5e42d4-e184-4e2c-88f2-0ef843749e3f.jpg"
              }
          ],
          "retrieval_config": {
              "retrieval_strategy": "semantic",
              "k": 5,
              "score": 0.5
          },
          "long_term_memory": {
              "enable": true
          },
          "opening_statement": "嘿！🎉 我是你的好朋友，Gauthmath 导师机器人。",
          "opening_questions": [
              "你能解释一下二次方程的概念吗？",
              "如何解线性方程组？",
              "求解x^2-4x+4=0"
          ],
          "speech_to_text": {
              "enable": true
          },
          "text_to_speech": {
              "enable": true,
              "voice": "echo",
              "auto_play": false
          },
          "review_config": {
              "enable": true,
              "keywords": ["敏感词", "Wissfi"],
              "inputs_config": {
                  "enable": true,
                  "preset_response": "很抱歉，该问题无法回复"
              },
              "outputs_config": {
                  "enable": true
              }
          },
          "updated_at": 1714053834,
          "created_at": 1714053834
      },
      "message": ""
  }
  ```
