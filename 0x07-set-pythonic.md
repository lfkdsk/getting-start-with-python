## 0x07 Pythonic 时间：使用字典排除重复数据

我们在程序之中更经常会使用的数据结构还是 `List` 和 `Dict` ，但是在一些场景之中使用 `Set` 能更轻松方便的解决问题。比如说我们在编写一个处理 **调查问卷** 的处理程序，我们知道从各个社交网络、线上线下收集到的调查问卷的来源是比较混杂的，因此有可能产生很多的重复来源的问卷提交，因此我们在对问卷的处理之前需要先对收集到的问卷进行去重，我们之前也学过和去重相关的操作：

``` python
# all_questionnaires
unique_questionnaires = []

for questionnaire in all_questionnaires:
    if questionnaire not in unique_questionnaires:
        unique_questionnaires.append(questionnaire)

for questionnaire in unique_questionnaires:
    # 对每份调查表进行处理
```

这个办法虽然可以使用，但是如果类似的功能写多了，也会流于 **模板代码** 。但是我们要是使用 `Set` 来处理这种情况就能减少很多模板代码的编写，Set 有这样的一些优点让我们在这种情况下选择它：

* Set 仅包含各不相同的数据
* 已存在的元素再添加 Set 之后会被忽略
* Set 可以使用 **可迭代对象**（列表、元组、字典） 来创建，每个元素都会被 Hash 化

这是三个优点简直就是为了我们的这种场景而生的啊 =。=！这里我们可以直接参考第三条看看我们的代码能被精简到什么程度：

``` python
# all_questionnaires
unique_questionnaires = set(all_questionnaires)
for questionnaire in unique_questionnaires:
    # 对每份调查表进行处理
```

这里我们把原来的列表(all_questionnaires) 传进去创建了一个 `Set` 之中，List 中的重复的数据就会被自动的消除，返回的 Set 就是我们想要的数据了，接着我们直接进行处理就好了。