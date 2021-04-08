<script>
  import gettext from 'gettext.js';
  import { onMount } from 'svelte/internal';
  import { getCookie } from 'tiny-cookie';

  import APIClient from './client';
  import ApolloDatabase from './database';
  import FormList from './components/FormList.svelte';
  import LoginForm from './components/LoginForm.svelte';
  import Navbar from './components/Navbar.svelte';
  import Welcome from './components/Welcome.svelte';

  const endpoints = {
    formData: '/api/participants/forms',
    login: '/api/participants/login',
    logout: '/api/participants/logout',
    submit: '/api/submissions',
  };

  const i18n = new gettext();
  const apiClient = new APIClient(endpoints);
  const appDatabase = new ApolloDatabase();
  const browserCapabilities = {
    canDoBackgroundSync: 'SyncManager' in window,
    canDoPeriodicSync: 'periodicSync' in ServiceWorkerRegistration,
    canGetLocation: 'geolocation' in navigator,
    canUsePermissions: 'permissions' in navigator
  };

  let allowLocationAccess = false;
  let currentForm = null, participant = null;

  const onAppMount = () => {
    appDatabase.getParticipant()
      .then(dbParticipant => {
        participant = dbParticipant;
      })
      .catch(error => console.error(error));
  };

  const retrieveForms = () => {
    apiClient.getFormData()
      .then((response) => {
        let forms = response.data.data.forms.map(form => Object.assign(form, {participant_id: participant.participant_id}));
        let serials = response.data.data.serials
          .map(si => Object.assign({participant_id: participant.participant_id}, si));

        if (forms.length > 0)
          appDatabase.saveForms(forms);

        if (serials.length > 0)
          appDatabase.saveSerials(serials);
      });
  };

  const authSuccess = (event) => {
    participant = event.detail.participant;
    participant.lastLogin = new Date();

    appDatabase.saveParticipant(participant);
    retrieveForms();
  };

  const logout = () => {
    apiClient.logout(getCookie('csrf_access_token'))
      .finally(() => {
        participant = null;
      });
  };

  const locationAccessToggled = (event) => {
    allowLocationAccess = event.detail.status;
  };

  onMount(onAppMount);
</script>

<Navbar {i18n}/>
<main class="container h-100">
  <div class="row h-75 align-items-center">
    <div class="col-sm-10 offset-sm-1 mt-3">
      {#if participant === null}
      <LoginForm {apiClient} {i18n} on:authenticated={authSuccess}/>
      {:else}
      <Welcome {i18n} {participant} on:logged-out={logout} on:location-access-toggled={locationAccessToggled}/>
      {#if currentForm === null}
        <FormList db={appDatabase} {i18n} {participant}/>
      {/if}
      {/if}
    </div>
  </div>
</main>

<style>
</style>