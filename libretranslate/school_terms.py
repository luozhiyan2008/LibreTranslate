# 校园中俄专业术语库（深圳北理莫斯科大学 · 双创项目）v2 双保险版
#  1) protect:  翻译前，把源文本里的中文术语替换为占位符 [[0]] [[1]] ...
#  2) restore:  翻译后回填，分两层：
#     第一层：译文里还能找到占位符 -> 直接回填术语（最精确）
#     第二层：占位符被机翻吞掉、但术语大致被翻出 -> 用词干匹配把译文统一成术语库标准译法

import json
import os
import re

_terms = None


def _load():
    """加载术语表（只加载一次，之后走内存缓存）"""
    global _terms
    if _terms is None:
        path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "school_terms.json",
        )
        try:
            with open(path, "r", encoding="utf-8") as f:
                _terms = json.load(f)
            print("[school_terms] 已加载术语 %d 条" % len(_terms))
        except Exception as e:
            print("[school_terms] 术语库加载失败: %s" % e)
            _terms = {}
    return _terms


def _stem(word, n=6):
    """简单俄语词干：取前 n 个字符"""
    w = word.strip().lower()
    return w[:n]


def protect(q, source_lang, target_lang):
    """翻译前：把源文本中命中的术语替换为占位符。返回 (新文本, 映射表)"""
    terms = _load()
    if not terms or not q or not source_lang or not target_lang:
        return q, None
    # 当前术语表方向为 中 -> 俄，仅在这两个语言之间启用
    if not source_lang.startswith("zh") or not target_lang.startswith("ru"):
        return q, None
    mapping = {}
    i = 0
    # 长术语优先替换，避免"高等数学"被短词抢先
    for src_term in sorted(terms.keys(), key=len, reverse=True):
        if src_term in q:
            ru_term = terms[src_term]
            stems = [_stem(w) for w in ru_term.split() if len(w) > 4]
            mapping[str(i)] = {"ru": ru_term, "stems": stems}
            q = q.replace(src_term, "[[" + str(i) + "]]")
            i += 1
    return q, (mapping if mapping else None)


def restore(translated_text, mapping):
    """翻译后：两层策略把术语库译法注入译文"""
    if not mapping or not translated_text:
        return translated_text
    for idx, item in mapping.items():
        term = item["ru"]
        stems = item.get("stems") or []
        # 第一层：占位符回填（机翻保留了占位符时）
        pat = r"\[\[\s*" + re.escape(idx) + r"\s*\]\]|\[\s*" + re.escape(idx) + r"\s*\]"
        if re.search(pat, translated_text):
            translated_text = re.sub(pat, term, translated_text)
            print("[school_terms] 占位符回填 -> %s" % term)
            continue
        # 第二层：词干匹配（机翻吞掉占位符时，把译文中机翻出的术语统一为词典译法）
        if stems:
            phrase = r"\b" + r"\s+".join(re.escape(s) + r"\w*" for s in stems) + r"\b"
            if re.search(phrase, translated_text, flags=re.IGNORECASE):
                translated_text = re.sub(phrase, term, translated_text, flags=re.IGNORECASE)
                print("[school_terms] 词典统一 -> %s" % term)


# 模块加载时立即读取术语表，服务启动日志中可看到加载结果
_load()
