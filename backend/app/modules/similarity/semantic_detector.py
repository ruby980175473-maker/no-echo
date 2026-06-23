# ============================================================
# NO ECHO · 语义相似度检测（洗稿风险）
# 职责：计算段落间语义向量余弦相似度，识别洗稿风险
# 技术：sentence-transformers paraphrase-multilingual-MiniLM-L12-v2
# 参考：docs/TDD/NO_ECHO_TDD_V1.0.md § 5.3
# ============================================================

from __future__ import annotations
from app.modules.parser.docx_parser import ParsedParagraph


async def detect_paraphrase_risk(
    paragraphs: list[ParsedParagraph],
    model,                           # sentence_transformers.SentenceTransformer 实例（从 app.state 注入）
    similarity_threshold: float = 0.85,
) -> list[dict]:
    """
    对段落列表进行向量编码，计算两两余弦相似度。
    相似度 > threshold 且非引用关系时，标记为 paraphrase 风险。

    注意：model.encode() 是 CPU 密集型操作，需通过 run_in_executor 在线程池执行。
    """
    # TODO: 实现
    # import asyncio
    # loop = asyncio.get_event_loop()
    # embeddings = await loop.run_in_executor(None, model.encode, texts)
    raise NotImplementedError
