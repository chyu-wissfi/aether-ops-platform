# LangChain 版本回退报告

## 操作时间
2026-03-14

## 操作概述
将langchain从1.0.8版本降级至0.3.28版本

## 版本变更详情

### 核心包变更

| 包名 | 变更前版本 | 变更后版本 | 变更类型 |
|------|-----------|-----------|---------|
| langchain | 1.0.8 | 0.3.28 | 降级 |
| langchain-core | 1.0.7 | 0.3.83 | 降级 |
| langchain-text-splitters | 1.0.0 | 0.3.11 | 降级 |
| langchain-openai | 1.0.3 | 0.3.35 | 降级 |
| langgraph | 1.0.10 | 0.3.34 | 降级 |
| langgraph-checkpoint | 4.0.1 | 2.0.21 | 降级 |
| langgraph-checkpoint-postgres | 3.0.4 | 2.0.21 | 降级 |
| langgraph-prebuilt | 1.0.8 | 0.1.8 | 降级 |
| langgraph-sdk | 0.3.9 | 0.1.66 | 降级 |

### 未变更包

| 包名 | 版本 |
|------|------|
| langchain-community | 0.3.31 |
| langchain-postgres | 0.0.17 |
| pydantic | 2.12.5 |
| pydantic-settings | 2.13.1 |
| pydantic_core | 2.41.5 |

## 功能测试结果

| 测试项 | 结果 |
|-------|------|
| 基础导入 | ✓ 通过 |
| 提示词构建 | ✓ 通过 |
| 聊天提示词构建 | ✓ 通过 |
| 输出解析器 | ✓ 通过 |
| FakeListLLM模型 | ✓ 通过 |
| 简单链执行 | ✓ 通过 |
| ChatOpenAI接口 | ✗ 失败 (未设置API Key，预期行为) |

## 回滚方法

如需回滚到原版本，执行以下命令：

```bash
conda activate LLMOps
pip install langchain==1.0.8 langchain-core==1.0.7 langchain-text-splitters==1.0.0 \
    langchain-openai==1.0.3 langgraph==1.0.10 langgraph-checkpoint==4.0.1 \
    langgraph-checkpoint-postgres==3.0.4 langgraph-prebuilt==1.0.8 langgraph-sdk==0.3.9
```

## 备份文件位置

- 降级前依赖版本: /tmp/langchain_before_downgrade.txt
- 降级后依赖版本: /tmp/langchain_after_downgrade.txt
