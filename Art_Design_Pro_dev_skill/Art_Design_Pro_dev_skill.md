---
name: art-design-pro
description: 专为 Art Design Pro（ADP）企业级中后台 UI 框架的二次开发和代码更新而设计的技能。当用户提到 Art Design Pro、ADP、artd.pro、基于该框架新增页面/模块/路由/菜单、修改主题配置、对接后端接口、添加权限控制、使用 useTable/ArtSearchBar 组件，或需要同步/升级 ADP 框架代码时，必须使用此技能。即使用户只是说"帮我加一个管理页面"、"新增一个路由"或"对接接口"而没有明确提到 ADP，只要项目使用了该框架，也应使用此技能。
---

# Art Design Pro 二次开发技能

Art Design Pro（ADP）是基于 Vue 3 + TypeScript + Vite + Element Plus + Tailwind CSS 的企业级中后台框架。本技能指导 AI 在该框架上进行准确、规范的二次开发。

**官方文档**：https://www.artd.pro/docs/zh/guide/introduce.html  
**技术栈**：Vue 3 · TypeScript · Vite · Element Plus · Tailwind CSS · Sass · Pinia · Vue Router 4

---

## 核心项目结构速查

```
src/
├── api/                    # 接口定义（auth.ts, system-manage.ts ...）
├── assets/styles/          # 样式（core=系统级, custom=业务级）
├── components/
│   ├── business/           # 业务组件（项目专属）
│   └── core/               # 框架核心组件（不要随意修改）
├── config/setting.ts       # 系统全局配置
├── directives/             # 自定义指令（v-auth, v-roles）
├── hooks/core/             # 核心 Composable（useTable, useTheme...）
├── locales/langs/          # 国际化（en.json, zh.json）
├── router/
│   ├── routes/asyncRoutes.ts   # 动态路由（业务菜单）⭐
│   └── routes/staticRoutes.ts  # 静态路由（登录/404等）
├── store/modules/          # Pinia 状态（user, menu, setting...）
├── types/                  # TypeScript 类型定义
├── utils/                  # 工具函数（http, storage, form...）
└── views/                  # 页面组件（按模块组织）
```

---

## 任务一：新增业务页面（完整流程）

### Step 1 - 创建页面文件

在 `src/views/` 下按模块创建，使用 `page-content` 类名撑满屏幕高度：

```vue
<!-- src/views/[模块名]/[页面名]/index.vue -->
<template>
  <div class="page-content">
    <!-- 页面内容 -->
  </div>
</template>

<script setup lang="ts">
// 页面逻辑
</script>
```

> ⚠️ `class="page-content"` 是框架约定，会自动将最小高度撑满屏幕剩余高度，必须加。

### Step 2 - 注册路由（asyncRoutes.ts）

编辑 `src/router/routes/asyncRoutes.ts`：

```typescript
// 一级菜单
export const asyncRoutes: MenuListType[] = [
  {
    path: '/product/list',
    name: 'ProductList',
    component: '/product/list',   // 对应 src/views/product/list/index.vue
    meta: {
      title: 'menus.product.list',  // i18n key
      icon: 'ri:shopping-bag-line',  // Remix Icon 图标
      keepAlive: true,
    },
  },
];

// 多级菜单（父路由 component 固定为 '/index/index'）
export const asyncRoutes: MenuListType[] = [
  {
    name: 'Product',
    path: '/product',
    component: '/index/index',   // 固定值，代表布局容器
    meta: {
      title: 'menus.product.title',
      icon: 'ri:store-line',
    },
    children: [
      {
        path: 'list',
        name: 'ProductList',
        component: '/product/list',
        meta: {
          title: 'menus.product.list',
          keepAlive: true,
          roles: ['R_SUPER', 'R_ADMIN'],  // 可选：角色权限控制
        },
      },
    ],
  },
];
```

### Step 3 - 添加 i18n 翻译

同步更新两个语言文件：

```json
// src/locales/langs/zh.json
{
  "menus": {
    "product": {
      "title": "商品管理",
      "list": "商品列表"
    }
  }
}

// src/locales/langs/en.json
{
  "menus": {
    "product": {
      "title": "Product",
      "list": "Product List"
    }
  }
}
```

