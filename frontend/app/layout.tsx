// ============================================================
// NO ECHO · 根布局
// 不使用 Google Fonts（国内访问慢），改为系统字体
// ============================================================
import type { Metadata } from "next";
import "@/styles/globals.css";

export const metadata: Metadata = {
  title: "NO ECHO · 论文预检平台",
  description: "本科论文提交前的最后一道防线：重复风险 × AIGC风险 × 格式检查",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body style={{ fontFamily: "'PingFang SC', 'Microsoft YaHei', sans-serif" }}>
        {children}
      </body>
    </html>
  );
}
