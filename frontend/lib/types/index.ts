// ============================================================
// NO ECHO · 全局 TypeScript 类型定义
// 与后端 Pydantic schemas (backend/app/models/schemas.py) 保持同步
// ============================================================

export type JobStatus = "pending" | "parsing" | "checking" | "completed" | "failed";
export type RiskLevel = "high" | "medium" | "low" | "none";
export type SimilarityRiskType = "web" | "academic" | "internal" | "paraphrase";

export interface UploadResponse {
  job_id: string;
  status: JobStatus;
  message: string;
}

export interface StatusResponse {
  job_id: string;
  status: JobStatus;
  progress: {
    parsing: boolean;
    format_check: boolean;
    similarity: boolean;
    aigc: boolean;
  };
  estimated_seconds_remaining?: number;
}

export interface RiskSummaryCard {
  risk_level: RiskLevel;
  risk_star: number;
  affected_paragraphs?: number;
  issue_count?: number;
  description: string;
}

export interface SummaryResponse {
  job_id: string;
  file_name: string;
  completed_at: string;
  summary: {
    similarity: RiskSummaryCard;
    aigc: RiskSummaryCard;
    format: RiskSummaryCard;
  };
}

export interface SimilarityRisk {
  risk_level: RiskLevel;
  risk_type: SimilarityRiskType;
  source_url?: string;
  source_title?: string;
  matched_text?: string;
  similarity_score?: number;
  suggestion?: string;
}

export interface AigcRisk {
  risk_level: RiskLevel;
  ai_probability: number;
  sentence_details?: Array<{ text: string; probability: number }>;
}

export interface ParagraphResult {
  id: string;
  index: number;
  text: string;
  heading_level: number | null;
  risks: {
    similarity?: SimilarityRisk;
    aigc?: AigcRisk;
  };
}

export interface FormatIssue {
  section: string;
  issue_type: string;
  description: string;
  expected?: string;
  actual?: string;
  paragraph_index?: number;
}

export interface DetailResponse {
  job_id: string;
  paragraphs: ParagraphResult[];
  format_issues: FormatIssue[];
}