---

## 任务二：标准 CRUD 列表页模板

这是 ADP 项目中最常见的页面模式，使用 `useTable` + `ArtSearchBar` + `ArtTable`：

```vue
<template>
  <div class="page-content">
    <!-- 搜索栏 -->
    <ArtSearchBar
      v-model="searchForm"
      :items="searchItems"
      @search="handleSearch"
      @reset="handleReset"
    />

    <!-- 操作栏 -->
    <div class="flex justify-between mb-3">
      <div class="flex gap-2">
        <ElButton type="primary" @click="handleAdd">
          <i class="ri-add-line mr-1" /> 新增
        </ElButton>
      </div>
    </div>

    <!-- 数据表格 -->
    <ArtTable
      :loading="loading"
      :data="data"
      :columns="columns"
      :pagination="pagination"
      @pagination:size-change="handleSizeChange"
      @pagination:current-change="handleCurrentChange"
    >
      <!-- 自定义列插槽示例 -->
      <template #status="{ row }">
        <ElTag :type="row.status === 1 ? 'success' : 'danger'">
          {{ row.status === 1 ? '启用' : '禁用' }}
        </ElTag>
      </template>
      <template #action="{ row }">
        <ElButton v-auth="'edit'" text type="primary" @click="handleEdit(row)">编辑</ElButton>
        <ElButton v-auth="'delete'" text type="danger" @click="handleDelete(row)">删除</ElButton>
      </template>
    </ArtTable>

    <!-- 新增/编辑弹窗 -->
    <ElDialog v-model="dialogVisible" :title="isEdit ? '编辑' : '新增'" width="500px">
      <!-- 表单内容 -->
      <template #footer>
        <ElButton @click="dialogVisible = false">取消</ElButton>
        <ElButton type="primary" @click="handleSubmit">确定</ElButton>
      </template>
    </ElDialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useTable } from '@/hooks'
import { fetchGetXxxList, fetchAddXxx, fetchUpdateXxx, fetchDeleteXxx } from '@/api/xxx'
import { ElMessage, ElMessageBox } from 'element-plus'

// ---- 搜索表单 ----
const searchForm = ref({ name: '', status: '' })

const searchItems = [
  { label: '名称', key: 'name', type: 'input', placeholder: '请输入名称' },
  {
    label: '状态', key: 'status', type: 'select',
    props: { options: [{ label: '启用', value: 1 }, { label: '禁用', value: 0 }] },
  },
]

// ---- useTable 核心 ----
const {
  data, loading, pagination,
  handleSizeChange, handleCurrentChange,
  searchParams, getData,
  refreshCreate, refreshUpdate, refreshRemove,
} = useTable({
  core: {
    apiFn: fetchGetXxxList,
    apiParams: { current: 1, size: 20, name: '', status: '' },
    columnsFactory: () => [
      { prop: 'id', label: 'ID', width: 80 },
      { prop: 'name', label: '名称' },
      { prop: 'status', label: '状态', useSlot: true },  // useSlot: true 启用插槽
      { prop: 'createTime', label: '创建时间', width: 180 },
      { prop: 'action', label: '操作', width: 160, fixed: 'right', useSlot: true },
    ],
  },
})

// ---- 搜索 / 重置 ----
const handleSearch = () => {
  Object.assign(searchParams, searchForm.value)
  getData()
}
const handleReset = () => {
  searchForm.value = { name: '', status: '' }
  Object.assign(searchParams, { name: '', status: '' })
  getData()
}

// ---- 新增 / 编辑 ----
const dialogVisible = ref(false)
const isEdit = ref(false)
const formData = reactive({ id: '', name: '', status: 1 })

const handleAdd = () => {
  isEdit.value = false
  Object.assign(formData, { id: '', name: '', status: 1 })
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  isEdit.value = true
  Object.assign(formData, row)
  dialogVisible.value = true
}

const handleSubmit = async () => {
  const api = isEdit.value ? fetchUpdateXxx : fetchAddXxx
  await api(formData)
  ElMessage.success(isEdit.value ? '编辑成功' : '新增成功')
  dialogVisible.value = false
  isEdit.value ? refreshUpdate() : refreshCreate()
}

// ---- 删除 ----
const handleDelete = async (row: any) => {
  await ElMessageBox.confirm(`确认删除「${row.name}」吗？`, '提示', { type: 'warning' })
  await fetchDeleteXxx(row.id)
  ElMessage.success('删除成功')
  refreshRemove()
}
</script>
```

