# AI Development Skills Collection

这是一个专为 AI 辅助开发设计的技能库（Skills Repository），旨在提升 AI 在特定框架和技术栈下的编码准确性与效率。本项目汇集了 **ThinkPHP 6**、**ThinkPHP 8** 以及 **Art Design Pro** 等主流开发框架的专家级开发技能（Skill Prompts）和相关文档。

通过使用这些 Skills，AI 能够更深入地理解框架的架构、规范和最佳实践，从而生成更高质量的代码。

---

## 📂 目录结构

```
development-skills/
├── Art_Design_Pro_dev_skill/    # Art Design Pro 前端框架开发技能
│   └── Art_Design_Pro_dev_skill.md
├── thinkphp6-SKILL/             # ThinkPHP 6 后端框架开发技能
│   └── thinkphp6-SKILL.md
├── thinkphp8-SKILL/             # ThinkPHP 8 后端框架开发技能
│   └── thinkphp8-SKILL.md
├── thinkphp6_docs/              # ThinkPHP 6 官方文档（参考资料）
├── thinkphp8_docs/              # ThinkPHP 8 官方文档（参考资料）
└── README.md                    # 项目说明文件
```

---

## 🚀 可用技能 (Available Skills)

### 1. ThinkPHP 6.x 开发专家

*   **适用版本**: ThinkPHP 6.0 / 6.1 (PHP 7.2+)
*   **文件路径**: `thinkphp6-SKILL/thinkphp6-SKILL.md`
*   **功能描述**: 
    涵盖了 ThinkPHP 6 开发的全流程指南，包括：
    *   **基础**: 目录结构、命名规范、安装配置。
    *   **核心**: 路由定义、控制器编写、请求/响应处理。
    *   **数据库**: 查询构造器、模型 ORM、关联查询。
    *   **进阶**: 中间件、事件系统、依赖注入容器、多应用模式。
*   **触发场景**: 当用户进行 TP6 项目开发、代码调试或咨询架构问题时。

### 2. ThinkPHP 8.x 开发专家

*   **适用版本**: ThinkPHP 8.0+ (PHP 8.0+)
*   **文件路径**: `thinkphp8-SKILL/thinkphp8-SKILL.md`
*   **功能描述**:
    专注于 ThinkPHP 8 的现代化开发特性，强调：
    *   **现代 PHP**: 强类型声明 (`strict_types`)、PHP 8 新特性（注解、构造器提升等）。
    *   **架构升级**: 语义化版本控制、组件独立化（PSR-11/16）。
    *   **多应用**: 默认单应用与多应用模式的配置与切换。
    *   **路由增强**: 注解路由与中间件的高级用法。
*   **触发场景**: 当用户使用 TP8 开发、升级旧项目或需要利用 PHP 8 新特性时。

### 3. Art Design Pro 二次开发

*   **技术栈**: Vue 3 + TypeScript + Vite + Element Plus + Tailwind CSS
*   **文件路径**: `Art_Design_Pro_dev_skill/Art_Design_Pro_dev_skill.md`
*   **功能描述**:
    针对 Art Design Pro 企业级中后台框架的定制化开发指南：
    *   **页面开发**: 标准化的页面创建流程与布局规范。
    *   **路由配置**: 动态路由 (`asyncRoutes`) 与菜单权限控制。
    *   **核心组件**: 熟练使用框架提供的 `useTable`、`ArtSearchBar` 等 Hook 和组件。
    *   **系统对接**: 接口定义、状态管理 (Pinia) 与国际化配置。
*   **触发场景**: 当用户进行 ADP 框架的二次开发、新增业务模块或修改系统配置时。

---

## 📖 使用说明 (How to Use)

### 在 AI 编辑器中使用 (如 Trae, Cursor)

1.  **导入 Skill**:
    *   将对应框架的 `.md` 文件内容（如 `thinkphp6-SKILL.md`）复制到你的 AI 编辑器的 **System Prompt**（系统提示词）或 **Rules**（规则）设置中。
    *   或者，如果编辑器支持加载本地知识库，可以将本项目作为 Context 添加。

2.  **触发 Skill**:
    *   在与 AI 对话时，明确提及框架名称（如 "用 ThinkPHP6 写一个用户登录接口"），AI 将自动应用相应的最佳实践和规范。

3.  **参考文档**:
    *   `thinkphp6_docs/` 和 `thinkphp8_docs/` 包含了完整的官方文档内容，可作为 AI 的外部知识库（Knowledge Base）索引，以提供更精准的 API 用法查询。

---

## 🌟 维护与贡献

欢迎提交 PR 补充更多框架的 Skill Prompts 或完善现有文档。

*   **提交规范**: 请在对应的框架目录下创建或更新 Markdown 文件。
*   **文档更新**: 如果官方文档有更新，请同步更新 `_docs` 目录下的内容。
