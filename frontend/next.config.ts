import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // 将 /api/* 请求代理到后端（开发环境）
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`,
      },
    ];
  },

  // 静态文件上传大小限制
  experimental: {
    serverActions: {
      bodySizeLimit: "25mb",
    },
  },
};

export default nextConfig;
