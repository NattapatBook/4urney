<template>
  <div class="home-page">
    <div class="header">
      <h1>Welcome to Home Page</h1>
      <nav>
        <button @click="$emit('navigate', 'landing')">Logout</button>
      </nav>
    </div>
    <div class="content">
      <h2>Dashboard</h2>
      <p>
        This is your dashboard. You can view your account details and other
        settings here.
      </p>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  padding: 20px;
  background-color: #f4f4f9;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
}

header h1 {
  font-size: 1.5rem;
}

nav button {
  background-color: transparent;
  color: white;
  border: 1px solid white;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
}

nav button:hover {
  background-color: white;
  color: #007bff;
}

.content {
  margin-top: 20px;
}

.content h2 {
  font-size: 1.5rem;
}

.content p {
  font-size: 1rem;
  color: #333;
}

@media (max-width: 600px) {
  .header h1 {
    font-size: 1.2rem;
  }

  .content h2 {
    font-size: 1.2rem;
  }

  .content p {
    font-size: 0.9rem;
  }

  nav button {
    padding: 8px 12px;
  }
}
</style>
