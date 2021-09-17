---
title: groovy基础语法
date: 2021-09-17 19:30:20
tags: groovy
---

# GROOVY基础入门

## 概要

groovy基于JVM（java虚拟机）的敏捷开发语言，结合了Python，Ruby和Smalltalk许多强大的特性。groovy代码能够与java代码很好地结合，也能够用于扩展现有代码。groovy可以使用java代码编写的库。

<!-- more -->

## 特点

- java之外的特性支持 
- 支持dsl（领域定义语言）
- 有原生类型、有面向对象，ant dsl，编写脚本很简单
- 开发web，gui，数据库或者控制台程序时通过减少框架性代码提高编码效率
- 直接编译成java字节码，可以在任何用java的地方直接用groovy
- 支持函数式编程，不需要main函数
- 新的运算符，默认导入常用的包，支持单元测试和模拟
- 类不支持default作用域，默认作用域为public
- groovy基本类型也是对象，可以直接调用对象的方法

## 重要特性

1. 动态类型

   类型对于变量，属性，方法，闭包的参数以及方法的返回类型都是可有可无的，都是在给变量赋值的时候才决定它的类型， 不同的类型会在后面用到，任何类型都可以被使用,即使是基本类型 (通过自动包装（autoboxing）). 当需要时，很多类型之间的转换都会自动发生，比如在这些类型之间的转换: 字符串（String），基本类型(如int) 和类型的包装类 (如Integer)之间，可以把不同的基本类型添加到同一数组（collections）中。

2. 闭包

   可以使用参数的代码片段，每个闭包会被编译成继承groovy.lang.Closure类的类，这个类有一个叫call方法，通过该方法可以传递参数并调用这个闭包.它们可以访问并修改在闭包创建的范围内的变量，在闭包内创建的变量在闭包被调用的范围内同样可以被引用， 闭包可以保存在变量中并被作为参数传递到方法中。

3. 语法

   可以将它想像成 Java 语言的一种更加简单、表达能力更强的变体。Groovy 和 Java 语言的主要区别是：完成同样的任务所需的 Groovy 代码比 Java 代码更少。

4. 类

   Groovy类和java类一样，完全可以用标准java bean的语法定义一个Groovy类。但作为另一种语言，可以使用更Groovy的方式定义类，这样的好处是，可以少写一半以上的javabean代码。

   **（1）不需public修饰符**

   如前面所言，Groovy的默认访问修饰符就是public，如果Groovy类成员需要public修饰，则根本不用写它。

   **（2）不需要类型说明**

   同样前面也说过，Groovy也不关心变量和方法参数的具体类型。

   **（3）不需要getter/setter方法**

   在很多ide（如eclipse）早就可以为程序员自动产生getter/setter方法了，在Groovy中，不需要getter/setter方法--所有类成员（如果是默认的public）根本不用通过getter/setter方法引用它们（当然，如果一定要通过getter/setter方法访问成员属性，Groovy也提供了它们）。

   **（4）不需要构造函数**

   不再需要程序员声明任何构造函数，因为实际上只需要两个构造函数（1个不带参数的默认构造函数，1个只带一个map参数的构造函数--由于是map类型，通过这个参数可以构造对象时任意初始化它的成员变量）。

   **（5）不需要return**

   Groovy中，方法不需要return来返回值。

   **（6）不需要（）**

   Groovy中方法调用可以省略（）（构造函数除外）。

## 基本语法

​	**导入** 默认导入以下库

```groovy
import java.lang.* 
import java.util.* 
import java.io.* 
import java.net.* 

import groovy.lang.* 
import groovy.util.* 

import java.math.BigInteger 
import java.math.BigDecimal
```

导入其他库时可以这么导

```groovy
import groovy.xml.MarkupBuilder 
def xml = new MarkupBuilder() 
```

**分号**

```groovy
class Example {
   static void main(String[] args) {
      // One can see the use of a semi-colon after each statement
      def x = 5;
      println('Hello World');  
   }
}
```

**身份标识**  标识符被用来定义变量，函数或其他用户定义的变量。标识符以字母开头，美元或下划线。他们不能以数字开头。

```groovy
def employeename 
def student1 
def student_name
```

def是用来定义标识符的关键字

**关键词**

