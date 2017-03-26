<%def name="render_field(field)">
  ${field.label}
  ${field()}
  % if field.errors:
    <ul class="errors">
	  % for error in field.errors:
	    <li class="error">${error}</li>
	  % endfor
	</ul>
  % endif
</%def>
