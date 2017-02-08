<%inherit file="base.mako" />

<h1>Login</h1>

<form method="POST" action="${request.route_url('login')}">
  <label for="email">
    Email
  </label> 
  <input type="text" name="email"/>

  <label for="password">
    Password
  </label> 
  <input type="password" name="password">

  <input type="submit" value="Submit"/>
</form>

<%def name="auth()">
  <%doc>Override base.mako's auth() which shows auth status</%doc>
</%def>
