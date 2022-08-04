# dm-discbot

This is the source code of a discord bot that dms everyone with specific roles

## Commands

!addroles {role/s}: Adds roles to the ones that will recieve a dm
!remroles {role/s}: Removes a role from the ones to dm
!setroles {role/s}: Sets the roles that will recieve a dm
!seeroles: Lets you see the roles that will recieve a dm
!dm {message}: Sends a dm to everyone with selected roles

## Examples

!setroles admin owner
!addroles mod srmod jrmod
!remroles jrmod
!seeroles
<I will ping this roles: admin, owner, mod, srmod>
!dm Hello
