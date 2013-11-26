# -*- coding: utf-8 -*-

import sys
import jieba



jieba.load_userdict("userdict.txt") 

seg_list = jieba.cut("1碗米粉蒸肉")
print ", ".join(seg_list)

seg_list = jieba.cut("一个鸡蛋")
print ", ".join(seg_list)

seg_list = jieba.cut("一根玉米")
print ", ".join(seg_list)

seg_list = jieba.cut("半小碗饭")
print ", ".join(seg_list)

seg_list = jieba.cut("十颗开心果")
print ", ".join(seg_list)

seg_list = jieba.cut("12个包子")
print ", ".join(seg_list)

seg_list = jieba.cut("100g包子")
print ", ".join(seg_list)

seg_list = jieba.cut("100克包子")
print ", ".join(seg_list)