| as     | assert  | break      | case       |
| ------ | ------- | ---------- | ---------- |
| catch  | class   | const      | continue   |
| def    | default | do         | else       |
| enum   | extends | false      | Finally    |
| for    | goto    | if         | implements |
| import | in      | instanceof | interface  |
| new    | pull    | package    | return     |
| super  | switch  | this       | throw      |
| throws | trait   | true       | try        |
| while  |         |            |            |

**空白** 告诉编译器如何分割不同声明的部分

**文字** 文字表示固定值的符号，符号整数，浮点数，字符和字符串

```groovy
12 
1.45 
‘a’ 
“aa”
```

## groovy数据类型

内置类型：byte short int  long float double char Boolean String

| byte   | -128到127                                               |
| ------ | ------------------------------------------------------- |
| short  | -32,768到32,767                                         |
| int    | 2,147,483,648 到,147,483,647                            |
| long   | -9,223,372,036,854,775,808到+9,223,372,036,854,775,807  |
| float  | 1.40129846432481707e-45到3.40282346638528860e + 38      |
| double | 4.94065645841246544e-324d 到1.79769313486231570e + 308d |

支持高精度计算的累（java包装类）

| 名称                 | 描述                             | 例如 |
| -------------------- | -------------------------------- | ---- |
| java.math.BigInteger | 不可变的任意精度的有符号整数数字 | 30g  |
| java.math.BigDecimal | 不可变的任意精度的有符号十进制数 | 3.5g |

## 运算符

特别注意的运算符

范围运算符 .. 

```groovy
def range = 0..5
```

表示一个整数范围，下限0上限5，具体案例：

```groovy
class Example { 
   static void main(String[] args) { 
      def range = 5..10; 
      println(range); 
      println(range.get(2)); 
   } 
}
```

get语句会从定义的范围中获取一个对象，将索引值作为参数

优先级

| 运算符                                               | 名称                    |
| ---------------------------------------------------- | ----------------------- |
| ++ - + -                                             | 预增/减，一元加，一元减 |
| * / ％                                               | 乘法，除法，取模        |
| + -                                                  | 加法，减法              |
| ==！= <=>                                            | 等于，不等于，比较      |
| ＆                                                   | 二进制/位运算符与       |
| ^                                                    | 二进制/位异或           |
| \|                                                   | 二进制/按位或           |
| &&                                                   | 逻辑和                  |
| \|\|                                                 | 逻辑或                  |
| = ** = * = / =％= + = - = << = >> = >>> = = ^ = \| = | 各种赋值运算符          |

## 循环 

break continue语句用于改变循环里的控制流 break还可以用于改变switch语句内的控制流

```groovy
while(condition) { 
   statement #1 
   statement #2 
   ... 
}
for(variable declaration;expression;Increment) { 
   statement #1 
   statement #2 
   … 
}
for(variable in range) { 
   statement #1 
   statement #2 
   … 
}
```

## 条件语句

**if** if/else 嵌套if  switch  嵌套switch

## 方法

Groovy 中的方法是使用返回类型或使用 def 关键字定义的。方法可以接收任意数量的参数。定义参数时，不必显式定义类型。可以添加修饰符，如 public，private 和 protected。默认情况下，如果未提供可见性修饰符，则该方法为 public。

**默认参数：**默认参数在参数列表的末尾定义

```groovy
def someMethod(parameter1, parameter2 = 0, parameter3 = 0) {    // Method code goes here } 
```

**返回值：** 

```groovy
static int sum(int a,int b = 5) {      int c = a+b;      return c;   } 
```

**实例方法：**

**本地参数和外部参数**：

```groovy
class Example { // x是全局的属性   static int x = 100; 	   public static int getX() {       // lx是内部属性      int lx = 200;       println(lx);       return x;    } 	   static void main(String[] args) {       println getX()    }  }
```

**方法属性：**

groovy 可以使用 this 关键字访问它的实例成员。

## 可选类型

与Java相比，Java是一种“强”类型的语言，由此编译器知道每个变量的所有类型，并且可以在编译时理解和尊重合同。这意味着方法调用能够在编译时确定。

Groovy中编写代码时，开发人员可以灵活地提供类型或不是类型。可选类型通过def关键字键入，可以用于声明一些基本类型或者是包装类。

为了避免想要使用可选类型提供的灵活性同时兼顾后期开发阶段的可维护性，可以采用鸭式编程的方式。

