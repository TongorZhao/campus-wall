---
name: Campus Wall
description: 校园匿名/公开论坛系统
colors:
  primary: "#4361ee"
  primary-deep: "#3f37c9"
  accent: "#4895ef"
  neutral-bg: "#f0f2f5"
  neutral-surface: "#ffffff"
  neutral-text: "#212529"
  neutral-muted: "#6c757d"
  neutral-border: "#dee2e6"
  danger: "#dc3545"
  warning: "#ffc107"
typography:
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans SC', sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.5
  display:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans SC', sans-serif"
    fontSize: "clamp(1.5rem, 3vw, 2rem)"
    fontWeight: 700
    lineHeight: 1.2
rounded:
  sm: "4px"
  md: "8px"
  lg: "12px"
spacing:
  sm: "8px"
  md: "16px"
  lg: "24px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#ffffff"
    rounded: "{rounded.sm}"
    padding: "8px 16px"
  button-primary-hover:
    backgroundColor: "{colors.primary-deep}"
    textColor: "#ffffff"
  card:
    backgroundColor: "{colors.neutral-surface}"
    rounded: "{rounded.lg}"
    padding: "16px"
---

# Design System: Campus Wall

## 1. Overview

**Creative North Star: "The Campus Hub"**

校园墙是一个现代化的校园交流平台，设计风格简约专业，强调信息的清晰展示和高效的用户交互。系统拒绝传统BBS论坛的功能堆砌和视觉混乱，追求干净、现代、高效的界面体验。

**Key Characteristics:**
- 简约不简单：界面干净但功能完整
- 信息优先：内容展示清晰，操作便捷
- 移动友好：适配手机端使用场景
- 一致性：统一的视觉语言和交互模式

## 2. Colors

调色板以蓝色为主色调，搭配中性灰色系，营造专业、可信赖的视觉感受。

### Primary
- **Campus Blue** (#4361ee): 主要品牌色，用于导航栏、按钮、链接等核心交互元素
- **Deep Blue** (#3f37c9): 主色的深色变体，用于悬停状态和强调

### Accent
- **Light Blue** (#4895ef): 辅助强调色，用于次级按钮、标签和装饰性元素

### Neutral
- **Background Gray** (#f0f2f5): 页面背景色，营造清爽的视觉基础
- **Surface White** (#ffffff): 卡片、模态框等容器的背景色
- **Text Dark** (#212529): 主要文本颜色，确保最佳可读性
- **Text Muted** (#6c757d): 辅助文本、时间戳等次要信息
- **Border Gray** (#dee2e6): 分隔线和边框

### Semantic
- **Danger Red** (#dc3545): 错误状态、删除操作、置顶标签
- **Warning Yellow** (#ffc107): 警告状态、收藏按钮

### Named Rules
**The One Accent Rule.** 主蓝色仅用于核心交互元素（导航、主按钮、链接），不超过屏幕面积的10%。稀释其使用频率以保持视觉焦点。

## 3. Typography

**Display Font:** System Stack (-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans SC', sans-serif)
**Body Font:** System Stack (同上)

**Character:** 系统字体栈确保跨平台一致性和最佳可读性，中文使用Noto Sans SC作为后备字体。

### Hierarchy
- **Display** (700, clamp(1.5rem, 3vw, 2rem), 1.2): 页面标题、帖子标题
- **Headline** (600, 1.25rem, 1.3): 卡片标题、区块标题
- **Title** (600, 1rem, 1.4): 列表项标题、按钮文本
- **Body** (400, 1rem, 1.5): 正文内容、描述文本，最大行宽65-75ch
- **Label** (500, 0.875rem, 0.5px): 按钮、标签、表单标签

### Named Rules
**The Readability Rule.** 正文文本必须达到4.5:1以上的对比度，确保在各种光照条件下清晰可读。

## 4. Elevation

系统采用混合层次策略：默认平面设计，通过微妙的阴影变化传达交互状态。

### Shadow Vocabulary
- **Subtle Shadow** (`box-shadow: 0 2px 4px rgba(0,0,0,0.1)`): 导航栏、卡片默认状态
- **Hover Shadow** (`box-shadow: 0 4px 12px rgba(0,0,0,0.1)`): 卡片悬停状态
- **Modal Shadow** (`box-shadow: 0 4px 24px rgba(0,0,0,0.15)`): 模态框、下拉菜单

### Named Rules
**The Flat-By-Default Rule.** 所有表面默认平面状态，仅在交互状态（悬停、聚焦、激活）时显示阴影，保持界面清爽。

## 5. Components

### Buttons
- **Shape:** 圆角4px (rounded-sm)
- **Primary:** 蓝色背景(#4361ee)，白色文本，内边距8px 16px
- **Hover / Focus:** 深蓝色背景(#3f37c9)，平滑过渡0.2s
- **Secondary / Ghost:** 边框样式，悬停时填充浅色背景

### Cards
- **Corner Style:** 圆角12px (rounded-lg)
- **Background:** 白色(#ffffff)
- **Shadow Strategy:** 默认无阴影，悬停时显示微妙阴影
- **Border:** 无边框
- **Internal Padding:** 16px

### Inputs / Fields
- **Style:** 浅灰色边框，白色背景，圆角4px
- **Focus:** 蓝色边框(#4895ef)，微妙的外发光效果
- **Error:** 红色边框，错误提示文本

### Navigation
- **Style:** 深蓝色背景，白色文字，固定在顶部
- **Typography:** 品牌名称加粗，导航链接常规字重
- **Default/Hover/Active:** 悬停时透明度变化，激活状态高亮

### Chips / Tags
- **Style:** 浅色背景(#f8f9fa)，深色文本，圆角4px
- **State:** 悬停时加深背景色

## 6. Do's and Don'ts

### Do:
- **Do** 使用系统字体栈确保跨平台一致性
- **Do** 保持卡片设计简洁，无边框，仅通过阴影传达层次
- **Do** 使用蓝色作为主要交互色，保持视觉一致性
- **Do** 确保文本对比度达到WCAG AA标准（4.5:1）
- **Do** 在移动设备上优化触摸目标尺寸（至少44px）

### Don't:
- **Don't** 使用传统BBS论坛的复杂布局和功能堆砌
- **Don't** 在卡片上使用左边框或右边框作为装饰
- **Don't** 使用渐变文本或玻璃拟态效果
- **Don't** 在页面上过度使用主蓝色，保持克制
- **Don't** 使用小于14px的正文字体
- **Don't** 在内容区域使用全大写文本
