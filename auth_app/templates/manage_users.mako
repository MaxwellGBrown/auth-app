<%inherit file="base.mako"/>
<%page args="request, users=list(), **kwargs" />

<h1>User Management</h1>

<h2>Create User</h2>
<form action="${request.route_url('create_user')}" method="POST">
  <label for="email">Email</label>
  <input name="email"/>

  <select name="user_type">
    <option value="basic" selected>User</option>
    <option value="admin">Admin</option>
  </select>

  <input type="submit" value="Submit"/>
</form>

<h2>Users</h2>

<table id="user-table">
  <tr>
    <th>Id</th>
	<th>Type</th>
    <th>Email</th>
	<th>Token</th>
	<th>Delete</th>
  </tr>

  % for user in users:
    ${row(user)}
  % endfor
</table>

<%def name="row(user)">
<tr>
  <td>${user.user_id}</td>
  <td>${user.user_type}</td>
  <td>${user.email}</td>
  
  % if user.token is not None:
  <td>${request.route_url('redeem', token=user.token)}</td>
  % else:
  <td></td>
  % endif
  
  <td>
    <a href="${request.route_url('delete_user', user_id=user.user_id)}">
	  delete
	</a>
  </td>
</tr>
</%def>
