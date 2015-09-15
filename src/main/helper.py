#!/usr/bin/env python
#
# (c) 2015 CSIOM, http://www.csiom.com
#
# This file is part of DeeDee project.
#
# DeeDee is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# DeeDee is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DeeDee.  If not, see <http://www.gnu.org/licenses/>.
#
#%% Authors %%
#Jasvir Singh Grewal <js@csiom.com>
#Aseem Mittal <aseemmittal@csiom.com>

_CODE_INTEGER_LENGTH = '03'

def code_generator(project,manager, project_id):
	"""Helper function for generating codes."""
	format_dict = '{0:' + _CODE_INTEGER_LENGTH + '}'
	project_code_id = project_id + 1	
	code = str(project[:1].upper()) + str(manager[:1].upper()) + format_dict.\
		format(project_code_id)
	return code