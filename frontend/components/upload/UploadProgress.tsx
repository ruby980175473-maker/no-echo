// ============================================================
// NO ECHO · UploadProgress 组件
// Sprint 1: 显示上传中 / 成功 / 失败三种状态
// ============================================================
"use client";

interface UploadProgressProps {
  status: "uploading" | "success" | "error";
  jobId?: string;
  errorMessage?: string;
  onReset: () => void;
}

export function UploadProgress({ status, jobId, errorMessage, onReset }: UploadProgressProps) {
  if (status === "uploading") {
    return (
      <div className="text-center py-12">
        {/* 简单的脉冲动画 */}
        <div className="flex justify-center mb-4">
          <div className="w-10 h-10 border-4 border-gray-200 border-t-gray-800 rounded-full animate-spin" />
        </div>
        <p className="text-gray-500 text-sm">正在上传，请稍候...</p>
      </div>
    );
  }

  if (status === "success") {
    return (
      <div className="text-center py-10">
        <div className="text-5xl mb-4">✅</div>
        <h2 className="text-xl font-semibold text-gray-900 mb-2">上传成功</h2>
        <p className="text-sm text-gray-400 mb-1">文件已安全接收</p>

        {/* 任务 ID（调试用，Sprint 2+ 检测完成后用于跳转结果页） */}
        <div className="mt-4 bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 inline-block">
          <p className="text-xs text-gray-400 mb-1">任务 ID（Sprint 2+ 用于查询结果）</p>
          <p className="font-mono text-xs text-gray-600 break-all">{jobId}</p>
        </div>

        <div className="mt-6">
          <p className="text-xs text-gray-400 mb-3">
            ⏳ Sprint 2+ 将在此处显示检测进度
          </p>
          <button
            onClick={onReset}
            className="text-sm text-gray-500 underline hover:text-gray-700"
          >
            重新上传另一份论文
          </button>
        </div>
      </div>
    );
  }

  // status === "error"
  return (
    <div className="text-center py-10">
      <div className="text-5xl mb-4">❌</div>
      <h2 className="text-xl font-semibold text-gray-900 mb-2">上传失败</h2>
      <p className="text-sm text-red-500 mb-6">{errorMessage || "发生未知错误"}</p>
      <button
        onClick={onReset}
        className="bg-gray-900 text-white px-6 py-3 rounded-xl text-sm font-medium hover:bg-gray-700 transition-colors"
      >
        重试
      </button>
    </div>
  );
}
