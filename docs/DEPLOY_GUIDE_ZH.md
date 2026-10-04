# Windows 中文用户名环境部署排障指南

本人在 Windows（中文用户名）下自托管 LibreTranslate 的踩坑记录：

## 1. pip 安装报 GBK 编码错误
中文用户名导致 pip 读写缓存崩溃。解决：
    setx PYTHONUTF8 1

## 2. libretranslate 命令找不到
pip --user 安装后 Scripts 目录不在 PATH，
把 %APPDATA%\Python\Python310\Scripts 加入 PATH。

## 3. 语言包报 NOT_FOUND（sentencepiece.model）
C++ 组件无法读取含中文的路径，把语言包目录移到纯英文路径：
    setx ARGOS_PACKAGES_DIR "D:\argos-packages"

## 4. GitHub 连接
