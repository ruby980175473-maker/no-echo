// HTTP 客户端封装：统一 baseURL / 超时 / 错误拦截
import axios from "axios";

export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000",
  timeout: 90_000,
});

apiClient.interceptors.response.use(
  (res) => res,
  (err) => {
    // TODO: 统一 toast 错误提示
    console.error("[API Error]", err.response?.data ?? err.message);
    return Promise.reject(err);
  }
);
