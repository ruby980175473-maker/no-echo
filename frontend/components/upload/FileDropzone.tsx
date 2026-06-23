// ============================================================
// NO ECHO · FileDropzone 组件
// 功能：文件拖拽 / 点击选择 → 显示文件名 → 触发上传回调
// Sprint 1: 只支持 .docx，其他格式在前端直接提示
// ============================================================
"use client";

import { useRef, useState, DragEvent, ChangeEvent } from "react";

interface FileDropzoneProps {
  onFileSelected: (file: File) => void;
  disabled?: boolean;
}

export function FileDropzone({ onFileSelected, disabled = false }: FileDropzoneProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [clientError, setClientError] = useState<string>("");

  // 统一的文件处理入口
  const handleFile = (file: File) => {
    setClientError("");

    // 前端格式校验（避免用户拖错文件）
    if (!file.name.toLowerCase().endsWith(".docx")) {
      setClientError("请选择 .docx 格式的文件（Word 2007 及以上版本保存的格式）");
      setSelectedFile(null);
      return;
    }

    // 前端大小预校验（20MB）
    if (file.size > 20 * 1024 * 1024) {
      setClientError(`文件太大（${(file.size / 1024 / 1024).toFixed(1)}MB），最大支持 20MB`);
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
    // 重置 input，允许重复选择同一文件
    e.target.value = "";
  };

  const handleUploadClick = () => {
    if (selectedFile) onFileSelected(selectedFile);
  };

  return (
    <div>
      {/* 拖拽 / 点击区域 */}
      <div
        onClick={() => !disabled && inputRef.current?.click()}
        onDrop={handleDrop}
        onDragOver={(e) => { e.preventDefault(); if (!disabled) setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        className={[
          "border-2 border-dashed rounded-2xl p-10 text-center transition-colors",
          disabled
            ? "opacity-50 cursor-not-allowed bg-gray-50"
            : "cursor-pointer",
          isDragging
            ? "border-blue-400 bg-blue-50"
            : selectedFile
            ? "border-green-400 bg-green-50"
            : "border-gray-300 hover:border-gray-400 bg-white",
        ].join(" ")}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".docx"
          className="hidden"
          onChange={handleChange}
          disabled={disabled}
        />

        {selectedFile ? (
          // 已选择文件：显示文件信息
          <div>
            <div className="text-3xl mb-2">📄</div>
            <div className="font-medium text-gray-800 break-all">{selectedFile.name}</div>
            <div className="text-sm text-gray-400 mt-1">
              {(selectedFile.size / 1024).toFixed(0)} KB
            </div>
            {!disabled && (
              <div className="text-xs text-gray-400 mt-3">点击更换文件</div>
            )}
          </div>
        ) : (
          // 未选择文件：显示引导文字
          <div>
            <div className="text-4xl mb-3">📂</div>
            <div className="font-medium text-gray-600">点击选择文件，或拖拽到此处</div>
            <div className="text-sm text-gray-400 mt-2">.docx 格式 · 最大 20MB</div>
          </div>
        )}
      </div>

      {/* 前端校验错误提示 */}
      {clientError && (
        <p className="mt-3 text-sm text-red-500">{clientError}</p>
      )}

      {/* 上传按钮（仅在文件选择后显示） */}
      {selectedFile && !disabled && (
        <button
          onClick={handleUploadClick}
          className="mt-4 w-full bg-gray-900 text-white rounded-2xl py-4 font-semibold text-base hover:bg-gray-700 transition-colors"
        >
          开始上传
        </button>
      )}
    </div>
  );
}