---

## 任务三：API 接口定义规范

在 `src/api/` 下创建对应模块文件：

```typescript
// src/api/product.ts
import { http } from '@/utils/http'

/** 查询列表 */
export const fetchGetProductList = (params: ProductListParams) => {
  return http.get<PageResult<ProductItem>>('/api/product/list', params)
}

/** 新增 */
export const fetchAddProduct = (data: ProductForm) => {
  return http.post('/api/product/add', data)
}

/** 编辑 */
export const fetchUpdateProduct = (data: ProductForm) => {
  return http.put('/api/product/update', data)
}

/** 删除 */
export const fetchDeleteProduct = (id: string) => {
  return http.delete(`/api/product/delete/${id}`)
}
```

类型定义放到 `src/types/api/api.d.ts` 或新建对应模块 `.d.ts`：

```typescript
// 分页响应通用类型（框架已内置）
interface PageResult<T> {
  records: T[]
  total: number
  current: number
  size: number
}
```

---

## 任务四：权限控制

### 路由级权限（角色控制）

```typescript
// asyncRoutes.ts 中配置 roles
meta: {
  roles: ['R_SUPER', 'R_ADMIN']  // 只有这两个角色能访问此路由
}
```

### 按钮级权限（两种方式）

**方式 1：v-auth 指令（推荐，后端模式）**

先在路由 meta 中定义 authList：
```typescript
meta: {
  authList: [
    { title: '新增', authMark: 'add' },
    { title: '编辑', authMark: 'edit' },
    { title: '删除', authMark: 'delete' },
  ]
}
```

然后在模板中使用：
```vue
<ElButton v-auth="'add'">新增</ElButton>
<ElButton v-auth="'edit'">编辑</ElButton>
<ElButton v-auth="'delete'">删除</ElButton>
```

**方式 2：hasAuth 函数（前端模式）**
```vue
<script setup lang="ts">
import { useAuth } from '@/composables/useAuth'
const { hasAuth } = useAuth()
</script>

<template>
  <ElButton v-if="hasAuth('add')">新增</ElButton>
</template>
```

**方式 3：v-roles 指令（基于角色）**
```vue
<ElButton v-roles="['R_SUPER', 'R_ADMIN']">超级管理员按钮</ElButton>
```

### 权限模式切换

```env
# .env 文件
VITE_ACCESS_MODE=frontend   # 前端控制（角色匹配路由 roles 字段）
VITE_ACCESS_MODE=backend    # 后端控制（后端返回菜单列表动态注册路由）
```

---

## 任务五：useTable 高级用法速查

### 配置选项全览

```typescript
const tableState = useTable<RowType>({
  // 核心（必填）
  core: {
    apiFn: fetchXxxList,          // API 函数
    apiParams: { current: 1, size: 20 },  // 默认参数
    immediate: true,              // 是否立即请求（默认 true）
    columnsFactory: () => [],     // 列配置工厂
    excludeParams: ['daterange'], // 不传给接口的参数字段
    paginationKey: { current: 'pageNum', size: 'pageSize' },  // 字段映射（非标准分页时使用）
  },
  // 数据转换（可选）
  transform: {
    dataTransformer: (records) => records.map(item => ({ ...item, fullName: item.firstName + item.lastName })),
    responseAdapter: (res) => ({ records: res.list, total: res.totalCount, current: res.pageNum, size: res.pageSize }),
  },
  // 性能（可选）
  performance: {
    enableCache: true,
    cacheTime: 5 * 60 * 1000,
    debounceTime: 300,
    maxCacheSize: 100,
  },
  // 钩子（可选）
  hooks: {
    onSuccess: (data) => console.log('成功', data.length),
    onError: (err) => ElMessage.error(err.message),
    onCacheHit: (data) => console.log('缓存命中'),
  },
})
```