```groovy
def aint = 100;       println(aint); 		      // Example of an float using def       def bfloat = 100.10;       println(bfloat); 		      // Example of an Double using def       def cDouble = 100.101;       println(cDouble);		      // Example of an String using def       def dString = "HelloWorld";       println(dString); 
```

## 列表

List 中的对象引用占据序列中的位置，并通过整数索引来区分。

列表文字表示为一系列用逗号分隔并用方括号括起来的对象。

groovy 列表使用索引操作符 [] 索引。列表索引从 0 开始，指第一个元素。

groovy 中的一个列表中的数据可以是任意类型。这 java 下集合列表有些不同，java 下的列表是同种类型的数据集合。

groovy 列表可以嵌套列表。groovy 列表内置有反转方法 reverse()。groovy 列表内置有排序方法 sort()。空列表表示为 [] 声明一个空集合：

```groovy
def list1 = []  def list2 = [1,2,3,4]  list2.add(12)  list2.add(12)  println list1.size()
```

**添加**

```groovy
def list1 = [100, 101]def list2 = [ 99,98,1]println list2.plus(list1)//输出结果： [100, 101, 99, 98,1]// list2.plus(list1) 也可以写成 list2 + list1
```

**删除**

```groovy
def list1 = [12, 13]def list2 = [11, 2, 33, 12, 13, 16]println list2.minus(list1) //输出结果： [11, 2, 33, 16]//list2.minus(list1) 也可以写成 list2 - list1
```

