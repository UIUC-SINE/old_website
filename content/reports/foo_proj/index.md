----
author: evan
template: project.j2
date: 2019-04-09
title: Formatting and math demo
description: Demonstrating various formatting features
----

[TOC]

# Heading 1

foo

## Heading 2

bar

### Heading 3

baz

#### Heading 4

spam

##### Heading 5

ham

* bullet1
* bullet2
    * sub bullet
    

# Images

![inline image](cheetos_small.png "title"){: .inline } 
![inline image](cheetos_small.png){: .inline } 
![inline image](cheetos_small.png){: .inline } 

![](cheetos_small.png){: #id1 .class1 .class2 }


# Math

$$3x + 4y$$

$$[Rf](t, \theta) = \int_{\mathbb{R}^2} f(x)\delta(N_{\theta}^T x - t)\, dx$$ 

This is called a Radon transform. [^1]

# Code

A code snippet

``` python
print('hello world')
print('my name is evan')
```

`test.py`

``` python
def fib():
    a, b = 0, 1
    while 1:
        yield a
        a, b = b, a + b

x = fib()
next(x)
```

# Table

<iframe src="result1.html"></iframe>

# Bibliography

[^1]: Test, Foo, Bar