### 刷新策略选择

| 操作 | 调用方法 | 效果 |
|------|----------|------|
| 点击刷新按钮 | `refreshData()` | 清空所有缓存，回第一页 |
| 新增数据后 | `refreshCreate()` | 回第一页，清分页缓存 |
| 编辑数据后 | `refreshUpdate()` | 保持当前页刷新 |
| 删除数据后 | `refreshRemove()` | 智能处理页码（末页自动回退） |
| 定时刷新 | `refreshSoft()` | 只清当前搜索条件缓存 |

---

## 任务六：ArtSearchBar 搜索栏

### 所有支持的 type 类型

| type 值 | 控件 |
|---------|------|
| `input` | 文本输入框 |
| `number` | 数字输入框 |
| `select` | 下拉选择 |
| `cascader` | 级联选择器 |
| `treeselect` | 树选择器 |
| `datetime` | 日期/时间选择（通过 props.type 细化） |
| `timepicker` | 时间选择器 |
| `switch` | 开关 |
| `radiogroup` | 单选框组 |
| `checkboxgroup` | 复选框组 |
| `rate` | 评分 |
| `slider` | 滑块 |
| `() => h(组件)` | 自定义渲染函数 |

### 日期范围示例

```typescript
{
  label: '时间范围',
  key: 'dateRange',
  type: 'datetime',
  props: {
    type: 'daterange',
    rangeSeparator: '至',
    startPlaceholder: '开始日期',
    endPlaceholder: '结束日期',
    valueFormat: 'YYYY-MM-DD',
  },
}
```

### Props 完整参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `v-model` | `Record<string, any>` | `{}` | 表单数据 |
| `items` | `SearchFormItem[]` | `[]` | 表单项配置 |
| `span` | `number` | `6` | 每项占栅格数（24格制） |
| `gutter` | `number` | `12` | 栅格间距 |
| `labelWidth` | `string/number` | `'70px'` | 标签宽度 |
| `labelPosition` | `'left'/'right'/'top'` | `'right'` | 标签位置 |
| `defaultExpanded` | `boolean` | `false` | 默认展开 |
| `showExpand` | `boolean` | `true` | 显示展开按钮 |

---

## 任务七：主题和样式规范

### CSS 变量命名（框架内置）

```scss
// 主色调（跟随 Element Plus 主题）
var(--el-color-primary)
var(--el-color-primary-light-3)

// 背景色
var(--art-bg-color)
var(--art-main-bg-color)

// 文字色
var(--art-text-gray-100)   // 主要文字
var(--art-text-gray-600)   // 次要文字
```

### 自定义样式位置

```
src/assets/styles/
├── core/      # ⛔ 不要修改，框架核心样式
└── custom/    # ✅ 这里放业务自定义样式
```

### Tailwind 使用

直接在模板中使用 Tailwind 工具类，框架已集成：

```vue
<div class="flex items-center gap-4 px-4 py-2 rounded-lg shadow-sm">
  <span class="text-sm text-gray-500">标签</span>
</div>
```

---

## 任务八：iframe 内嵌外部页面

```typescript
// asyncRoutes.ts
{
  path: '/outside/iframe/vue-docs',
  name: 'VueDocs',
  component: '',   // 留空
  meta: {
    title: 'Vue 文档',
    isIframe: true,
    link: 'https://cn.vuejs.org/',
    keepAlive: false,
  }
}
```

---

## 任务九：国际化多语言

### 在页面中使用

```vue
<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>

<template>
  <span>{{ t('menus.product.title') }}</span>
  <ElButton>{{ t('common.confirm') }}</ElButton>
</template>
```

### 语言文件结构建议

```json
{
  "menus": { "模块名": { "子菜单": "显示名" } },
  "common": { "confirm": "确认", "cancel": "取消", "search": "搜索", "reset": "重置", "add": "新增", "edit": "编辑", "delete": "删除" },
  "msg": { "success": "操作成功", "deleteConfirm": "确认删除吗？" }
}
```

