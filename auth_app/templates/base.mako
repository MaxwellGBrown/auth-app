<html>
  <head>
    <title>
      ${self.title()}
	</title>
  </head>

  <body>
	${self.navbar()}
    ${next.body(**context.kwargs)}
  </body>
</html>

<%def name="title()">
  Auth App  
</%def>

<%def name="navbar()">
  <ul>
    % if request.has_permission("authenticated"):
	<li>
      Logged in as ${request.user.email}
	  <ul>
	  	<li>
          <a href="${request.route_url('logout')}">Logout</a>
		</li>
	  </ul>
	</li>

    % else:
	<li>
	  <a href="${request.route_url('login')}">Log in</a>
	</li>

    % endif

    <li>
	  <a href="${request.route_url('index')}">Index</a>
	</li>

	% if request.has_permission("authenticated"):
    <li>
	  <a href="${request.route_url('home')}">Home</a>
	</li>
	% endif

	% if request.has_permission("admin"):
    <li>
	  Admin
	  <ul>
	    <li>
	      <a href="${request.route_url('manage_users')}">Users</a>
	    </li>
	  </ul>
	</li>
	% endif
  </ul>

</%def>

<%def name="auth()">
</%def>
