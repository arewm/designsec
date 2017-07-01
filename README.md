# design-sec

Help in the translation from a design document to implementation, specifically taking into account security and usability concerns.

## High level design

Django backend

Either a function to generate the HTML for each sort method or a JQuery method to reorganize the elements based on the category they belong to.

Each report will have:
* A brief description of the design
* A brief description of the threat model
* The contact person for the project on the KNOX SECURITY team
* A list containing all elements that should be focused on

There will be an admin interface where a specific report can be generated. Once a report is generated, it will be assigned a unique ID to be accessed statically. If someone tries to access an invalid report (including no report), all elements will be displayed. The admin interface will also allow custom elements to be generated. 

*Using JQuery will be better so the admin interface can also be rearranged while keeping the selections*

Potential sorting features are:
* Development process
* Code location
* ??

