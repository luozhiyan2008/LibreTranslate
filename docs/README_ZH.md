# LibreTranslate 中文说明（深北莫校区术语增强版）

本项目是 LibreTranslate 的 fork，面向深圳北理莫斯科大学日常学习场景，
新增校区中俄专业术语库。

## 新增功能
- 校区中俄专业术语库：金融科技、高等数学、数据结构等高频专业词汇译法统一
- 占位符保护 + 词干匹配双保险，防止机翻破坏术语

## 快速开始
pip install -e .
libretranslate --load-only zh,ru,en

浏览器打开 http://localhost:5000 即可使用。