---

## 任务十：框架代码同步更新

当需要将项目代码与上游 Art Design Pro 最新版本同步时：

### 官方同步方式（Git）

```bash
# 1. 添加上游远程仓库（首次）
git remote add upstream https://github.com/Daymychen/art-design-pro.git

# 2. 拉取上游更新
git fetch upstream

# 3. 合并到当前分支（推荐 rebase 保持提交历史整洁）
git rebase upstream/main

# 4. 解决冲突后继续
git add .
git rebase --continue
```

### 冲突处理原则

| 文件/目录 | 冲突策略 |
|-----------|----------|
| `src/components/core/` | 优先使用上游版本（框架核心） |
| `src/hooks/core/` | 优先使用上游版本 |
| `src/assets/styles/core/` | 优先使用上游版本 |
| `src/assets/styles/custom/` | 保留本地版本（业务样式） |
| `src/views/` | 保留本地版本（业务页面） |
| `src/api/` | 保留本地版本（业务接口） |
| `src/router/routes/asyncRoutes.ts` | 手动合并（重要！） |
| `src/config/setting.ts` | 手动合并（检查新增配置项） |
| `vite.config.ts` | 手动合并 |
| `package.json` | 手动合并，之后运行 `npm install` |

### 更新检查清单

更新后必须验证：
- [ ] `npm install`（依赖是否有变更）
- [ ] `npm run dev` 是否正常启动
- [ ] 路由/菜单是否正常加载
- [ ] 主题切换是否正常
- [ ] 自定义业务页面是否受影响
- [ ] 检查 `CHANGELOG` 了解破坏性变更

---

## 常见问题与注意事项

### ❌ 常见错误

```typescript
// ❌ 错误：多级路由父级 component 写成实际组件
{
  path: '/system',
  component: '/system/index',   // 错误
}

// ✅ 正确：父级固定用布局容器
{
  path: '/system',
  component: '/index/index',    // 正确
}
```

```typescript
// ❌ 错误：静态路由和动态路由同时配置同一路径
// 会导致路由重复注册

// ✅ 正确：动态路由会自动注册，静态路由中删除重复项
```

### ✅ 最佳实践

1. **业务代码只放在指定目录**：`src/views/`、`src/api/`、`src/assets/styles/custom/`、`src/components/business/`
2. **不直接修改 `core/` 目录下的任何文件**，需要扩展时在 `business/` 下创建新组件
3. **路由 name 全局唯一**，使用 PascalCase 命名（如 `ProductList`）
4. **组件名与路由 name 保持一致**，方便 keepAlive 缓存生效
5. **useTable 的 columnsFactory 中**，需要插槽渲染的列必须加 `useSlot: true`
6. **删除操作必须有 ElMessageBox 二次确认**，然后调用 `refreshRemove()`
7. **新增/编辑成功后** 分别调用 `refreshCreate()` / `refreshUpdate()`，不要直接调用 `getData()`

### 路由 meta 字段速查

| 字段 | 类型 | 说明 |
|------|------|------|
| `title` | string | 菜单标题（支持 i18n key） |
| `icon` | string | Remix Icon 图标名 |
| `keepAlive` | boolean | 页面缓存 |
| `isHide` | boolean | 在菜单中隐藏 |
| `isHideTab` | boolean | 在标签页中隐藏 |
| `roles` | string[] | 角色权限白名单 |
| `authList` | Array | 按钮权限列表 |
| `fixedTab` | boolean | 固定标签页（不可关闭） |
| `isFullPage` | boolean | 全屏页面（不显示侧边栏） |
| `isIframe` | boolean | iframe 内嵌页 |
| `link` | string | iframe 目标 URL |
| `activePath` | string | 手动指定高亮的菜单路径 |

---

## 快速命令参考

```bash
# 开发
npm run dev

# 构建
npm run build

# 一键清理演示数据（获取干净项目基础）
npm run clean

# 代码检查
npm run lint

# 格式化
npm run format
```