<script>
  export let i18n;

  let isOnline = navigator.onLine;
  const handler = () => {
    isOnline = navigator.onLine;
  };

  window.addEventListener('offline', handler);
  window.addEventListener('online', handler);
</script>


<div class="d-flex text-light">
{#if isOnline}
<span>{ i18n.gettext('Online') } <svg width="24" height="24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M5.636 5.636a1 1 0 00-1.414-1.414c-4.296 4.296-4.296 11.26 0 15.556a1 1 0 001.414-1.414 9 9 0 010-12.728zm14.142-1.414a1 1 0 10-1.414 1.414 9 9 0 010 12.728 1 1 0 101.414 1.414c4.296-4.296 4.296-11.26 0-15.556zM8.464 8.464A1 1 0 007.05 7.05a7 7 0 000 9.9 1 1 0 101.414-1.414 5 5 0 010-7.072zM16.95 7.05a1 1 0 10-1.414 1.414 5 5 0 010 7.072 1 1 0 001.414 1.414 7 7 0 000-9.9zM9 12a3 3 0 116 0 3 3 0 01-6 0z" fill="currentColor"/></svg></span>
{:else}
<span>{ i18n.gettext('Offline') } <svg width="24" height="24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414L15.535 16.95l2.829 2.828 1.929 1.93a1 1 0 001.414-1.415l-1.253-1.254c3.607-4.321 3.382-10.76-.676-14.817a1 1 0 10-1.414 1.414 9.001 9.001 0 01.668 11.982l-1.425-1.425a7.002 7.002 0 00-.657-9.143 1 1 0 10-1.414 1.414 5.002 5.002 0 01.636 6.294l-1.465-1.465a3 3 0 00-4-4l-7-7zM3.75 8.4a1 1 0 00-1.834-.8C.161 11.624.928 16.485 4.222 19.778a1 1 0 001.414-1.414A9.004 9.004 0 013.749 8.4zm3.32 2.766a1 1 0 00-1.972-.332A6.992 6.992 0 007.05 16.95a1 1 0 101.414-1.414 4.993 4.993 0 01-1.394-4.37z" fill="currentColor"/></svg></span>
{/if}
</div>