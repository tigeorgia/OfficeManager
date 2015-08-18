
## Office Manager

The application closely follows the work flow of work time reporting currently used at Transparency International Georgia.
It allows to:
- request a leave 
- submit the monthly time sheet
- approve a leave or a time sheet (by a designated supervisor)
- allows to configure salary sources and monthly percentage assignments to employees
- lets office managers generate bulk reports of all the documents handled in the system ( time sheets, leave requests, salary assignments)
- allows for collection and exposure of organisation-wide public documents



## Installation note

The application communicates with an AD server on an unencrypted channel and only AD users can access it.
The configuration allows for the selection of user group who can access the functionality.

Once deployed, a super user account needs to be created and that superuser needs to build the firt employee profile, who receives the role of an HR manager (profile setting). This setting allows this employee to have unrestricted access to data, namely - pubic document repository and profile creation and modification.


## License

Tigeorgia's Office Manager notifier is released under the terms of [GNU General Public License (V2)](http://www.gnu.org/licenses/gpl-2.0.html).
