<template>
  <div class="loading">
    <div class="loading-spinner"></div>
    <p>Loading...</p>
  </div>
</template>

<script>
export default {
  name: "LoadingSpinner",
};
</script>

<style scoped>

.loading {
  display: flex;
  flex-direction: column; /* Stack spinner and text vertically */
  align-items: center;    /* Center horizontally */
  justify-content: center; /* Center vertically */
  gap: 10px;
  min-height: 100vh;      /* Take full viewport height */
  position: fixed;        /* Fix it to the viewport */
  top: 0;
  left: 0;
  width: 100%;           /* Full width */
  margin: 0;             /* Remove any margins */
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

p {
  color: #fcfcfc;
  font-family: Arial, sans-serif;
  font-size: 22px;
  margin: 0;
}
</style>