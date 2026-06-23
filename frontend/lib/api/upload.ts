// ============================================================
// NO ECHO · 上传 API 调用
// Sprint 1: 直接 fetch /api/upload（Next.js 代理到后端 8000 端口）
// ============================================================

import type { UploadResponse } from "@/lib/types";

/**
 * 上传论文 DOCX 文件
 *
 * @param file       用户选择的 .docx 文件
 * @param template   可选的格式模板文件（Sprint 1 暂不处理）
 * @returns          UploadResponse（含 job_id 和上传状态）
 * @throws           Error（含后端返回的中文错误信息）
 */
export async function uploadFile(
  file: File,
  template?: File,
): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  if (template) {
    formData.append("template", template);
  }

  // 注意：不要手动设置 Content-Type，让浏览器自动设置 multipart/form-data boundary
  const response = await fetch("/api/upload", {
    method: "POST",
    body: formData,
  });

  // 解析响应
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    // 优先使用后端返回的中文错误信息
    const detail = (data as { detail?: string }).detail;
    throw new Error(detail ?? `上传失败（HTTP ${response.status}），请重试`);
  }

  return data as UploadResponse;
}
