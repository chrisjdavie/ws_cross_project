# ws_cross_project
Common code used in all my PhD projects

This code is functions I used accross my PhD projects.  It is from an Eclipse workspace, which manages dependencies
so it won't run without quite a bit of editting.  

Possibly this ought to be different repositories.  There are 4 types of functions here;

1.0  File input and output functions

data_io_fns

I have a number of io operations to do with standard file types I used - ZeusMP hdfs and my csvs, primariy.

2.0  File and directory management

File_classes, Zeus_classes

Towards the end of my PhD, the separate functions for managing my output were becoming complex, so I created
a number of classes that deal with standard file and directory structures from my simulation codes, and made 
these the parents of more specialised functions.

3.0  Maths and physics.

general_maths

There were a number of mathematical forms that reoccured throughout my research, but were either not in common libraries
or the common library implementation was overly general or very slow.  So I did my own versions.

4.0  Plotting

generic_plotting

Broadly, 2 heirarchies of plotting, formatted in the same so to have consistent (and hopefully attractive) plotting 
throughout my thesis work.  I think I was successful, because other papers started copying my plotting style in certain
cases.

the linear plotting, which is x, y and lines.

'colour plotting' - which is different types of colour plots and quiver plots.

These branches have some duplication of code, but they stem from different ways of doing things in matplotlib, and it
was quicker and less fiddly to manage them as two independent paths.  (They were 1 tree before)

Copyright Chris J. Davie, 2015
