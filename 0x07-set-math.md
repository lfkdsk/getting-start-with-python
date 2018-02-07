## 0x07 Pythonic 时间：集合的数学操作符

我们在学习过 **List** ，**Dict** 之后再学习 **Set** 就很好理解了，Set 就像是去重的 List，或者是只有 Key 没有 Value 的 Dict，像这两种数据结构一样，Set 也实现了 Iterable 和 Container 接口，所以我们对于 Set 也可以使用 `for-in` 循环进行遍历，也可以直接使用 `in` 关键字来判断一个元素是否存在于这个集合之中。

但是我们这么来使用 Set 仅仅使用了它一部分的功能，忽略了 Set 代表的数学意义。*集合论* 是一种是研究集合的数学理论，包括对元素、集合、关系等多个方面的讨论。不过我们这里不用对这些数学概念有特别详细的了解，这需要了解这些操作集合的基础符号就好了：

* 并：包含集合 A 和 B 两个集合的元素（ $A | B$ ）
* 交：包含集合 A 和 B 两个结合元素的交集（$A \& B$）
* 差：包含集合 A 中和集合 B 中不重合的元素 （$A - B$）, 如果反过来就是（$B - A$）
* 对称差：包含集合 A 或是 B 中的元素，但是不包含 A 和 B 的交际部分（*A ^ B*）

比如说我们正常想求出两个列表之中共同的部分（交集），比如说我们还用刚才的那个 **调查问卷** 的例子，我们需要求出多个调查问卷来源之中重复的部分：

``` python
# questionnaire_A
# questionnaire_B

result = []
for A in questionnaire_A:
    if A in questionnaire_B:
        result.append(A)
```

这段代码在 Iterable 和 Container 接口的加持之下看起来已经很简洁了，但是我们使用集合的数学操作符能将这个过程变得非常的简洁：

``` python
# questionnaire_A
# questionnaire_B

result = set(questionnaire_A) & set(questionnaire_B)
```

