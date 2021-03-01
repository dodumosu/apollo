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
    <div class="col">
        <div class="form-signin">
            <form>
                <div class="card shadow-sm">
                    <h5 class="card-header">{ i18n.gettext('Login') }</h5>
                    <div class="card-body">
                        <div class="mb-3">
                            <label for="participant_id" class="visually-hidden">{ i18n.gettext('Participant ID') }</label>
                            <input type="text" class="form-control bg-light" id="participant_id" placeholder="{i18n.gettext('Participant ID')}" bind:value={participant_id}>
                        </div>
                        <div class="mb-3">
                            <label for="password" class="visually-hidden">{ i18n.gettext('Password') }</label>
                            <input type="password" class="form-control bg-light" id="password" placeholder="{i18n.gettext('Password')}" bind:value={password}>
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