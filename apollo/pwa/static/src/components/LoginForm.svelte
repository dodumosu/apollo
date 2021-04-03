<script>
  import { Loading, Report } from 'notiflix';
  import { createEventDispatcher } from 'svelte';

  export let apiClient, i18n;

  const dispatch = createEventDispatcher();
  let participant_id, password;

  const authenticate = () => {
    let participant;

    Loading.Standard(i18n.gettext('Please wait'));

    apiClient.authenticate(participant_id, password)
      .then((response) => {
        Loading.Remove();
        dispatch('authenticated', {participant: response.data.data.participant});
      })
      .catch(error => {
        Loading.Remove();

        switch (error.status) {
          case 403:
            Report.Failure(
              i18n.gettext('Error'),
              i18n.gettext('Please check your credentials and try again'),
              i18n.gettext('OK')
            );
            break;
          default:
            Report.Failure(
              i18n.gettext('Error'),
              i18n.gettext('An error occurred contacting the server'),
              i18n.gettext('OK')
            );
        }
      });
  };
</script>

<div class="row">
  <div class="col">
    <div class="form-signin">
      <form>
        <div class="card shadow-sm mt-3">
          <div class="h5 card-header">{ i18n.gettext('Login') }</div>
          <div class="card-body">
            <div class="mb-3">
              <label for="participant_id" class="visually-hidden">{ i18n.gettext('Participant ID') }</label>
              <input type="text" class="form-control bg-light" id="participant_id" placeholder="{ i18n.gettext('Participant ID') }" bind:value="{participant_id}">
            </div>
            <div class="mb-3">
              <label for="password" class="visually-hidden">{ i18n.gettext('Password') }</label>
              <input type="password" class="form-control bg-light" id="password" placeholder="{ i18n.gettext('Password') }" bind:value="{password}">
            </div>
            <div class="mb-3">
              <div class="d-grid gap-2">
                <button class="btn btn-primary" on:click|preventDefault={authenticate}>{ i18n.gettext('Login') }</button>
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</div>