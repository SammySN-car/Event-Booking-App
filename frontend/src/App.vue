<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <router-link class="navbar-brand" to="/">App</router-link>
        <div class="navbar-nav ms-auto">
          <router-link class="nav-link" to="/login">Login</router-link>
          <router-link class="nav-link" to="/signup">Signup</router-link>
        </div>
      </div>
    </nav>
    <div class="container mt-4">
      <router-view></router-view>
    </div>
  </div>
</template>
<script setup>
</script>
