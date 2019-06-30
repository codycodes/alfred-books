# alfred-books
_Use Alfred as an interface to access Apple's Books application_

## "Screenshots"


👩‍💻 Search title, author, or both at the same time 👨‍💻

![title or author or both](./media/author_title.gif)

***

👩‍💻 Search by genre, use large type to get some metadata, and quicklook to attempt to retrieve the cover 👨‍💻

![genre](./media/genre.gif)

***

👩‍💻 Get help on which options are available 👨‍💻
![help](./media/help.gif)

## Installation
Go to the [releases](https://github.com/codycodes/alfred-books/releases) page, download the latest version, double click to import it into Alfred (note: powerpack is required for all third party workflows, including this one!)
## Usage & General Info
	
You can search for title and author using the keyword search (default is `ib`).
You can also use options as follows (in the format `ib -a` for each option, respectively):

`-a`  search by author only  
`-t`  search by title only  
`-g`  search by genre only  
`-h`  get available options for using this workflow

By default, if a title doesn't have a genre, Alfred Books won't be able to search for it.

While searching, you can press ⌘L to see some metadata about the selected title; this includes:  
title and author,   
genre,  
percentage read,  
description

While searching, pressing ⇧ (shift) on a selected title will attempt to show a cover and the actual filename.

While searching, pressing your action button (one of the following: → (right arrow), fn, ctrl, ⇥ (tab)) will allow you to act directly on the Books file. Be cautious here, as modifying the file from this interface may cause inconsistencies with the Books sqlite database, causing you to need to modify the actual sqlite database if you say modify or delete a file here.

This software (currently) only searches for downloaded books by confirming an accessible path to said file in the Books sqlite database. If they're on iCloud and not downloaded, they won't show up in Alfred Books!

If you have any issues whatsoever using this software, or if you have recommendations for features, please visit:
https://github.com/codycodes/alfred-books/issues