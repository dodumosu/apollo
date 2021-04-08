<script>
  import { createEventDispatcher } from 'svelte/internal';
  export let i18n, participant, unsentSubmissions = 0;

  let dispatch = createEventDispatcher();
  const greeting = () => {
    let hourOfDay = new Date().getHours();
    if (hourOfDay < 12)
      return i18n.gettext('Good morning');
    else if ((12 >= hourOfDay) && (hourOfDay < 17))
      return i18n.gettext('Good afternoon');
    else
      return i18n.gettext('Good evening');
  };

  const logout = () => {
    dispatch('logged-out');
  };

  const toggleLocationAccess = (event) => {
    dispatch('location-access-changed', {status: event.target.checked});
  };
</script>

<div class="row">
  <div class="col">
    <div class="card shadow-sm mt-3">
      <div class="card-body">
        <h5 class="card-title">{ greeting() }, { participant.full_name }</h5>
        <div class="row mb-3">
          <div class="col-4"><strong>{ i18n.gettext('Participant ID') }</strong></div>
          <div class="col">{ participant.participant_id }</div>
        </div>
        <div class="row mb-3">
          <div class="col-4"><strong>{ i18n.gettext('Location') }</strong></div>
          <div class="col">{ participant.location }</div>
        </div>
        <div class="row mb-3">
          <div class="col">{ i18n.gettext('If this is not correct,') } <button class="btn btn-outline-dark" on:click={logout}>{ i18n.gettext('click here') }</button></div>
        </div>
        <div class="row mb-3">
          <div class="col">
            <div class="form-check">
              <input type="checkbox" id="location-access-toggle" class="form-check-input" on:change={toggleLocationAccess}>
              <label for="location-access-toggle" class="form-check-label">{ i18n.gettext('Allow access to your location as needed') }</label>
            </div>
          </div>
        </div>
        {#if unsentSubmissions > 0}
        <div class="row">
          <div class="col">
            <div class="alert alert-info"></div>
          </div>
        </div>
        {/if}
      </div>
    </div>
  </div>
</div>