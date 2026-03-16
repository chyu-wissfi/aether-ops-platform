import dotenv, os
from injector import inject
from langchain_weaviate import WeaviateVectorStore
from weaviate import WeaviateClient
import weaviate
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever



dotenv.load_dotenv()


@inject
class VectorDatabaseService:
    """
    Vector database service
    """
    client: WeaviateClient
    vector_store: WeaviateVectorStore

    def __init__(self):
        """
        完成向量数据库服务的客户端+LangChain向量数据库实例的创建
        
        Args:
            None
        
        Returns:
            None
        """
        self.client = weaviate.connect_to_local(
            host=os.getenv("WEAVIATE_HOST"),
            port=int(os.getenv("WEAVIATE_PORT")),
        )
        self.vector_store = WeaviateVectorStore(
            client=self.client,
            index_name="Dataset",
            text_key="text",
            embedding=OpenAIEmbeddings(
                model="text-embedding-3-small",
                openai_api_base=os.getenv("BASE_URL"),
                # openai_api_key=os.getenv("OPENAI_API_KEY"), 
            ),
        )

    def get_retriever(self) -> VectorStoreRetriever:
        """获取检索器"""
        return self.vector_store.as_retriever()

    @classmethod
    def combine_documents(cls, documents: list[Document]) -> str:
        """将对应的文档列表使用换行符进行合并"""
        return "\n\n".join([document.page_content for document in documents])