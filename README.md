# design-sec

This is a proof of concept of a tool intended to help translate from requirements to implementation, by
ensuring that developers are aware of security and usability concerns.

Further development of this proof of concept was abandoned as a bigger re-architecture of the review process is needed
in order to prevent this interface from being just another site to check. I will still leave the original design
details below for reference.

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

