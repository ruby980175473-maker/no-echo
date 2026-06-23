import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // NO ECHO 风险颜色系统（与 ADR 风险等级定义对应）
        risk: {
          high:   "#EF4444",  // 红色
          medium: "#F97316",  // 橙色
          low:    "#EAB308",  // 黄色
          none:   "#22C55E",  // 绿色
        },
      },
    },
  },
  plugins: [],
};

export default config;
