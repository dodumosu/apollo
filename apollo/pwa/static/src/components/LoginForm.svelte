<script>
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    let participant_id, password;

    export let i18n;

    const handleLogin = () => {
        dispatch('authenticate', {
            participant_id, password
        });
    }
</script>

<div class="row">
    <div class="col-sm-4 offset-sm-4">
        <div class="form-signin">
            <form>
                <div class="card shadow-sm mt-3">
                    <h5 class="card-header">{ i18n.gettext('Login') }</h5>
                    <div class="card-body">
                        <div class="mb-3">
                            <label for="participant_id" class="visually-hidden">{ i18n.gettext('Participant ID') }</label>
                            <div class="input-group">
                                <span class="input-group-text"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-user"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg></span>
                                <input type="text" class="form-control bg-light" id="participant_id" placeholder="{i18n.gettext('Participant ID')}" bind:value={participant_id}>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="password" class="visually-hidden">{ i18n.gettext('Password') }</label>
                            <div class="input-group">
                                <span class="input-group-text"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-lock"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg></span>
                                <input type="password" class="form-control bg-light" id="password" placeholder="{i18n.gettext('Password')}" bind:value={password}>
                            </div>
                        </div>
                        <div class="mb-3">
                            <div class="d-grid gap-2">
                                <button class="btn btn-primary" on:click|preventDefault={handleLogin} disabled={!navigator.onLine}>{ i18n.gettext('Login') }</button>
                            </div>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>