| 序号 |                          方法和描述                          |
| ---- | :----------------------------------------------------------: |
| 1    | [add()](https://www.w3cschool.cn/groovy/groovy_add.html)将新值附加到此列表的末尾。 |
| 2    | [contains()](https://www.w3cschool.cn/groovy/groovy_lists_contains.html)如果此列表包含指定的值，则返回 true。 |
| 3    | [get()](https://www.w3cschool.cn/groovy/groovy_lists_get.html)返回此列表中指定位置的元素。 |
| 4    | [isEmpty()](https://www.w3cschool.cn/groovy/groovy_isempty.html)如果此列表不包含元素，则返回 true |
| 5    | [minus()](https://www.w3cschool.cn/groovy/groovy_lists_minus.html)创建一个由原始元素组成的新列表，而不是集合中指定的元素。 |
| 6    | [plus()](https://www.w3cschool.cn/groovy/groovy_lists_plus.html)创建由原始元素和集合中指定的元素组成的新列表。 |
| 7    | [pop()](https://www.w3cschool.cn/groovy/groovy_pop.html)从此列表中删除最后一个项目 |
| 8    | [remove()](https://www.w3cschool.cn/groovy/groovy_remove.html)删除此列表中指定位置的元素。 |
| 9    | [reverse()](https://www.w3cschool.cn/groovy/groovy_reverse.html)创建与原始列表的元素相反的新列表 |
| 10   | [size()](https://www.w3cschool.cn/groovy/groovy_lists_size.html)获取此列表中的元素数。 |
| 11   | [sort()](https://www.w3cschool.cn/groovy/groovy_sort.html)返回原始列表的排序副本。 |

## 映射

映射（也称为关联数组，字典，表和散列）是对象引用的无序集合。Map集合中的元素由键值访问。 Map中使用的键可以是任何类。当我们插入到Map集合中时，需要两个值：键和值。

- ['TopicName'：'Lists'，'TopicName'：'Maps'] - 具有TopicName作为键的键值对的集合及其相应的值。
- [：] - 空映射。

| 序号 |                          方法和描述                          |
| ---- | :----------------------------------------------------------: |
| 1    | [containsKey()](https://www.w3cschool.cn/groovy/groovy_containskey.html)此映射是否包含此键？ |
| 2    | [get()](https://www.w3cschool.cn/groovy/groovy_maps_get.html)查找此Map中的键并返回相应的值。如果此映射中没有键的条目，则返回null。 |
| 3    | [keySet()](https://www.w3cschool.cn/groovy/groovy_keyset.html)获取此映射中的一组键。 |
| 4    | [put()](https://www.w3cschool.cn/groovy/groovy_put.html)将指定的值与此映射中的指定键相关联。如果此映射先前包含此键的映射，则旧值将替换为指定的值。 |
| 5    | [size()](https://www.w3cschool.cn/groovy/groovy_maps_size.html)返回此地图中的键值映射的数量。 |
| 6    | [values()](https://www.w3cschool.cn/groovy/groovy_values.html)返回此地图中包含的值的集合视图。 |

## 异常

**捕获异常： **try和catch关键字的组合捕获异常。 try / catch块放置在可能生成异常的代码周围。

```groovy
try {    //Protected code } catch(ExceptionName e1) {   //Catch block }
```

**多个捕获块： ** 对具体类型的异常做不同的处理

**finally块** 跟在try块或catch块之后。代码的finally块总是执行，而不管异常的发生。

## 面向对象

**扩展**  extends用于继承累的属性的关键字

**内部类** 内部类在另一个类中定义。封闭类可以像往常一样使用内部类。另一方面，内部类可以访问其封闭类的成员，即使它们是私有的。不允许除封闭类之外的类访问内部类。

```groovy
class Outer {    String name;	   def callInnerMethod() {       new Inner().methodA()    } 	   class Inner {      def methodA() {          println(name);       }    } }  
```

**抽象类 ** 表示通用概念，因此，它们**不能被实例化**，被创建为子类化。成员包括字段/属性和抽象或具体方法。抽象方法没有实现，必须通过具体子类来实现。抽象类必须用抽象关键字声明。抽象方法也必须用抽象关键字声明。

```groovy
abstract class Person {    public String name;    public Person() { }    abstract void DisplayMarks();} class Student extends Person {    int StudentID    int Marks1; 	   public Student() {       super();    } 	   void DisplayMarks() {       println(Marks1);    }  } 
```

**接口 ** 接口仅定义需要实现的方法的列表，但是不定义方法实现。需要使用interface关键字声明接口。接口仅定义方法签名。接口的方法总是公开的。在接口中使用受保护或私有方法是一个错误。

```groovy
interface Marks {    void DisplayMarks(); } class Student implements Marks {   int StudentID   int Marks1;	   void DisplayMarks() {      println(Marks1);   }}
```

## 泛型

以下是一个泛型类的实例：

```groovy
public class ListType<T> {   private T localt;	   public T get() {      return this.localt;   }	   public void set(T plocal) {      this.localt = plocal;   } }
```

## 特征 

特征是语言的结构构造，允许 -

- 行为的组成。
- 接口的运行时实现。
- 与静态类型检查/编译的兼容性

可看作是承载默认实现和状态的接口。使用trait关键字定义 trait。

```groovy
trait Marks {    void DisplayMarks() {      println("Display Marks");   } } class Student implements Marks {    int StudentID   int Marks1;}
```

**实现接口**

Traits 可以实现接口，在这种情况下，使用 interface 关键字声明接口。下

- 接口 Total 使用方法 DisplayTotal 定义。
- 特征 Marks 实现了 Total 接口，因此需要为 DisplayTotal 方法提供一个实现。

```groovy
interface Total {   void DisplayTotal() } trait Marks implements Total {   void DisplayMarks() {      println("Display Marks");   }	   void DisplayTotal() {      println("Display Total");    } } class Student implements Marks {    int StudentID   int Marks1;  } 
```

**属性** 特征可以定义属性。

```groovy
interface Total {      void DisplayTotal()    } 	   trait Marks implements Total {      int Marks1;		      void DisplayMarks() {         this.Marks1 = 10;         println(this.Marks1);      }		      void DisplayTotal() {         println("Display Total");      }    } 	   class Student implements Marks {      int StudentID    }
```

**行为的构成**

特征可以用于以受控的方式实现多重继承，避免钻石问题。

```groovy
trait Marks {   void DisplayMarks() {      println("Marks1");   } } trait Total {   void DisplayTotal() {       println("Total");   } }  //Student扩展了两个特征，可以访问这两种方法class Student implements Marks,Total {   int StudentID }   
```

**扩展特征** 特征可能扩展另一个特征，在这种情况下，必须使用extends关键字。在下面的代码示例中，我们使用 Marks trait 扩展了 Total trait。

```groovy
class Example {   static void main(String[] args) {      Student st = new Student();      st.StudentID = 1;      println(st.DisplayMarks());// 输出Total   } } trait Marks {   void DisplayMarks() {      println("Marks1");   } } trait Total extends Marks {   void DisplayMarks() {      println("Total");   } }  class Student implements Total {   int StudentID }
```

## 闭包

短的匿名代码段

```groovy
def clos = {println "Hello World"};clos.call();
```

**形式参数：** 使用$ {param}，这导致closure接受一个参数。当通过clos.call语句调用闭包时，我们现在可以选择将一个参数传递给闭包。

```groovy
def clos = {param->println "Hello ${param}"};clos.call("World");
```

```groovy
def clos = {println "Hello ${it}"};clos.call("World");//和上一个例子是同样的结果，it是关键字
```

**闭包和变量： **闭包可以在定义闭包时引用变量

```groovy
def str1 = "Hello";def clos = {param -> println "${str1} ${param}"}clos.call("World");//Hello Worldstr1 = "Welcome";clos.call("World");//Welcome World
```

**在方法中使用闭包** 闭包也可以用作方法的参数

```groovy
def static Display(clo) {      // This time the $param parameter gets replaced by the string "Inner"               clo.call("Inner");   } static void main(String[] args) {      def str1 = "Hello";      def clos = { param -> println "${str1} ${param}" }      clos.call("World");      // Passing our closure to a method      Example.Display(clos);   } 
```

**集合和字符串中的闭包** list Map String 方法接收一个闭包作为参数

```groovy
def lst = [11, 12, 13, 14];lst.each {println it}
```

**使用映射闭包** 

```groovy
def mp = ["TopicName" : "Maps", "TopicDescription" : "Methods in Maps"]             mp.each {println it}mp.each {println "${it.key} maps to: ${it.value}"}
```

```groovy
lst.each{num -> if(num % 2 == 0) println num}
```

**闭包本身使用的方法**

| 序号 |                          方法和描述                          |
| ---- | :----------------------------------------------------------: |
| 1    | [find()](https://www.w3cschool.cn/groovy/groovy_find.html)find方法查找集合中与某个条件匹配的第一个值。 |
| 2    | [findAll（）](https://www.w3cschool.cn/groovy/groovy_findall.html)它找到接收对象中与闭合条件匹配的所有值。 |
| 3    | [any() & every()](https://www.w3cschool.cn/groovy/groovy_any_every.html)方法any迭代集合的每个元素，检查布尔谓词是否对至少一个元素有效。 |
| 4    | [collect()](https://www.w3cschool.cn/groovy/groovy_collect.html)该方法通过集合收集迭代，使用闭包作为变换器将每个元素转换为新值。 |

```groovy
 value = lst.find {element -> element > 2} value = lst.findAll {element -> element > 2}// Is there any value above 2value = lst.any{element -> element > 2}println(value);//true// Are all value above 2value = lst.every{element -> element > 2}println(value);//falsenewlst = lst.collect {element -> return element * element}println(newlst);
```

## DSLS

Groovy允许在顶层语句的方法调用的参数周围省略括号。这被称为“命令链”功能。这个扩展的工作原理是允许一个人链接这种无括号的方法调用，在参数周围不需要括号，也不需要链接调用之间的点。

```groovy
class EmailDsl {     String toText    String fromText    String body 	   /**    * This method accepts a closure which is essentially the DSL. Delegate the    * closure methods to    * the DSL class so the calls can be processed    */       def static make(closure) {       EmailDsl emailDsl = new EmailDsl()       // any method called in closure will be delegated to the EmailDsl class       closure.delegate = emailDsl      closure()    }      /**    * Store the parameter as a variable and use it later to output a memo    */ 	   def to(String toText) {       this.toText = toText    }      def from(String fromText) {       this.fromText = fromText    }      def body(String bodyText) {       this.body = bodyText    } }EmailDsl.make {    to "Nirav Assar"    from "Barack Obama"    body "How are things? We are doing well. Take care" }
```

- 使用接受闭包的静态方法。这是一个很麻烦的方式来实现DSL。
- 在电子邮件示例中，类EmailDsl具有make方法。它创建一个实例，并将闭包中的所有调用委派给实例。这是一种机制，其中“to”和“from”节结束了EmailDsl类中的执行方法。
- 一旦to（）方法被调用，我们将文本存储在实例中以便以后格式化。
- 我们现在可以使用易于为最终用户理解的简单语言调用EmailDSL方法。

## shebang

除了单行注释外, 还有一种被特别的行注释, 通常被称作shebang行，它通常在UNIX系统中被认知，它容许脚本直接在命令行中运行那些你已经安装的Groovy和那些已经在PATH中可用的groovy命令。

```sh
#!/usr/bin/env groovyprintln "Hello from the shebang line"
```

