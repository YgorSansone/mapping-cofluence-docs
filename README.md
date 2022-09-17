## Mapping all confluence docs and saving as spreadsheets in Google Sheets
<p align="center">
  <img src="https://img.shields.io/badge/-Python-1e415e?logo=Python&logoColor=ffdd54&link=https://github.com/YgorSansone/mapping-cofluence-docs/" />
</p>

First, let's understand how the confluence document structure works. This is a tree structure, if you are not familiar with it, you can read more here [Everything you need to know about tree data structures
](https://medium.com/free-code-camp/all-you-need-to-know-about-tree-data-structures-bceacb85490c). 
Knowing this, we can use an Algorithm model similar to print all nodes from a tree stucture.

```
`-- "Page root"
    `-- "Page 1"
        |-- "Page 1.1"
        `-- "Page 1.2"
            |-- "Page 1.2.1"
            `-- "Page 1.2.2"
    `-- "Page 2"
        |-- "Page 2.1"
        |-- "Page 2.2"
        `-- "Page 2.3"
```

## How to use
##### - :computer:  Install
```sh
  $ git clone git@github.com:YgorSansone/mapping-cofluence-docs.git
```

##### - ⚙️ Customize configuration
SPACE_ID -> is a root page (need to set id) </br>
AUTHORIZATION -> is a confluence Basic Authorization </br>
SKIP_LABELS -> is a list of labels to skip</br>
URL_ROOT -> is a path from confluence</br>

Here is the tutorial to get your google credentials [From CSV to Google Sheet Using Python](https://medium.com/craftsmenltd/from-csv-to-google-sheet-using-python-ef097cb014f9)

Here is the tutorial to get you confluence authorization [Authentication and authorization](https://developer.atlassian.com/cloud/confluence/rest/intro/)

##### - 🚀 RUN

```sh
  $ pip install -r requirements.txt 
  $ python main.py
```

Thanks
<br>
