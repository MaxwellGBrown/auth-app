<%inherit file="base.mako"/>
<%page args="request, users=list(), **kwargs" />

<ul>
  % for user in users:
    <li>${user.email}</li>
  % endfor
</ul>
