# 11/09 Multi Img + Single Img 标签 任务提交处

## 任务需求

注：在更新的格式基础上加图、加标签（颢怡提前反馈格式修改情况）
1. multi-img
在各自负责的既有数据集上，针对4o识图弱点扩充图片（同时json文件中加上count键），即自己之前造的+下面分配给你的数据集
从中抽取60%，也就是每人扩充大约150个
每个数据的扩充倍数3~9倍（平均6倍）(两种图的总数相乘)
single img中使用过的图，重命名序号必须为1！
2. **给所有single img（也就包括了multi img）加标签：conception/perception（自己之前造的+下面分配给你的数据集都由你负责加标签）**

## 提交格式

需要把纯single数据和multi数据分l离（群里已有辅助脚本seperate single from multi.py

```
- jhy
  - single
    - images（含许多子文件夹的大文件夹）
    - data_single.json
  - multi
    - images
    - data_multi.json
```
