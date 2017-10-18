# -*- coding: utf-8 -*-


# 用于打印类似于/ex17之类的utf字段
def utf_print(element):
    return unicode(element, "utf8", errors="ignore")