<%inherit file="base.mako"/>
<%page args="request, users=list(), **kwargs" />

<h1>User Management</h1>

<h2>Create User</h2>
<form action="${request.route_url('create_user')}" method="POST">
  <label for="email">Email</label>
  <input name="email"/>

  <label for="password">Password</label>
  <input type="password" name="password"/>

  <select name="user_type">
    <option value="basic" selected>User</option>
    <option value="admin">Admin</option>
  </select>

  <input type="submit" value="Submit"/>
</form>

<h2>Users</h2>
<ul>
  % for user in users:
    <li>
	  ${user.email}
	</li>
  % endfor
</ul>
