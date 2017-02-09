<html>
  <head>
    <title>
      ${self.title()}
	</title>
  </head>

  <body>
  	${self.header()}
    ${next.body()}
  </body>
</html>

<%def name="title()">
  Auth App  
</%def>

<%def name="header()">
  ${self.auth()}
</%def>

<%def name="auth()">
  % if request.user is not None:
    <p>
      Logged in as ${request.user.email}
	  <a href="${request.route_url('logout')}">
	    Logout
	  </a>
	</p>
  % else:
  	<a href="${request.route_url('login')}">
	  Log in
	</a>
  % endif
</%def>
