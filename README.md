# Lignin
#### Description:
**lignin** is a program that takes an image as input, and output the image split in two files
with half of it each.

**lignin** was created with the intention to help automatize page splitting after scanning a book
with a printer or scanner.

Let's say that you want to scan an old book of yours, so you can have a digital version of it, letting 
your old book live forever, without the need to worry about the consequences of time over a physical copy.
But your book has hundreds of pages, scanning it's pages will take some time, but you can cut that time in
half if you scan the book open with two pages at time, unfortunately it creates another problem, now each
image files has two pages each, and for the sake of organization you want a file per page. You could use
an image manipulation software and __manually__ split each file, but it would take a **lot** of time to
do, and also would require some knowledge with image manipulation software's.
So what to do? Let your pages de-organized with two pages per file? or increase the time spent scanning page
per page? Well, luckily with the power of programming I made a simple command line program for quickly
automate the process of splitting your files, so you don't need to spend more time scanning page by page of
your book! And even more, **lignin** offers some other simple functionalities for further adjust the
output pages after the scanning process with some options as per bellow.

---
## Options

### Cropping
> **-c**, **--crop**:
__Reason:__ The size of books are not always the same, so depending of the scan area of your scanner the
image file may have some wide empty spaces.

__Usage:__ Using **-c** or **--crop** require an argument, the argument is a **string**, it should contain
**four non negative integers** separated by **comma space (, )**. Each number represents a side of the image
in order being: **Left, Top, Right, Bottom** (it's easier to remember if you start with left and follow the
image in a clockwise direction). It works by providing a number of **pixel** to remove from the specific side.
For example, if you provide "150" to the left, it will crop 150 pixels from the left to the right.
The crop happens __before__ the splitting.

**VALID** examples:
'100, 50, 25, 100'
'0, 0, 200, 0'
'1, 2, 3, 4'

**INVALID** examples:
'-100, -50, -25, -100'
'200'
'1.5, 2.2, 3.8, 4.1'
'1,2,3,4'

**Applied example**:
``` bash
lignin -c '150, 0, 150, 0'
```

### Split Direction
> **-d**, **--direction**:
__Reason:__ Some books (mainly books for children) use an horizontal orientation for the pages, so instead
of reading the **left to right page**, you read **top to bottom page**.

__Usage:__ Using **-d** or **--direction** require an argument, there are only two arguments, **"v"** for vertical and
**"h"** for horizontal. The **"h"** argument will split the page horizontally. The **"v"** argument will split the
page vertically.
**"v"** (vertical) is the default value for this option.

**VALID** examples:
'v'
'V'
'h'
'H'

**INVALID** examples:
'vertical'
'horizontal'

**Applied example**:
``` bash
lignin -d 'h'
```

### Page Start Index
> **-i**, **--index**:
__Reason:__ If for some reason you need to split only part of the pages with a different set-up, so the suffix of the
files need to start from a specific index.

__Usage:__ Using **-i** or **--index** require an argument, the argument needs to be an integer number. It will set
the page number suffix to start at the given integer.

**VALID** examples:
2
400
64

**INVALID** examples:
2.5
'fox'

**Applied example**:
``` bash
lignin -i 64
```

### Force
> **-f**, **--force**:
__Reason:__ Maybe you split with the wrong set-up and you want to re-run the program with slight changes, but keeping
the file name, so you don't want a prompt asking for confirmation for all the files.

__Usage:__ Using **-f** or **--force** does NOT require an argument, it is a flag so just need to include it on the command.

**Applied example**:
``` bash
lignin -f
```

### Output prefix
> **-o**, **--output**:
__Reason:__ You may want to have some prefix name before the page index number.

__Usage:__ Using **-o** or **--output** require an argument, the argument is a **string** of text with anything you want.

**Applied example**:
``` bash
lignin -o 'my-book'
```

### Page Order
> **--order**:
__Reason:__ Some oriental countries read the pages **Right to Left** while occidental countries read **Left to Right**, so
you need to change the order the pages will be saved.

__Usage:__ Using **--order** require an argument, the argument is a **string** and there are only **four** possible arguments:
**"L-R"**, **"R-L"**, **"T-B"** and **"B-T"**, where: **L** is **Left**, **R** is **Right**, **T** is **Top** and **B** is **Bottom**.
It's needed to have the characters separated by a **-** (dash).
Note that it is **NOT** possible to mix __--direction 'v'__ with __--order 'T-B'__ or __'B-T'__ as they have **incompatible** orientation,
the same applies to __--direction 'h'__.

**"L-R"** is the default value.

**VALID** examples:
'L-R'
'R-L'
'T-B'
'B-T'

**INVALID** examples:
'LR'
'TB'
'Left Right'

**Applied example**:
``` bash
lignin --order 'R-L'
```

### Rotate
> **-r**, **--rotate**:
__Reason:__ The scanner may save by default in the wrong orientation, so it is useful to be able to rotate before splitting.

__Usage:__ Using **-r** or **--rotate** require an argument, the argument is a **number**. The image will be rotated in "__n__"
degrees clockwise, with "__n__" being the provided argument.
The rotation will be applied __BEFORE__ the split.

**VALID** examples:
'90'
'180'
'-90'
'40.8'
'0.5'

**Applied example**:
``` bash
lignin -r 90
```

### Zero Align
> **-z**, **--zalign**:
__Reason:__ Books have different amount of pages, so, for be more organized, you may want to align the numbers with zeros at the left,
so they will have the same character length.

__Usage:__ Using **-z** or **--zalign** require an argument, the argument is an **integer**. The file name index suffix will be aligned
with zeros until the index have the specified character length.
The default value will be the character length of the amount of files **after** split.

**VALID** examples:
'2'
'4'
'10'

**INVALID** examples:
'2.5'
'three'

**Applied example**:
``` bash
lignin -z 3
```

