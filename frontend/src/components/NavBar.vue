<template>
  <nav class="nav-wrapper">
    <div class="nav-title">
      <h2>App title</h2>
    </div>
    <div class="nav-auth">
      <p>Current user,</p>
      <a href="#">Login</a>
      <a href="#">Register</a>
      <a href="#">Logout</a>
    </div>
  </nav>
</template>

<script>
export default {};
</script>

<style>
.nav-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  background-color: #333;
  color: white;
  box-sizing: border-box;
}
.nav-auth {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.nav-auth a {
  color: white;
  margin-left: 10px;
  text-decoration: none;
}
.nav-auth a:hover {
  text-decoration: underline;
}
</style>