// ============================================================
// NO ECHO · E2E 测试：文件上传流程
// 工具：Playwright
// ============================================================

import { test, expect } from "@playwright/test";

test.describe("文件上传流程", () => {
  test("首页可以正常加载", async ({ page }) => {
    await page.goto("/");
    await expect(page).toHaveTitle(/NO ECHO/);
  });

  test("上传非 DOCX 文件显示错误提示", async ({ page }) => {
    // TODO: 实现
    await page.goto("/upload");
    // ...
  });

  test("上传合法 DOCX 后跳转到进度页", async ({ page }) => {
    // TODO: 实现
  });
});
