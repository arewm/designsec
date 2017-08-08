# design-sec

This tool is intended to help the translation from a design document to implementation, specifically taking into account
security and usability concerns.

## High level design

Django backend to display sorted recommendation reports for individual projects. If someone tries to access an invalid project
id, they will be shown all possible recommendations.

There is also an admin interface to allow reports and recommendations to be created and edited easier.

Each report will have:
* A brief description of the design
* A brief description of the threat model
* The contact person for the project on the KNOX SECURITY team
* A list containing all recommendations that should be focused on

Potential sorting features are:
* Development process
* Code location
* Vulnerability of protocols -- no replay, sensitive to sequence of inputs
* Hardware/firmware recommendations
* Server/VM recommendations
* Usability
* ??

Long-term features
* Integrate into some tracking software to link to bugs found
* Allow suggested recommendations to be predicted based on a probabilistic model
* Comment functionality for user and admin
* Attach files to a recommendation
* Let recommendations be customized for a specific project without having to create a new one

