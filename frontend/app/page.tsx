// ============================================================
// NO ECHO · 首页 Landing Page
// ============================================================
import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-8">
      <div className="text-center max-w-lg">
        {/* Logo 区域 */}
        <div className="mb-8">
          <h1 className="text-5xl font-bold text-gray-900 tracking-tight">
            NO ECHO
          </h1>
          <p className="mt-3 text-gray-500 text-lg">本科论文预检平台</p>
        </div>

        {/* 功能说明 */}
        <div className="flex justify-center gap-6 mb-10 text-sm text-gray-400">
          <span>🔁 重复风险</span>
          <span>🤖 AIGC 风险</span>
          <span>📐 格式检查</span>
        </div>

        {/* 免责说明 */}
        <p className="text-xs text-gray-400 mb-8 leading-relaxed">
          预检结果仅供参考，不等于知网查重率。<br />
          上传文件将在 24 小时后自动删除。
        </p>

        {/* 主按钮 */}
        <Link
          href="/upload"
          className="inline-block bg-gray-900 text-white px-10 py-4 rounded-2xl text-base font-semibold hover:bg-gray-700 transition-colors"
        >
          开始检测
        </Link>
      </div>
    </main>
  );
}
