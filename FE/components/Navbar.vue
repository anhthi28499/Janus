<template>
  <nav class="navbar glass-panel">
    <div class="logo">
      <h1>Janus AI</h1>
    </div>
    <div class="nav-links">
      <NuxtLink to="/knowledgebase" class="nav-item">Knowledgebase</NuxtLink>
      <NuxtLink to="/evaluation" class="nav-item">Evaluation</NuxtLink>
      <NuxtLink to="/janus" class="nav-item">Janus</NuxtLink>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  height: var(--nav-height);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo h1 {
  font-size: 1.25rem;
  font-weight: 700;
  background: linear-gradient(90deg, var(--color-primary), #9333ea);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-item {
  color: var(--color-text-muted);
  font-weight: 500;
  padding: 0.5rem;
  transition: all 0.2s;
  position: relative;
}

.nav-item:hover {
  color: var(--color-text);
}

.router-link-active {
  color: var(--color-primary);
}

.router-link-active::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--color-primary);
  border-radius: 2px;
}
</style>
