# PyShapes:A Shape detection module for Python

[![Build Status](https://travis-ci.org/sudoRicheek/PyShapes.svg?branch=master)](https://travis-ci.org/sudoRicheek/PyShapes)

**PyShapes** is a python package that allows to detect and extract the basic shapes(polygons and circles) present in an image. It also has some in-built attributes and functions to get basic information and perform basic operations on those shapes.

This module uses Python OpenCV as dependency

### Installation

Installation is very simple through pip

For pip

```
pip install PyShapes
```

For pip3

```
pip3 install PyShapes
```

### Usage

Importing the package

```
from PyShapes import *
```

Creating **PyShape** objects(Note : **Object creation must be on PyShape class !**)

```
shapes = PyShape("C:\\path\\to\\image")
```

Useful functions in **PyShape** -

* Getting all the shapes detected in an image :

  ```
  shapes_dictionary = shapes.get_all_shapes()
  ```

  *Gets all the shapes in the image and returns a dictionary !*

* Displaying the shapes detected by providing coloured boundaries to them in original image :

  ```
  shapes.show_shapes()
  ```

  *Creates the coloured boundaries on top of the original image and displays the shape names along with the indexes*

* Getting the coordinates of the corners of a particular shape :

  ```
  numpy_array = shapes.get_corners("name of shape", index_of_shape)
  ```

  *Returns the coordinates of the corners of the shape in form of a numpy array*

  *Returns* **None** *if there is no shape with that name/index*

* Getting the area of a particular shape :

  ```
  area_of_shape = shapes.get_area("name of shape", index_of_shape)
  ```

  *Returns the area of a particular shape in pixel<sup>2* *units; return type :* **double**

  *Returns* **-1** *if there is no shape with that name/index*
  
* Finally, don't forget to close the running object !
  
  ```
  shapes.close()
  ```
  
  *Closes the object and the binded dependencies*

### About

The source is in the PyShape.py file.

Created By Richeek. Copyright 2020
