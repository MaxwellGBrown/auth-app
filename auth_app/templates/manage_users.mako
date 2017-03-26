<%inherit file="base.mako"/>
<%page args="request, users, create_user_form, **kwargs"/>
<%namespace name="forms" file="utils/forms.mako"/>

<h1>User Management</h1>

<h2>Create User</h2>
<form id="create-user-form" action="${request.route_url('create_user')}" method="POST">
  ${forms.render_field(create_user_form.email)}
  ${forms.render_field(create_user_form.user_type)}
  <input type="submit" value="Submit"/>
</form>

<h2>Users</h2>

<table id="user-table">
  <thead>
    <tr>
      <th>Id</th>
      <th>Type</th>
      <th>Email</th>
      <th>Token</th>
      <th>Actions</th>
    </tr>
  </thead>

  <tbody>
    % for user in users:
      ${row(user)}
    % endfor
  </tbody>
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
	<a href="${request.route_url('reset_user', user_id=user.user_id)}">
	  reset
	</a>
  </td>
</tr>
</%def>
