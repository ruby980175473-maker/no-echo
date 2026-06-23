// ============================================================
// NO ECHO · 上传页面
// 状态机：idle → uploading → success / error → (reset) → idle
// ============================================================
"use client";

import { useState } from "react";
import Link from "next/link";
import { FileDropzone } from "@/components/upload/FileDropzone";
import { UploadProgress } from "@/components/upload/UploadProgress";
import { uploadFile } from "@/lib/api/upload";

type PageStatus = "idle" | "uploading" | "success" | "error";

export default function UploadPage() {
  const [status, setStatus] = useState<PageStatus>("idle");
  const [jobId, setJobId]   = useState<string>("");
  const [errMsg, setErrMsg] = useState<string>("");

  // 用户点击「开始上传」后触发
  const handleFileSelected = async (file: File) => {
    setStatus("uploading");
    setErrMsg("");

    try {
      const result = await uploadFile(file);
      setJobId(result.job_id);
      setStatus("success");
    } catch (err) {
      const message = err instanceof Error ? err.message : "上传失败，请重试";
      setErrMsg(message);
      setStatus("error");
    }
  };

  // 重置到初始状态
  const handleReset = () => {
    setStatus("idle");
    setJobId("");
    setErrMsg("");
  };

  return (
    <main className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-6">
      {/* 返回首页 */}
      <div className="w-full max-w-xl mb-4">
        <Link
          href="/"
          className="text-sm text-gray-400 hover:text-gray-600 transition-colors"
        >
          ← 返回首页
        </Link>
      </div>

      {/* 主卡片 */}
      <div className="w-full max-w-xl bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
        {/* 标题 */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">上传论文</h1>
          <p className="text-gray-400 text-sm mt-1">
            上传你的毕业论文（.docx 格式），支持最大 20MB
          </p>
        </div>

        {/* 根据当前状态显示不同内容 */}
        {status === "idle" || status === "error" ? (
          <>
            <FileDropzone
              onFileSelected={handleFileSelected}
              disabled={false}
            />
            {status === "error" && errMsg && (
              <p className="mt-4 text-sm text-red-500">{errMsg}</p>
            )}
          </>
        ) : (
          <UploadProgress
            status={status === "uploading" ? "uploading" : status === "success" ? "success" : "error"}
            jobId={jobId}
            errorMessage={errMsg}
            onReset={handleReset}
          />
        )}

        {/* 底部说明 */}
        {status === "idle" && (
          <div className="mt-8 pt-6 border-t border-gray-100">
            <ul className="text-xs text-gray-400 space-y-1">
              <li>✓ 文件仅用于检测，24 小时后自动删除</li>
              <li>✓ 检测结果不等同于知网查重率，仅供参考</li>
              <li>✓ Sprint 1 版本：当前仅支持上传，检测功能开发中</li>
            </ul>
          </div>
        )}
      </div>
    </main>
  );
}
