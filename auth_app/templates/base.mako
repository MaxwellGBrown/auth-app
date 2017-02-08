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
  % if request.user is not None:
    Logged in as ${request.user.email}
  % endif
</%def>
