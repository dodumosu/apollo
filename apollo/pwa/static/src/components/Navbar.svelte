<script>
  export let i18n;

  import ConnectivityIndicator from './ConnectivityIndicator.svelte';
</script>

<nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top-mb-6">
  <div class="container-fluid">
    <a href="." class="navbar-brand">Apollo</a>
    <ConnectivityIndicator {i18n}/>
  </div>
</nav>