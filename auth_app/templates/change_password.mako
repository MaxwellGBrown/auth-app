<%inherit file="base.mako" />

<form action="${request.route_url('redeem', token=request.context.token)}" method="POST">
  <label for="password">
    New Password
  </label>
  <input type="password" name="password" />
  <input type="submit" label="Submit" />
</form>
